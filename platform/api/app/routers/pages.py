from pathlib import Path
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.deps import get_current_user, require_website_access
from app.models import User
from app.schemas_api import PageRouteOut

router = APIRouter(prefix="/websites/{website_id}/pages", tags=["pages"])

CURATED = [
    ("Home", "index.html", "/"),
    ("About", "about/index.html", "/about"),
    ("Contact", "contact/index.html", "/contact"),
    ("Services", "services/index.html", "/services"),
    ("Pricing", "pricing/index.html", "/pricing"),
    ("Blog", "blog/index.html", "/blog"),
]


@router.get("", response_model=List[PageRouteOut])
def list_pages(
    website_id: str,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> List[PageRouteOut]:
    website = require_website_access(website_id, user, db)
    root = Path(website.static_root)
    out: List[PageRouteOut] = []
    for name, rel, url in CURATED:
        exists = (root / rel).is_file()
        out.append(PageRouteOut(label=name, path=rel, url=url, exists=exists, editable=name in ("Home", "Contact")))
    blog_count = sum(1 for _ in (root / "blog").iterdir() if _.is_dir()) if (root / "blog").is_dir() else 0
    out.append(PageRouteOut(label="Blog posts", path="blog/*/index.html", url="/blog", exists=blog_count > 0, editable=False))
    return out
