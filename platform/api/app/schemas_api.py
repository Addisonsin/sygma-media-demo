from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class ClientCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class WebsiteCreate(BaseModel):
    client_id: str
    slug: str = Field(pattern=r"^[a-z0-9-]+$", max_length=64)
    name: str
    public_domain: Optional[str] = None
    static_root: str
    cf_pages_project: Optional[str] = None


class WebsiteOut(BaseModel):
    id: str
    client_id: str
    slug: str
    name: str
    public_domain: Optional[str]
    static_root: str
    cf_pages_project: Optional[str]

    class Config:
        from_attributes = True


class ClientOut(BaseModel):
    id: str
    agency_id: str
    name: str
    websites: List[WebsiteOut] = []

    class Config:
        from_attributes = True


class ContentSaveRequest(BaseModel):
    doc_type: str
    doc_key: str = "default"
    payload: Dict[str, Any]
    note: Optional[str] = None
    publish: bool = False


class ContentRevisionOut(BaseModel):
    id: str
    version: int
    status: str
    payload: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True


class PublishJobOut(BaseModel):
    id: str
    status: str
    build_path: Optional[str]
    error_message: Optional[str]
    deploy_attempted: bool
    created_at: datetime

    class Config:
        from_attributes = True


class MediaOut(BaseModel):
    id: str
    logical_key: str
    mime_type: str
    size_bytes: int
    width: Optional[int]
    height: Optional[int]
    alt_text: Optional[str]

    class Config:
        from_attributes = True


class UserClientCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=10)
    role: str = "client_owner"
    website_ids: List[str]
    can_publish: bool = True


class PageRouteOut(BaseModel):
    label: str
    path: str
    url: str
    exists: bool
    editable: bool


class PreviewInfoOut(BaseModel):
    job_id: str
    build_path: str
    homepage_preview_url: str


class AuditLogOut(BaseModel):
    id: str
    action: str
    website_id: Optional[str]
    detail: Optional[dict]
    created_at: datetime

    class Config:
        from_attributes = True


class PublishJobAgencyOut(PublishJobOut):
    website_id: str
    website_name: str
    website_slug: str
