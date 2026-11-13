"""Apply published CMS documents to static HTML (design-preserving text swaps)."""
from __future__ import annotations

import html as html_lib
import json
import re
from pathlib import Path


def _esc(text: str) -> str:
    return html_lib.escape(text, quote=False)


def patch_homepage_index(path: Path, homepage: dict, seo: dict | None = None) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8", errors="replace")
    original = content
    hero = homepage.get("hero") or {}

    line1 = hero.get("line1") or hero.get("heading_line1")
    line2 = hero.get("line2_emphasis") or hero.get("line2")
    if line1:
        content = re.sub(
            r'(<span class="ap-l1">)(.*?)(</span>)',
            lambda m: f"{m.group(1)}{_esc(str(line1))}{m.group(3)}",
            content,
            count=1,
        )
    if line2:
        content = re.sub(
            r'(<span class="ap-l2"><em>)(.*?)(</em></span>)',
            lambda m: f"{m.group(1)}{_esc(str(line2))}{m.group(3)}",
            content,
            count=1,
        )

    meta_title = (seo or {}).get("title") or hero.get("meta_title")
    meta_desc = (seo or {}).get("meta_description") or hero.get("meta_description")
    if meta_title:
        content = re.sub(
            r"<title>[^<]*</title>",
            f"<title>{_esc(str(meta_title))}</title>",
            content,
            count=1,
        )
    if meta_desc:
        content = re.sub(
            r'(<meta[^>]+name=["\']description["\'][^>]+content=["\'])([^"\']*)(["\'])',
            lambda m: f"{m.group(1)}{_esc(str(meta_desc))}{m.group(3)}",
            content,
            count=1,
            flags=re.I,
        )

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def patch_contact_page(path: Path, settings_doc: dict) -> bool:
    if not path.is_file():
        return False
    content = path.read_text(encoding="utf-8", errors="replace")
    original = content
    phone_e164 = settings_doc.get("phone_e164")
    email = settings_doc.get("email")
    whatsapp = settings_doc.get("whatsapp_e164")

    if phone_e164:
        content = content.replace('"telephone":"+12125550147"', f'"telephone":"{phone_e164}"')
        content = re.sub(
            r'href="tel:\+?[0-9]+"',
            f'href="tel:{phone_e164.lstrip("+")}"',
            content,
            count=0,
        )
    if email:
        content = re.sub(
            r'"email":"[^"]+@sygmamedia\.com"',
            f'"email":"{email}"',
            content,
            count=1,
        )
    if whatsapp:
        digits = re.sub(r"\D", "", str(whatsapp))
        content = re.sub(r"https://wa\.me/[0-9]+", f"https://wa.me/{digits}", content)

    if content != original:
        path.write_text(content, encoding="utf-8")
        return True
    return False


def apply_manifest_to_build(build_root: Path, manifest: dict) -> dict:
    """Return summary of patched files."""
    docs = manifest.get("documents") or {}
    homepage = docs.get("homepage:default") or {}
    seo = docs.get("seo:home") or docs.get("seo:default")
    settings = docs.get("site_settings:default") or {}

    report = {"patched": []}
    index = build_root / "index.html"
    if patch_homepage_index(index, homepage, seo):
        report["patched"].append("index.html")

    contact = build_root / "contact" / "index.html"
    if settings and patch_contact_page(contact, settings):
        report["patched"].append("contact/index.html")

    report_path = build_root / "_cms_patch_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report
