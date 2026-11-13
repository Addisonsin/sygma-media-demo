from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.db import get_db
from app.deps import audit, get_current_user, is_agency_user
from app.models import AuditLog, Client, PublishJob, User, UserRole, Website, WebsiteMembership
from app.schemas_api import (
    AuditLogOut,
    ClientCreate,
    ClientOut,
    PublishJobAgencyOut,
    UserClientCreate,
    WebsiteCreate,
    WebsiteOut,
)
from app.security import hash_password

router = APIRouter(prefix="/agency", tags=["agency"])


@router.get("/clients", response_model=List[ClientOut])
def list_clients(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> List[Client]:
    if not is_agency_user(user):
        raise HTTPException(status_code=403, detail="Agency role required")
    stmt = (
        select(Client)
        .where(Client.agency_id == user.agency_id)
        .options(joinedload(Client.websites))
        .order_by(Client.name)
    )
    return list(db.scalars(stmt).unique().all())


@router.post("/clients", response_model=ClientOut)
def create_client(body: ClientCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Client:
    if user.role != UserRole.agency_super_admin:
        raise HTTPException(status_code=403, detail="Super admin required")
    client = Client(agency_id=user.agency_id, name=body.name)
    db.add(client)
    db.commit()
    db.refresh(client)
    audit(db, user, "client_create", detail={"client_id": client.id})
    return client


@router.post("/websites", response_model=WebsiteOut)
def create_website(body: WebsiteCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Website:
    if user.role != UserRole.agency_super_admin:
        raise HTTPException(status_code=403, detail="Super admin required")
    client = db.get(Client, body.client_id)
    if not client or client.agency_id != user.agency_id:
        raise HTTPException(status_code=404, detail="Client not found")
    website = Website(
        client_id=client.id,
        slug=body.slug,
        name=body.name,
        public_domain=body.public_domain,
        static_root=body.static_root,
        cf_pages_project=body.cf_pages_project,
    )
    db.add(website)
    db.commit()
    db.refresh(website)
    audit(db, user, "website_create", website_id=website.id)
    return website


@router.post("/users/client")
def create_client_user(body: UserClientCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    if user.role != UserRole.agency_super_admin:
        raise HTTPException(status_code=403, detail="Super admin required")
    try:
        role = UserRole(body.role)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail="Invalid role") from exc
    if role not in (UserRole.client_owner, UserRole.client_editor):
        raise HTTPException(status_code=400, detail="Client role required")

    websites = []
    client_id = None
    for wid in body.website_ids:
        w = db.get(Website, wid)
        if not w or w.client.agency_id != user.agency_id:
            raise HTTPException(status_code=404, detail=f"Website {wid} not found")
        client_id = w.client_id
        websites.append(w)

    new_user = User(
        agency_id=user.agency_id,
        client_id=client_id,
        email=body.email,
        password_hash=hash_password(body.password),
        role=role,
    )
    db.add(new_user)
    db.flush()
    for w in websites:
        db.add(
            WebsiteMembership(
                website_id=w.id,
                user_id=new_user.id,
                client_id=w.client_id,
                can_edit=True,
                can_publish=body.can_publish,
            )
        )
    db.commit()
    audit(db, user, "client_user_create", detail={"user_id": new_user.id})
    return {"id": new_user.id, "email": new_user.email}


@router.get("/publish/jobs", response_model=List[PublishJobAgencyOut])
def agency_publish_jobs(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 50,
) -> List[dict]:
    if not is_agency_user(user):
        raise HTTPException(status_code=403, detail="Agency role required")
    stmt = (
        select(PublishJob, Website)
        .join(Website, PublishJob.website_id == Website.id)
        .join(Client, Website.client_id == Client.id)
        .where(Client.agency_id == user.agency_id)
        .order_by(PublishJob.created_at.desc())
        .limit(min(limit, 100))
    )
    rows = db.execute(stmt).all()
    out = []
    for job, website in rows:
        out.append(
            {
                "id": job.id,
                "status": job.status.value,
                "build_path": job.build_path,
                "error_message": job.error_message,
                "deploy_attempted": job.deploy_attempted,
                "created_at": job.created_at,
                "website_id": website.id,
                "website_name": website.name,
                "website_slug": website.slug,
            }
        )
    return out


@router.get("/audit", response_model=List[AuditLogOut])
def agency_audit(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
    limit: int = 80,
) -> List[AuditLog]:
    if not is_agency_user(user):
        raise HTTPException(status_code=403, detail="Agency role required")
    site_ids = select(Website.id).join(Client).where(Client.agency_id == user.agency_id)
    stmt = (
        select(AuditLog)
        .where(AuditLog.website_id.in_(site_ids))
        .order_by(AuditLog.created_at.desc())
        .limit(min(limit, 200))
    )
    return list(db.scalars(stmt).all())
