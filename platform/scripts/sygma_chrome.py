"""Shared header/footer loaders for static page generators."""

from __future__ import annotations

import importlib.util
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent


def _load_module(name: str, filename: str):
    path = _SCRIPTS / filename
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def site_footer(depth: int = 1) -> str:
    return _load_module("site_footer", "site_footer.py").render_site_footer(depth)


def site_header_block(depth: int = 1, active: str | None = None) -> str:
    return _load_module("site_header", "site_header.py").render_site_header_block(
        depth, active
    )


def static_head_extras(depth: int = 1) -> str:
    return _load_module("site_header", "site_header.py").render_static_head_extras(depth)
