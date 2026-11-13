from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user, require_website_access
from app.models import ContentDocument, MediaAsset, PublishJob, PublishJobStatus, User

router = APIRouter(prefix="/websites/{website_id}/overview", tags=["overview"])


@router.get("")
def website_overview(
    website_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    require_website_access(website_id, user, db)
    doc_count = db.scalar(select(func.count()).select_from(ContentDocument).where(ContentDocument.website_id == website_id))
    media_count = db.scalar(select(func.count()).select_from(MediaAsset).where(MediaAsset.website_id == website_id))
    last_job = db.scalar(
        select(PublishJob)
        .where(PublishJob.website_id == website_id)
        .order_by(PublishJob.created_at.desc())
        .limit(1)
    )
    blog_count = db.scalar(
        select(func.count())
        .select_from(ContentDocument)
        .where(ContentDocument.website_id == website_id, ContentDocument.doc_type == "blog_post")
    )
    return {
        "content_documents": doc_count or 0,
        "media_assets": media_count or 0,
        "blog_posts_managed": blog_count or 0,
        "last_publish_status": last_job.status.value if last_job else None,
        "last_publish_at": last_job.finished_at.isoformat() if last_job and last_job.finished_at else None,
    }
