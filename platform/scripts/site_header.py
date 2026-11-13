"""Homepage-matching header + mobile drawer for static Sygma pages."""

from __future__ import annotations

import html


def _prefix(depth: int) -> str:
    return "../" * depth if depth > 0 else ""


def _nav_cls(active: str | None, match: str) -> str:
    return "hd-k is-on" if active == match else "hd-k"


def render_site_header_block(depth: int = 1, active: str | None = None) -> str:
    """Header, mobile menu, and scrim — same structure as patched marketing pages."""
    p = _prefix(depth)
    root = p if depth > 0 else "/"
    logo = f"{p}brand/alb-logo-ink.png?v=2026111306"
    esc_root = html.escape(root, quote=True)
    esc_logo = html.escape(logo, quote=True)

    header = f"""<header class="hd hd--minimal" id="top"><div class="hd-in"><nav class="hd-l" aria-label="Main"><button type="button" class="hd-burger" aria-label="Open menu" aria-expanded="false" aria-controls="hd-mob"><i></i><i></i><span class="hd-burger-t" aria-hidden="true">Menu</span></button><a href="{p}services/" class="{_nav_cls(active, 'services')}">Services</a><a href="{p}portfolio/" class="{_nav_cls(active, 'portfolio')}">Portfolio</a><a href="{p}pricing/" class="{_nav_cls(active, 'pricing')}">Pricing</a></nav><a aria-label="Sygma Media, home" href="{esc_root}" class="hd-logo"><img src="{esc_logo}" alt="Sygma Media - Growth Partner for US Aesthetic &amp; Medical Clinics" width="170" height="48" fetchPriority="high" decoding="async"/></a><nav class="hd-r" aria-label="More"><a href="{esc_root}" class="{_nav_cls(active, 'home')}">Home</a><a href="{p}about/" class="{_nav_cls(active, 'about')}">About</a><a href="{p}contact/" class="hd-cta">Contact</a></nav></div></header>"""

    mob = (
        f'<div id="hd-mob" class="hd-mob" role="dialog" aria-label="Menu" inert="">'
        f'<div class="hd-mob-in"><nav aria-label="Menu"><ol class="hd-mob-list hd-mob-list--minimal">'
        f'<li><a href="{p}services/" class="hd-mob-k">Services</a></li>'
        f'<li><a href="{p}portfolio/" class="hd-mob-k">Portfolio</a></li>'
        f'<li><a href="{p}pricing/" class="hd-mob-k">Pricing</a></li>'
        f'<li><a href="{esc_root}" class="hd-mob-k">Home</a></li>'
        f'<li><a href="{p}about/" class="hd-mob-k">About</a></li>'
        f'<li><a href="{p}contact/" class="hd-mob-k hd-mob-cta">Contact</a></li>'
        f"</ol></nav></div></div>"
    )
    scrim = '<div class="hd-scrim" aria-hidden="true"></div>'
    return header + mob + scrim


SYGMA_CRITICAL = """    <style id="sygma-critical">
      .hd-pan,.hd-scrim{position:fixed!important;left:0!important;right:0!important;top:0!important;z-index:110!important;visibility:hidden!important;pointer-events:none!important;clip-path:inset(0 0 100% 0)!important;max-height:0!important;overflow:hidden!important}
      @media (max-width:1279.98px){
        .hd-pan,.hd-scrim{display:none!important}
        .hd:not(.hd--minimal) .hd-l .hd-k,.hd:not(.hd--minimal) .hd-r .hd-k,.hd:not(.hd--minimal) .hd-cta{display:none!important}
        .hd-burger{display:block!important}
      }
      @media (min-width:1280px){
        .hd-pan,.hd-scrim{display:block!important;max-height:none!important;overflow:visible!important}
        .hd-burger{display:none!important}
        .hd-l .hd-k,.hd-r .hd-k{display:inline-flex!important}
      }
    </style>"""

MINIMAL_NAV_OVERRIDE = """    <style id="sygma-minimal-nav-override">
      @media (min-width:1280px){
        .hd.hd--minimal .hd-l .hd-k,.hd.hd--minimal .hd-r .hd-k,.hd.hd--minimal .hd-cta{display:inline-flex!important;align-items:center}
        .hd.hd--minimal .hd-burger{display:none!important}
      }
      @media (max-width:1279.98px){
        .hd.hd--minimal .hd-l .hd-k,.hd.hd--minimal .hd-r .hd-k,.hd.hd--minimal .hd-cta{display:none!important}
        .hd.hd--minimal .hd-burger{display:block!important}
      }
    </style>
"""


def render_static_head_extras(depth: int = 1) -> str:
    p = _prefix(depth)
    return (
        f"{SYGMA_CRITICAL}\n"
        f"{MINIMAL_NAV_OVERRIDE}\n"
        f'    <script src="{p}assets/sygma-hd-guard.js"></script>\n'
        f'    <script src="{p}assets/sygma-hd-scroll.js" defer></script>\n'
        f'    <script src="{p}assets/sygma-hd-mob.js" defer></script>\n'
    )
