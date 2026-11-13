from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.deps import get_current_user, is_agency_user, require_website_access
from app.models import Client, User, Website, WebsiteMembership
from app.schemas_api import WebsiteOut

router = APIRouter(prefix="/websites", tags=["websites"])


@router.get("", response_model=List[WebsiteOut])
def my_websites(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> List[Website]:
    if is_agency_user(user):
        stmt = (
            select(Website)
            .join(Client)
            .where(Client.agency_id == user.agency_id)
            .order_by(Website.name)
        )
        return list(db.scalars(stmt).all())

    stmt = (
        select(Website)
        .join(WebsiteMembership)
        .where(WebsiteMembership.user_id == user.id)
        .order_by(Website.name)
    )
    return list(db.scalars(stmt).all())


@router.get("/{website_id}", response_model=WebsiteOut)
def get_website(website_id: str, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Website:
    return require_website_access(website_id, user, db)
