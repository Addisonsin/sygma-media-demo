from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import Agency, Client, ContentDocument, ContentRevision, ContentStatus, User, UserRole, Website
from app.security import hash_password


def init_db_schema(engine) -> None:
    from app.models import Base

    Base.metadata.create_all(bind=engine)
    Path("./data").mkdir(parents=True, exist_ok=True)
    settings.media_local_root.mkdir(parents=True, exist_ok=True)
    settings.publish_output_root.mkdir(parents=True, exist_ok=True)


def seed_if_empty(db: Session) -> None:
    if db.scalar(select(Agency).limit(1)):
        return

    agency = Agency(name=settings.bootstrap_agency_name)
    db.add(agency)
    db.flush()

    client = Client(agency_id=agency.id, name="Sygma Media")
    db.add(client)
    db.flush()

    static_root = str(settings.static_site_root.resolve())
    website = Website(
        client_id=client.id,
        slug="sygma-media",
        name="Sygma Media",
        public_domain="sygmamedia.com",
        static_root=static_root,
        cf_pages_project=settings.cloudflare_pages_project or "sygma-media",
    )
    db.add(website)
    db.flush()

    admin = User(
        agency_id=agency.id,
        email=settings.bootstrap_admin_email,
        password_hash=hash_password(settings.bootstrap_admin_password),
        role=UserRole.agency_super_admin,
    )
    db.add(admin)

    home_doc = ContentDocument(website_id=website.id, doc_type="homepage", doc_key="default")
    db.add(home_doc)
    db.flush()

    home_payload = {
        "hero": {
            "line1": "The U.S. Aesthetics",
            "line2_emphasis": "Marketing Agency.",
            "meta_title": "U.S. Aesthetic Marketing Agency | Sygma Media LLC",
            "meta_description": (
                "The US aesthetic clinic marketing agency for clinics and plastic surgeons, "
                "specializing in SEO, AI search, Google Maps, and high-converting clinic websites."
            ),
        }
    }
    db.add(
        ContentRevision(
            document_id=home_doc.id,
            website_id=website.id,
            version=1,
            status=ContentStatus.published,
            payload=home_payload,
            created_by_id=admin.id,
            note="bootstrap-from-live-site",
        )
    )

    settings_doc = ContentDocument(website_id=website.id, doc_type="site_settings", doc_key="default")
    db.add(settings_doc)
    db.flush()
    db.add(
        ContentRevision(
            document_id=settings_doc.id,
            website_id=website.id,
            version=1,
            status=ContentStatus.published,
            payload={
                "business_name": "Sygma Media",
                "phone_display": "+1 (212) 555-0147",
                "phone_e164": "+12125550147",
                "whatsapp_e164": "+12125550147",
                "email": "exec@sygmamedia.com",
            },
            created_by_id=admin.id,
            note="bootstrap-from-live-site",
        )
    )
    db.commit()
