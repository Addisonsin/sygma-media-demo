#!/usr/bin/env python3
"""Read-only content inventory for web-clones/01-sygma-media (Phase 1)."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2] / "web-clones" / "01-sygma-media"


def count_html_routes(site: Path) -> int:
    return sum(1 for p in site.rglob("index.html") if p.is_file())


def blog_slugs(site: Path) -> list[str]:
    blog = site / "blog"
    if not blog.is_dir():
        return []
    return sorted(d.name for d in blog.iterdir() if d.is_dir())


def extract_title(html: str) -> str | None:
    m = re.search(r"<title[^>]*>([^<]+)</title>", html, re.I)
    return m.group(1).strip() if m else None


def extract_meta_description(html: str) -> str | None:
    m = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)',
        html,
        re.I,
    )
    return m.group(1).strip() if m else None


def extract_json_ld(html: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(
        r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
        html,
        re.I | re.S,
    ):
        try:
            out.append(json.loads(m.group(1)))
        except json.JSONDecodeError:
            pass
    return out


def image_refs(site: Path) -> dict[str, int]:
    counts: dict[str, int] = {}
    for p in site.rglob("*.html"):
        text = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(r'(?:src|href)=["\'](/(?:img|brand|m)/[^"\']+)', text):
            key = m.group(1).split("?")[0]
            counts[key] = counts.get(key, 0) + 1
    return dict(sorted(counts.items(), key=lambda x: -x[1])[:50])


def main() -> int:
    if not ROOT.is_dir():
        print(f"Site root not found: {ROOT}", file=sys.stderr)
        return 1

    home = ROOT / "index.html"
    home_html = home.read_text(encoding="utf-8", errors="replace") if home.is_file() else ""

    report = {
        "site_root": str(ROOT),
        "html_route_count": count_html_routes(ROOT),
        "blog_post_folder_count": len(blog_slugs(ROOT)),
        "homepage": {
            "title": extract_title(home_html),
            "meta_description": extract_meta_description(home_html),
            "json_ld_types": [
                d.get("@type") for d in extract_json_ld(home_html) if isinstance(d, dict)
            ],
        },
        "sample_routes": [
            "index.html",
            "about/index.html",
            "contact/index.html",
            "pricing/index.html",
            "services/index.html",
            "blog/index.html",
        ],
        "top_image_refs": image_refs(ROOT),
        "notes": [
            "Body copy also lives in assets/index-*.js; migrate via structured docs, not JS patches.",
            "tRPC /api/trpc absent on static host — platform API is new.",
        ],
    }

    out_path = Path(__file__).resolve().parents[1] / ".." / "docs" / "platform" / "CONTENT-INVENTORY-SYGMA.json"
    out_path = out_path.resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"\nWrote {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
