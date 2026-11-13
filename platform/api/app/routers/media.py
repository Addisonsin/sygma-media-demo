from typing import List, Optional

from pathlib import Path

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import audit, get_current_user, require_website_access
from app.models import MediaAsset, User
from app.schemas_api import MediaOut
from app.config import settings
from app.services.media_storage import delete_local_media, save_local_media

router = APIRouter(prefix="/websites/{website_id}/media", tags=["media"])


@router.get("", response_model=List[MediaOut])
def list_media(website_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> List[MediaAsset]:
    require_website_access(website_id, user, db)
    return list(db.scalars(select(MediaAsset).where(MediaAsset.website_id == website_id).order_by(MediaAsset.created_at.desc())).all())


@router.post("/upload", response_model=MediaOut)
async def upload_media(
    website_id: str,
    logical_key: str = Form(...),
    alt_text: Optional[str] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> MediaAsset:
    require_website_access(website_id, user, db)
    storage_path, size, mime = await save_local_media(website_id, logical_key, file)

    existing = db.scalar(
        select(MediaAsset).where(MediaAsset.website_id == website_id, MediaAsset.logical_key == logical_key)
    )
    if existing:
        if existing.usage_count > 0:
            # keep old file until publish replaces refs — mark replacement in Phase 3
            delete_local_media(existing.storage_path)
        existing.storage_path = storage_path
        existing.size_bytes = size
        existing.mime_type = mime
        if alt_text is not None:
            existing.alt_text = alt_text
        db.commit()
        db.refresh(existing)
        audit(db, user, "media_replace", website_id=website_id, detail={"logical_key": logical_key})
        return existing

    asset = MediaAsset(
        website_id=website_id,
        logical_key=logical_key,
        storage_path=storage_path,
        mime_type=mime,
        size_bytes=size,
        alt_text=alt_text,
    )
    db.add(asset)
    db.commit()
    db.refresh(asset)
    audit(db, user, "media_upload", website_id=website_id, detail={"logical_key": logical_key})
    return asset


@router.get("/{asset_id}/file")
def media_file(
    website_id: str,
    asset_id: str,
    access_token: str = Query(...),
    db: Session = Depends(get_db),
) -> FileResponse:
    from app.security import decode_token

    try:
        payload = decode_token(access_token)
        user = db.get(User, payload.get("sub"))
    except ValueError:
        raise HTTPException(status_code=401, detail="Invalid token") from None
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    require_website_access(website_id, user, db)
    asset = db.get(MediaAsset, asset_id)
    if not asset or asset.website_id != website_id:
        raise HTTPException(status_code=404, detail="Not found")
    path = (settings.media_local_root / asset.storage_path).resolve()
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File missing")
    return FileResponse(path, media_type=asset.mime_type)


@router.delete("/{asset_id}")
def delete_media(
    website_id: str,
    asset_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    require_website_access(website_id, user, db)
    asset = db.get(MediaAsset, asset_id)
    if not asset or asset.website_id != website_id:
        raise HTTPException(status_code=404, detail="Not found")
    if asset.usage_count > 0:
        raise HTTPException(status_code=409, detail="Image is in use")
    delete_local_media(asset.storage_path)
    db.delete(asset)
    db.commit()
    audit(db, user, "media_delete", website_id=website_id, detail={"asset_id": asset_id})
    return {"ok": True}
