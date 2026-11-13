from __future__ import annotations

import shutil
import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.config import settings

ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp", "image/gif", "image/svg+xml"}
MAX_BYTES = 15 * 1024 * 1024


async def save_local_media(website_id: str, logical_key: str, file: UploadFile) -> tuple[str, int, str]:
    if settings.media_backend != "local":
        raise HTTPException(status_code=503, detail={"code": "CONFIG_MISSING", "message": "R2 backend not wired yet"})

    content_type = file.content_type or "application/octet-stream"
    if content_type not in ALLOWED_MIME:
        raise HTTPException(status_code=400, detail="Unsupported image type")

    data = await file.read()
    if len(data) > MAX_BYTES:
        raise HTTPException(status_code=400, detail="File too large")

    ext = Path(file.filename or "upload.bin").suffix.lower() or ".bin"
    dest_dir = settings.media_local_root / website_id
    dest_dir.mkdir(parents=True, exist_ok=True)
    storage_name = f"{uuid.uuid4().hex}{ext}"
    dest = dest_dir / storage_name
    dest.write_bytes(data)

    rel = str(dest.relative_to(settings.media_local_root))
    return rel, len(data), content_type


def delete_local_media(storage_path: str) -> None:
    path = settings.media_local_root / storage_path
    if path.is_file():
        path.unlink()
