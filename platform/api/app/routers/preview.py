from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user, require_website_access
from app.models import PublishJob, PublishJobStatus, User
from app.schemas_api import PreviewInfoOut
from app.security import decode_token

router = APIRouter(prefix="/websites/{website_id}/preview", tags=["preview"])


def _latest_build(db: Session, website_id: str) -> Optional[PublishJob]:
    return db.scalar(
        select(PublishJob)
        .where(PublishJob.website_id == website_id, PublishJob.status == PublishJobStatus.succeeded)
        .order_by(PublishJob.finished_at.desc())
        .limit(1)
    )


@router.get("/latest", response_model=PreviewInfoOut)
def preview_latest(
    website_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PreviewInfoOut:
    require_website_access(website_id, user, db)
    job = _latest_build(db, website_id)
    if not job or not job.build_path:
        raise HTTPException(status_code=404, detail="No successful build yet")
    index = Path(job.build_path) / "index.html"
    if not index.is_file():
        raise HTTPException(status_code=404, detail="Build missing index.html")
    return PreviewInfoOut(
        job_id=job.id,
        build_path=job.build_path,
        homepage_preview_url=f"/api/v1/websites/{website_id}/preview/files/index.html",
    )


def _user_from_preview_token(db: Session, access_token: str) -> User:
    try:
        payload = decode_token(access_token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail="Invalid preview token") from exc
    user = db.get(User, payload.get("sub"))
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User inactive")
    return user


@router.get("/files/{file_path:path}")
def preview_file(
    file_path: str,
    website_id: str,
    access_token: str = Query(..., description="JWT for browser preview tab"),
    db: Session = Depends(get_db),
) -> FileResponse:
    user = _user_from_preview_token(db, access_token)
    require_website_access(website_id, user, db)
    job = _latest_build(db, website_id)
    if not job or not job.build_path:
        raise HTTPException(status_code=404, detail="No build")
    root = Path(job.build_path).resolve()
    target = (root / file_path).resolve()
    if not str(target).startswith(str(root)) or not target.is_file():
        raise HTTPException(status_code=404, detail="Not found")
    return FileResponse(target)
