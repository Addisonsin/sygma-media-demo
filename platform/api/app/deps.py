from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User, UserRole, Website, WebsiteMembership
from app.security import decode_token

bearer = HTTPBearer(auto_error=False)


def get_current_user(
    creds: Optional[HTTPAuthorizationCredentials] = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    if not creds:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    try:
        payload = decode_token(creds.credentials)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from None
    user = db.get(User, payload.get("sub"))
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User inactive")
    return user


def is_agency_user(user: User) -> bool:
    return user.role in (UserRole.agency_super_admin, UserRole.agency_staff)


def require_website_access(
    website_id: str,
    user: User,
    db: Session,
    *,
    require_publish: bool = False,
) -> Website:
    website = db.get(Website, website_id)
    if not website:
        raise HTTPException(status_code=404, detail="Website not found")

    if is_agency_user(user) and user.agency_id == website.client.agency_id:
        return website

    if not user.client_editing_enabled:
        raise HTTPException(status_code=403, detail="Client editing disabled")

    stmt = select(WebsiteMembership).where(
        WebsiteMembership.website_id == website_id,
        WebsiteMembership.user_id == user.id,
    )
    membership = db.scalar(stmt)
    if not membership:
        raise HTTPException(status_code=403, detail="No access to this website")
    if require_publish and not membership.can_publish:
        raise HTTPException(status_code=403, detail="Publish not permitted")
    if not membership.can_edit and not require_publish:
        raise HTTPException(status_code=403, detail="Edit not permitted")
    return website


def audit(
    db: Session,
    user: Optional[User],
    action: str,
    website_id: Optional[str] = None,
    detail: Optional[dict] = None,
) -> None:
    from app.models import AuditLog

    db.add(AuditLog(website_id=website_id, user_id=user.id if user else None, action=action, detail=detail))
    db.commit()
