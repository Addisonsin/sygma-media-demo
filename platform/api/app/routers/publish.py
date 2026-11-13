from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import audit, get_current_user, require_website_access
from app.models import PublishJob, User
from app.schemas_api import PublishJobOut
from app.services.publish import PublishConflict, enqueue_publish

router = APIRouter(prefix="/websites/{website_id}/publish", tags=["publish"])


@router.post("", response_model=PublishJobOut)
def start_publish(
    website_id: str,
    deploy: bool = False,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PublishJob:
    website = require_website_access(website_id, user, db, require_publish=True)
    try:
        job = enqueue_publish(db, website, user.id, deploy=deploy)
    except PublishConflict as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    audit(db, user, "publish", website_id=website_id, detail={"job_id": job.id, "status": job.status.value})
    return job


@router.get("/jobs", response_model=List[PublishJobOut])
def list_jobs(
    website_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> List[PublishJob]:
    require_website_access(website_id, user, db)
    return list(
        db.scalars(
            select(PublishJob).where(PublishJob.website_id == website_id).order_by(PublishJob.created_at.desc()).limit(25)
        ).all()
    )
