from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import ContentDocument, ContentRevision, ContentStatus, PublishJob, PublishJobStatus, Website
from app.services.html_patch import apply_manifest_to_build


class PublishConflict(Exception):
    pass


class PublishConfigMissing(Exception):
    pass


def _active_job(db: Session, website_id: str) -> PublishJob | None:
    stmt = select(PublishJob).where(
        PublishJob.website_id == website_id,
        PublishJob.status.in_((PublishJobStatus.queued, PublishJobStatus.running)),
    )
    return db.scalar(stmt)


def gather_published_manifest(db: Session, website_id: str) -> dict:
    docs = db.scalars(select(ContentDocument).where(ContentDocument.website_id == website_id)).all()
    manifest: dict = {"documents": {}}
    for doc in docs:
        rev = db.scalar(
            select(ContentRevision)
            .where(
                ContentRevision.document_id == doc.id,
                ContentRevision.status == ContentStatus.published,
            )
            .order_by(ContentRevision.version.desc())
            .limit(1)
        )
        if rev:
            manifest["documents"][f"{doc.doc_type}:{doc.doc_key}"] = rev.payload
    return manifest


def apply_published_html(build_root: Path, manifest: dict) -> dict:
    report = apply_manifest_to_build(build_root, manifest)
    meta_path = build_root / "_cms_manifest.json"
    meta_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def run_publish_job(db: Session, job: PublishJob, website: Website, *, deploy: bool = False) -> None:
    job.status = PublishJobStatus.running
    job.started_at = datetime.now(timezone.utc)
    db.commit()

    try:
        source = Path(website.static_root)
        if not source.is_dir():
            raise FileNotFoundError(f"static_root missing: {source}")

        build_dir = settings.publish_output_root / website.slug / job.id
        if build_dir.exists():
            shutil.rmtree(build_dir)
        shutil.copytree(source, build_dir, dirs_exist_ok=False)

        manifest = gather_published_manifest(db, website.id)
        manifest["website_id"] = website.id
        manifest["built_at"] = datetime.now(timezone.utc).isoformat()
        (build_dir / "_cms_full_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        apply_published_html(build_dir, manifest)
        job.build_path = str(build_dir.resolve())
        job.status = PublishJobStatus.succeeded
        job.finished_at = datetime.now(timezone.utc)

        if deploy:
            if not settings.cf_configured:
                raise PublishConfigMissing("Cloudflare API credentials not configured")
            job.deploy_attempted = True
            # Phase 2+: wrangler/API upload — intentionally not invoked without credentials
            raise PublishConfigMissing("Deploy adapter not enabled in Phase 1 (build only)")

    except Exception as exc:
        job.status = PublishJobStatus.failed
        job.error_message = str(exc)
        job.finished_at = datetime.now(timezone.utc)
    finally:
        db.commit()


def enqueue_publish(db: Session, website: Website, user_id: str, *, deploy: bool = False) -> PublishJob:
    active = _active_job(db, website.id)
    if active:
        raise PublishConflict("A publish job is already in progress for this website")

    job = PublishJob(website_id=website.id, triggered_by_id=user_id)
    db.add(job)
    db.commit()
    db.refresh(job)
    run_publish_job(db, job, website, deploy=deploy)
    db.refresh(job)
    return job
