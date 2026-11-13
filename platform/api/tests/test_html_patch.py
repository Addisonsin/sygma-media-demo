from pathlib import Path

from app.services.html_patch import apply_manifest_to_build, patch_homepage_index


def test_patch_homepage_h1(tmp_path: Path):
    html = """<html><head><title>Old</title>
    <meta name="description" content="Old desc" />
    </head><body><h1 id="h1" class="ap-h1"><span class="ap-l1">Line A</span> <span class="ap-l2"><em>Line B.</em></span></h1></body></html>"""
    p = tmp_path / "index.html"
    p.write_text(html, encoding="utf-8")
    patch_homepage_index(
        p,
        {
            "hero": {
                "line1": "New One",
                "line2_emphasis": "New Two",
                "meta_title": "New Title",
                "meta_description": "New description",
            }
        },
    )
    out = p.read_text(encoding="utf-8")
    assert "New One" in out and "New Two" in out
    assert "<title>New Title</title>" in out
    assert 'content="New description"' in out


def test_apply_manifest(tmp_path: Path):
    (tmp_path / "index.html").write_text(
        '<span class="ap-l1">A</span> <span class="ap-l2"><em>B</em></span>',
        encoding="utf-8",
    )
    (tmp_path / "contact").mkdir()
    (tmp_path / "contact" / "index.html").write_text('{"telephone":"+12125550147"}', encoding="utf-8")
    report = apply_manifest_to_build(
        tmp_path,
        {
            "documents": {
                "homepage:default": {"hero": {"line1": "X", "line2_emphasis": "Y"}},
                "site_settings:default": {"phone_e164": "+19998887777"},
            }
        },
    )
    assert "index.html" in report["patched"]
