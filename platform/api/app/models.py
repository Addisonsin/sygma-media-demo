from __future__ import annotations  # required for SQLAlchemy on Python 3.9

import enum
import uuid
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    pass


class UserRole(str, enum.Enum):
    agency_super_admin = "agency_super_admin"
    agency_staff = "agency_staff"
    client_owner = "client_owner"
    client_editor = "client_editor"


class ContentStatus(str, enum.Enum):
    draft = "draft"
    published = "published"


class PublishJobStatus(str, enum.Enum):
    queued = "queued"
    running = "running"
    succeeded = "succeeded"
    failed = "failed"
    cancelled = "cancelled"


class Agency(Base):
    __tablename__ = "agencies"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    clients: Mapped[list[Client]] = relationship(back_populates="agency")
    users: Mapped[list[User]] = relationship(back_populates="agency")


class Client(Base):
    __tablename__ = "clients"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agency_id: Mapped[str] = mapped_column(ForeignKey("agencies.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    agency: Mapped[Agency] = relationship(back_populates="clients")
    websites: Mapped[list[Website]] = relationship(back_populates="client")
    memberships: Mapped[list[WebsiteMembership]] = relationship(back_populates="client")


class User(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agency_id: Mapped[Optional[str]] = mapped_column(ForeignKey("agencies.id"), index=True)
    client_id: Mapped[Optional[str]] = mapped_column(ForeignKey("clients.id"), index=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    client_editing_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    agency: Mapped[Optional[Agency]] = relationship(back_populates="users")
    memberships: Mapped[list[WebsiteMembership]] = relationship(back_populates="user")


class Website(Base):
    __tablename__ = "websites"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False, index=True)
    slug: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    public_domain: Mapped[Optional[str]] = mapped_column(String(255))
    static_root: Mapped[str] = mapped_column(Text, nullable=False)
    cf_pages_project: Mapped[Optional[str]] = mapped_column(String(128))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    client: Mapped[Client] = relationship(back_populates="websites")
    documents: Mapped[list[ContentDocument]] = relationship(back_populates="website")
    publish_jobs: Mapped[list[PublishJob]] = relationship(back_populates="website")


class WebsiteMembership(Base):
    __tablename__ = "website_memberships"
    __table_args__ = (UniqueConstraint("website_id", "user_id", name="uq_website_user"),)

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    website_id: Mapped[str] = mapped_column(ForeignKey("websites.id"), nullable=False, index=True)
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    client_id: Mapped[str] = mapped_column(ForeignKey("clients.id"), nullable=False, index=True)
    can_edit: Mapped[bool] = mapped_column(Boolean, default=True)
    can_publish: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped[User] = relationship(back_populates="memberships")
    client: Mapped[Client] = relationship(back_populates="memberships")


class ContentDocument(Base):
    __tablename__ = "content_documents"
    __table_args__ = (
        UniqueConstraint("website_id", "doc_type", "doc_key", name="uq_content_doc"),
        Index("ix_content_website_type", "website_id", "doc_type"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    website_id: Mapped[str] = mapped_column(ForeignKey("websites.id"), nullable=False)
    doc_type: Mapped[str] = mapped_column(String(64), nullable=False)
    doc_key: Mapped[str] = mapped_column(String(128), nullable=False, default="default")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, onupdate=utcnow)

    website: Mapped[Website] = relationship(back_populates="documents")
    revisions: Mapped[list[ContentRevision]] = relationship(back_populates="document")


class ContentRevision(Base):
    __tablename__ = "content_revisions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id: Mapped[str] = mapped_column(ForeignKey("content_documents.id"), nullable=False, index=True)
    website_id: Mapped[str] = mapped_column(ForeignKey("websites.id"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ContentStatus] = mapped_column(Enum(ContentStatus), nullable=False)
    payload: Mapped[dict] = mapped_column(JSON, nullable=False)
    created_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    note: Mapped[Optional[str]] = mapped_column(String(512))

    document: Mapped[ContentDocument] = relationship(back_populates="revisions")


class MediaAsset(Base):
    __tablename__ = "media_assets"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    website_id: Mapped[str] = mapped_column(ForeignKey("websites.id"), nullable=False, index=True)
    logical_key: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    storage_path: Mapped[str] = mapped_column(Text, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(128), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    width: Mapped[Optional[int]] = mapped_column(Integer)
    height: Mapped[Optional[int]] = mapped_column(Integer)
    alt_text: Mapped[Optional[str]] = mapped_column(String(512))
    usage_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class PublishJob(Base):
    __tablename__ = "publish_jobs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    website_id: Mapped[str] = mapped_column(ForeignKey("websites.id"), nullable=False, index=True)
    status: Mapped[PublishJobStatus] = mapped_column(Enum(PublishJobStatus), default=PublishJobStatus.queued)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    triggered_by_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    build_path: Mapped[Optional[str]] = mapped_column(Text)
    error_message: Mapped[Optional[str]] = mapped_column(Text)
    deploy_attempted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    website: Mapped[Website] = relationship(back_populates="publish_jobs")


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    website_id: Mapped[Optional[str]] = mapped_column(ForeignKey("websites.id"), index=True)
    user_id: Mapped[Optional[str]] = mapped_column(ForeignKey("users.id"))
    action: Mapped[str] = mapped_column(String(64), nullable=False)
    detail: Mapped[Optional[dict]] = mapped_column(JSON)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
