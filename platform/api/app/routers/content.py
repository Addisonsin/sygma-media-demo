from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import audit, get_current_user, require_website_access
from app.models import ContentDocument, ContentRevision, ContentStatus, User
from app.schemas_api import ContentRevisionOut, ContentSaveRequest
from app.services.validation import validate_doc

router = APIRouter(prefix="/websites/{website_id}/content", tags=["content"])


@router.get("/documents")
def list_documents(
    website_id: str,
    doc_type: Optional[str] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> List[dict]:
    require_website_access(website_id, user, db)
    stmt = select(ContentDocument).where(ContentDocument.website_id == website_id)
    if doc_type:
        stmt = stmt.where(ContentDocument.doc_type == doc_type)
    docs = db.scalars(stmt.order_by(ContentDocument.updated_at.desc())).all()
    out = []
    for doc in docs:
        draft = db.scalar(
            select(ContentRevision)
            .where(ContentRevision.document_id == doc.id, ContentRevision.status == ContentStatus.draft)
            .order_by(ContentRevision.version.desc())
            .limit(1)
        )
        pub = db.scalar(
            select(ContentRevision)
            .where(ContentRevision.document_id == doc.id, ContentRevision.status == ContentStatus.published)
            .order_by(ContentRevision.version.desc())
            .limit(1)
        )
        title = None
        if doc.doc_type == "blog_post" and draft:
            title = (draft.payload or {}).get("title")
        elif doc.doc_type == "blog_post" and pub:
            title = (pub.payload or {}).get("title")
        out.append(
            {
                "doc_type": doc.doc_type,
                "doc_key": doc.doc_key,
                "updated_at": doc.updated_at.isoformat() if doc.updated_at else None,
                "has_draft": draft is not None,
                "has_published": pub is not None,
                "title": title,
            }
        )
    return out


def _next_version(db: Session, document_id: str) -> int:
    rev = db.scalar(
        select(ContentRevision)
        .where(ContentRevision.document_id == document_id)
        .order_by(ContentRevision.version.desc())
        .limit(1)
    )
    return (rev.version + 1) if rev else 1


@router.get("/{doc_type}/{doc_key}", response_model=Optional[ContentRevisionOut])
def get_latest(
    website_id: str,
    doc_type: str,
    doc_key: str,
    status: str = "draft",
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ContentRevision | None:
    require_website_access(website_id, user, db)
    doc = db.scalar(
        select(ContentDocument).where(
            ContentDocument.website_id == website_id,
            ContentDocument.doc_type == doc_type,
            ContentDocument.doc_key == doc_key,
        )
    )
    if not doc:
        return None
    try:
        st = ContentStatus(status)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid status filter") from exc
    return db.scalar(
        select(ContentRevision)
        .where(ContentRevision.document_id == doc.id, ContentRevision.status == st)
        .order_by(ContentRevision.version.desc())
        .limit(1)
    )


@router.post("/save", response_model=ContentRevisionOut)
def save_content(
    website_id: str,
    body: ContentSaveRequest,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> ContentRevision:
    require_website_access(website_id, user, db)
    errors = validate_doc(body.doc_type, body.payload)
    if errors:
        raise HTTPException(status_code=422, detail={"validation_errors": errors})

    doc = db.scalar(
        select(ContentDocument).where(
            ContentDocument.website_id == website_id,
            ContentDocument.doc_type == body.doc_type,
            ContentDocument.doc_key == body.doc_key,
        )
    )
    if not doc:
        doc = ContentDocument(website_id=website_id, doc_type=body.doc_type, doc_key=body.doc_key)
        db.add(doc)
        db.flush()

    status = ContentStatus.published if body.publish else ContentStatus.draft
    rev = ContentRevision(
        document_id=doc.id,
        website_id=website_id,
        version=_next_version(db, doc.id),
        status=status,
        payload=body.payload,
        created_by_id=user.id,
        note=body.note,
    )
    db.add(rev)
    db.commit()
    db.refresh(rev)
    audit(db, user, "content_save", website_id=website_id, detail={"doc_type": body.doc_type, "version": rev.version})
    return rev


@router.get("/revisions/{doc_type}/{doc_key}", response_model=List[ContentRevisionOut])
def list_revisions(
    website_id: str,
    doc_type: str,
    doc_key: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> List[ContentRevision]:
    require_website_access(website_id, user, db)
    doc = db.scalar(
        select(ContentDocument).where(
            ContentDocument.website_id == website_id,
            ContentDocument.doc_type == doc_type,
            ContentDocument.doc_key == doc_key,
        )
    )
    if not doc:
        return []
    return list(
        db.scalars(
            select(ContentRevision)
            .where(ContentRevision.document_id == doc.id)
            .order_by(ContentRevision.version.desc())
            .limit(50)
        ).all()
    )
