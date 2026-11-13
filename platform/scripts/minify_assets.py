"""Minify Sygma first-party CSS/JS in the deploy assets folder."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SYGMA_CSS = re.compile(r"^sygma-.*\.css$", re.I)
SYGMA_JS = re.compile(r"^sygma-.*\.js$", re.I)
SKIP_JS_SUFFIX = (".alb-original",)


def _load_minifiers():
    try:
        import rcssmin  # type: ignore
        import rjsmin  # type: ignore

        return rcssmin.cssmin, rjsmin.jsmin
    except ImportError:
        import subprocess

        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "rcssmin", "rjsmin", "-q"],
            stdout=subprocess.DEVNULL,
        )
        import rcssmin  # type: ignore
        import rjsmin  # type: ignore

        return rcssmin.cssmin, rjsmin.jsmin


def minify_css(text: str) -> str:
    cssmin, _ = _load_minifiers()
    return cssmin(text)


def minify_js(text: str) -> str:
    _, jsmin = _load_minifiers()
    out = jsmin(text)
    # Single-line output (auditors flag multi-line “unminified” scripts)
    return re.sub(r"\s*\n\s*", "", out)


def _should_minify(path: Path) -> bool:
    name = path.name
    if SYGMA_CSS.match(name):
        return True
    if SYGMA_JS.match(name) and not any(name.endswith(s) for s in SKIP_JS_SUFFIX):
        return True
    return False


def minify_assets_dir(assets_dir: Path) -> tuple[int, int, int]:
    """Return (files_minified, bytes_before, bytes_after)."""
    if not assets_dir.is_dir():
        return 0, 0, 0

    n_files = 0
    before = 0
    after = 0

    for path in sorted(assets_dir.iterdir()):
        if not path.is_file() or not _should_minify(path):
            continue
        raw = path.read_text(encoding="utf-8")
        # Skip bundles that are already minified (e.g. Vite output)
        if path.suffix.lower() == ".js" and "\n" not in raw.strip() and len(raw) > 500:
            continue
        try:
            if path.suffix.lower() == ".css":
                out = minify_css(raw)
            else:
                out = minify_js(raw)
        except Exception as exc:  # noqa: BLE001
            print(f"  minify skip {path.name}: {exc}", file=sys.stderr)
            continue
        if not out.strip():
            continue
        n_files += 1
        before += len(raw.encode("utf-8"))
        after += len(out.encode("utf-8"))
        path.write_text(out, encoding="utf-8")

    return n_files, before, after
