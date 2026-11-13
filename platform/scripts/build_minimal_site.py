#!/usr/bin/env python3
"""Build minimal agency site into web-clones/sygma-minimal (does not modify 01-sygma-media)."""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "web-clones" / "01-sygma-media"
DEST = ROOT / "web-clones" / "sygma-minimal"

# Core marketing routes (directories with index.html)
ROUTE_DIRS = [
    "about",
    "contact",
    "services",
    "pricing",
    "faq",
    "privacy-policy",
    "terms-of-service",
]

# Homepage + /case-studies hub links (SPA detail routes → static shells)
CASE_STUDY_SLUGS = [
    "manhattan-dermatology",
    "miami-luxe-medspa",
    "dallas-integrative-skin",
    "beverly-hills-surgical",
    "scottsdale-wellness",
    "austin-medspa-collective",
    "chicago-facial-institute",
]

# Old React case-study slugs → static portfolio slugs
LEGACY_CASE_STUDY_TO_PORTFOLIO = {
    "the-hampton-clinic": "manhattan-dermatology",
    "halcyon-medispa": "miami-luxe-medspa",
    "dr-harry-clinic": "beverly-hills-surgical",
    "mesglo-london": "scottsdale-wellness",
    "luxe-skin-glasgow": "austin-medspa-collective",
    "facial-sculpting": "chicago-facial-institute",
    "aesthetic-doctors-australia": "dallas-integrative-skin",
}

ASSET_DIRS = ["assets", "brand", "img", "m", "fonts"]

ROOT_FILES = [
    "index.html",
    "404.html",
    "_headers",
    "favicon.ico",
    "favicon-16.png",
    "favicon-32.png",
    "favicon-96.png",
    "apple-touch-icon.png",
    "icon-192.png",
    "icon-512.png",
    "site.webmanifest",
]

NAV_REPLACEMENTS = [
    ("/aesthetic-clinic-seo", "/services/"),
    ("/plastic-surgery-seo", "/services/"),
    ("/guides", "/services/"),
    ('href="/admin"', 'href="/contact"'),
]

# Cloudflare Pages serves directory indexes — prefer trailing slashes (avoid 308).
TOOL_LINK_REPLACEMENTS = (
    ("/tools/clinic-launch-calculator", "/services/"),
    ("/tools/digital-readiness-checklist", "/services/"),
)

CANONICAL_DIR_ROUTES = (
    "services",
    "pricing",
    "about",
    "contact",
    "faq",
    "privacy-policy",
    "terms-of-service",
)

RE_FOOTER = re.compile(r"<footer class=\"ft(?: ft--minimal)?\">.*?</footer>", re.DOTALL)
RE_FT_BRAND = re.compile(r"<div class=\"ft-brand\">.*?</div>\s*(?=<nav class=\"ft-cols\")", re.DOTALL)
RE_FT_BAR = re.compile(r"<div class=\"ft-bar\">.*?</div>\s*(?=</div>\s*</footer>)", re.DOTALL)
RE_HEADER = re.compile(r'<header class="hd[^"]*"[^>]*>.*?</header>', re.DOTALL)
RE_LOGO = re.compile(r'<a[^>]*class="hd-logo"[^>]*>.*?</a>', re.DOTALL)

MINIMAL_FT_NAV = """<nav class="ft-cols" aria-label="Footer"><div class="ft-col"><div class="ft-h">Explore</div><a href="/services/">Services</a><a href="/pricing/">Pricing</a><a href="/portfolio/">Portfolio</a></div><div class="ft-col"><div class="ft-h">Company</div><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/faq/">FAQ</a></div></nav>"""

MINIMAL_FT_CONTACT = (
    '<div class="ft-contact"><div class="ft-h">Contact</div>'
    '<a class="ft-contact-link" href="tel:+12125550147">+1 (212) 555-0147</a>'
    '<a class="ft-contact-link" href="mailto:exec@sygmamedia.com">exec@sygmamedia.com</a>'
    '<p class="ft-loc">New York, NY · United States</p>'
    '<div class="ft-social">'
    '<a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer">Instagram</a>'
    '<a href="https://www.linkedin.com/company/sygmamedia" target="_blank" rel="noopener noreferrer">LinkedIn</a>'
    "</div></div>"
)

RE_FT_LOGO = re.compile(r'<a[^>]*class="ft-logo"[^>]*>.*?</a>', re.DOTALL)

MINIMAL_HD_MOB = (
    '<div id="hd-mob" class="hd-mob" role="dialog" aria-label="Menu" inert="">'
    '<div class="hd-mob-in"><nav aria-label="Menu"><ol class="hd-mob-list hd-mob-list--minimal">'
    '<li><a href="/services/" class="hd-mob-k">Services</a></li>'
    '<li><a href="/portfolio/" class="hd-mob-k">Portfolio</a></li>'
    '<li><a href="/pricing/" class="hd-mob-k">Pricing</a></li>'
    '<li><a href="/" class="hd-mob-k">Home</a></li>'
    '<li><a href="/about/" class="hd-mob-k">About</a></li>'
    '<li><a href="/contact" class="hd-mob-k hd-mob-cta">Contact</a></li>'
    "</ol></nav></div></div>"
)

MINIMAL_CSS = """/* Generated — minimal agency layout (header, footer, nav) */
/* Static pages do not load the SPA bundle — match its border-box reset */
*, *::before, *::after { box-sizing: border-box; }
html, body { margin: 0; padding: 0; max-width: 100%; }
img, svg, video { max-width: 100%; }

:root {
  --brand-olive-gradient: linear-gradient(165deg, #222e1f 0%, #2b3827 54%, #2f3d2b 100%);
  --brand-olive-gradient-hover: linear-gradient(165deg, #2b3827 0%, #354833 50%, #3d4a38 100%);
  --brand-olive-deep: #222e1f;
  --g: clamp(1.15rem, 4.4vw, 4.5rem);
  --rule: rgba(26, 33, 28, 0.07);
}

/* --- Header: ALB-width grid, centered logo --- */
html:has(.hd--minimal) {
  --hd-h: 84px;
}

header.hd.hd--minimal {
  --hd-minimal-pad-y: 0;
}

header.hd.hd--minimal,
header.pf-hd.hd.hd--minimal {
  position: fixed !important;
  inset: 0 0 auto 0 !important;
  left: 0 !important;
  right: 0 !important;
  width: 100% !important;
  z-index: 120 !important;
  transition: background-color 0.6s ease, box-shadow 0.6s ease !important;
  background: transparent !important;
  border-bottom: none !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
  overflow: visible !important;
}

header.hd.hd--minimal.is-sm,
header.hd.hd--minimal.is-pan,
header.hd.hd--minimal.is-mob,
header.pf-hd.hd.hd--minimal.is-sm {
  background: color-mix(in oklab, var(--ivory) 93%, transparent) !important;
  backdrop-filter: blur(18px) saturate(1.4) !important;
  -webkit-backdrop-filter: blur(18px) saturate(1.4) !important;
  border-bottom: 1px solid var(--rule) !important;
  box-shadow: 0 1px 0 var(--rule) !important;
}

/* Match home / services: transparent bar until scroll (sygma-hd-scroll.js sets .is-sm) */
.hm:not(.sygma-static-shell) .hd.hd--minimal:not(.is-sm):not(.is-pan):not(.is-mob),
.hm.sygma-static-shell .hd.hd--minimal:not(.is-sm):not(.is-pan):not(.is-mob) {
  background: transparent !important;
  border-bottom: none !important;
  box-shadow: none !important;
  backdrop-filter: none !important;
  -webkit-backdrop-filter: none !important;
}

.hd.hd--minimal,
.hd.hd--minimal .hd-in,
.ft.ft--minimal,
.ft.ft--minimal .ft-in,
.ft.ft--minimal .ft-shell,
.ft.ft--minimal .ft-top,
.ft.ft--minimal .ft-bar {
  box-sizing: border-box !important;
  max-width: 100% !important;
}

.hd.hd--minimal .hd-in {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) auto minmax(0, 1fr) !important;
  align-items: center !important;
  width: 100% !important;
  max-width: 1640px !important;
  margin-inline: auto !important;
  height: var(--hd-h, 84px) !important;
  min-height: var(--hd-h, 84px) !important;
  max-height: var(--hd-h, 84px) !important;
  padding: 0 var(--g) !important;
  column-gap: 2rem !important;
  row-gap: 0 !important;
  box-sizing: border-box !important;
}

.hd.hd--minimal .hd-l {
  grid-column: 1;
  justify-self: start;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-start !important;
  gap: clamp(0.65rem, 1.35vw, 1.45rem) !important;
  min-width: 0;
}

.hd.hd--minimal .hd-logo {
  grid-column: 2;
  justify-self: center;
  align-self: center;
  line-height: 0;
}

.hd.hd--minimal .hd-logo img,
.hd.hd--minimal .hd-logo svg {
  display: block !important;
  width: clamp(132px, 10.5vw, 168px) !important;
  height: auto !important;
  max-height: 52px !important;
  max-width: min(168px, 42vw) !important;
  object-fit: contain !important;
}

.hd.hd--minimal .hd-r {
  grid-column: 3;
  justify-self: end;
  display: flex !important;
  align-items: center !important;
  justify-content: flex-end !important;
  gap: clamp(0.65rem, 1.35vw, 1.45rem) !important;
  min-width: 0;
}

.hd.hd--minimal .hd-k {
  font-family: var(--font-sans) !important;
  font-size: clamp(0.6rem, 0.64vw, 0.64rem) !important;
  font-weight: 500 !important;
  letter-spacing: 0.2em !important;
  text-transform: uppercase;
  color: var(--charcoal) !important;
  padding: 0.6rem 0 !important;
  line-height: 1 !important;
  text-decoration: none;
  white-space: nowrap;
  transition: color 0.18s ease, opacity 0.18s ease;
}

.hd.hd--minimal .hd-k:hover {
  color: var(--charcoal) !important;
}

.hd.hd--minimal .hd-k.is-on {
  color: var(--sage) !important;
  font-weight: 600 !important;
}

.hd.hd--minimal .hd-car {
  display: none !important;
}

.hd.hd--minimal .hd-cta,
.hd.hd--minimal a.hd-k.hd-cta,
.pf-hd.hd--minimal .hd-cta {
  font-family: var(--font-sans) !important;
  font-size: clamp(0.56rem, 0.62vw, 0.62rem) !important;
  font-weight: 500 !important;
  letter-spacing: 0.22em !important;
  text-transform: uppercase;
  padding: 0.95rem 1.25rem !important;
  border-radius: 0;
  margin-left: clamp(0.35rem, 0.9vw, 0.65rem);
  align-self: center;
  color: var(--ivory) !important;
  text-decoration: none !important;
  background: var(--brand-olive-gradient) !important;
  border: 1px solid rgba(201, 168, 124, 0.42) !important;
  box-shadow: none !important;
}

.hd.hd--minimal .hd-cta:hover,
.pf-hd.hd--minimal .hd-cta:hover {
  color: #ffffff !important;
  background: var(--brand-olive-gradient-hover) !important;
  border-color: rgba(201, 168, 124, 0.62) !important;
}

.hd.hd--minimal .hd-burger-t {
  font-family: var(--font-sans) !important;
  font-size: 0.62rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.16em !important;
}

.hd-mob-list--minimal {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.hd-mob-list--minimal .hd-mob-k {
  display: block;
  font-family: var(--font-sans) !important;
  font-size: 0.82rem !important;
  font-weight: 500 !important;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  padding: 0.85rem 0;
  color: var(--charcoal-soft) !important;
  border-bottom: 1px solid rgba(10, 11, 13, 0.06);
}

.hd-mob-list--minimal .hd-mob-cta {
  margin-top: 0.5rem;
  text-align: center;
  color: var(--ivory) !important;
  background: var(--brand-olive-gradient);
  border-radius: 2px;
  border: 1px solid rgba(201, 168, 124, 0.42);
}

/* Minimal header: full link row on desktop only (mobile uses burger + drawer) */
@media (min-width: 1280px) {
  .hd.hd--minimal .hd-l .hd-k,
  .hd.hd--minimal .hd-r .hd-k,
  .hd.hd--minimal .hd-r .hd-cta,
  .hd.hd--minimal .hd-cta,
  .pf-hd.hd--minimal .hd-l .hd-k,
  .pf-hd.hd--minimal .hd-r .hd-k,
  .pf-hd.hd--minimal .hd-cta {
    display: inline-flex !important;
    align-items: center;
  }

  .hd.hd--minimal .hd-burger,
  .pf-hd.hd--minimal .hd-burger {
    display: none !important;
  }
}

@media (max-width: 1279.98px) {
  .hd.hd--minimal .hd-l .hd-k,
  .hd.hd--minimal .hd-r .hd-k,
  .hd.hd--minimal .hd-cta,
  .pf-hd.hd--minimal .hd-l .hd-k,
  .pf-hd.hd--minimal .hd-r .hd-k,
  .pf-hd.hd--minimal .hd-cta {
    display: none !important;
  }

  .hd.hd--minimal .hd-burger,
  .pf-hd.hd--minimal .hd-burger {
    display: block !important;
  }
}

@media (max-width: 720px) {
  .hd.hd--minimal .hd-in,
  .pf-hd.hd--minimal .hd-in {
    grid-template-columns: 1fr auto 1fr !important;
    column-gap: 0.35rem !important;
    padding-inline: 0.65rem !important;
  }

  .hd.hd--minimal .hd-k,
  .pf-hd.hd--minimal .hd-k {
    font-size: 0.52rem !important;
    letter-spacing: 0.07em !important;
  }

  .hd.hd--minimal .hd-l,
  .pf-hd.hd--minimal .hd-l {
    gap: 0.35rem !important;
  }

  .hd.hd--minimal .hd-r,
  .pf-hd.hd--minimal .hd-r {
    gap: 0.25rem !important;
  }

  .hd.hd--minimal .hd-cta,
  .pf-hd.hd--minimal .hd-cta {
    padding: 0.55rem 0.65rem !important;
    font-size: 0.5rem !important;
    margin-left: 0 !important;
  }

  .hd.hd--minimal .hd-logo img,
  .pf-hd.hd--minimal .hd-logo img {
    width: 5.5rem !important;
  }
}

@media (min-width: 721px) {
  .hd.hd--minimal .hd-l,
  .hd.hd--minimal .hd-r,
  .pf-hd.hd--minimal .hd-l,
  .pf-hd.hd--minimal .hd-r {
    align-self: center;
  }
}

/* --- Dark CTA → footer rhythm --- */
section[style*="deep-forest"] {
  padding-bottom: clamp(4.75rem, 8vw, 6.25rem) !important;
}

/* Static routes — same shell as homepage (.hm > header, main, footer) */
html:has(.sygma-static-shell),
body:has(.sygma-static-shell),
body:has(.ft.ft--minimal) {
  overflow-x: clip !important;
  max-width: 100% !important;
}

.hm.sygma-static-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 100%;
  overflow-x: clip;
  background: var(--ivory, #f7f3eb);
}

/* Fixed header (same as services bundle) — offset content except full-bleed portfolio hero */
.hm.sygma-static-shell:not(:has(.pf-hero)) {
  padding-top: var(--hd-h, 84px);
}

.hm.sygma-static-shell > main,
.hm.sygma-static-shell > .pf-main {
  flex: 1 0 auto;
  width: 100%;
  max-width: 100%;
}

/* Static pages: mobile drawer (SPA bundle normally supplies these rules) */
.hm.sygma-static-shell .hd-mob {
  position: fixed !important;
  inset: 0 !important;
  z-index: 115 !important;
  overflow-y: auto;
  overscroll-behavior: contain;
  background: var(--ivory, #f7f3eb);
  padding: calc(var(--hd-h, 84px) + 1rem) clamp(1.25rem, 4vw, 2.5rem)
    calc(2.5rem + env(safe-area-inset-bottom, 0px));
  clip-path: inset(0 0 100% 0) !important;
  visibility: hidden !important;
  pointer-events: none !important;
  transition: clip-path 0.75s ease, visibility 0s linear 0.75s;
}

.hm.sygma-static-shell .hd-mob.is-on {
  clip-path: inset(0) !important;
  visibility: visible !important;
  pointer-events: auto !important;
  transition: clip-path 0.8s ease, visibility 0s;
}

.hm.sygma-static-shell > .hd-scrim:not(.is-on) {
  pointer-events: none !important;
  visibility: hidden !important;
}

.hm.sygma-static-shell > footer.ft.ft--minimal {
  flex-shrink: 0;
  width: 100% !important;
  max-width: none !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
}

/* --- Footer (full-bleed band, content aligned to site grid) --- */
.ft.ft--minimal {
  background: linear-gradient(165deg, #222e1f 0%, #2b3827 54%, #2f3d2b 100%) !important;
  position: relative;
  box-sizing: border-box !important;
  width: 100% !important;
  max-width: 100% !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
  padding: clamp(2.75rem, 5vw, 4rem) 0 clamp(1.75rem, 3vw, 2.25rem) !important;
  border-top: 1px solid rgba(247, 243, 235, 0.07);
}

.hm > .ft.ft--minimal,
.hm.sygma-static-shell > .ft.ft--minimal {
  width: 100% !important;
  max-width: none !important;
  margin-left: 0 !important;
  margin-right: 0 !important;
}

.ft.ft--minimal .ft-in {
  max-width: 1640px !important;
  width: 100% !important;
  margin-inline: auto !important;
  padding: 0 var(--g) !important;
  box-sizing: border-box !important;
}

.ft.ft--minimal .ft-shell {
  border: none !important;
  border-radius: 0 !important;
  background: transparent !important;
  box-shadow: none !important;
  padding: 0 !important;
  max-width: none !important;
}

.ft.ft--minimal .ft-top {
  display: grid !important;
  grid-template-columns: minmax(0, 1.2fr) minmax(0, 1fr) minmax(0, 1fr) !important;
  align-items: start !important;
  gap: clamp(2rem, 5vw, 4rem) !important;
  padding-bottom: clamp(1.75rem, 3vw, 2.35rem) !important;
  border-bottom: 1px solid rgba(247, 243, 235, 0.08) !important;
}

.ft.ft--minimal .ft-brand {
  max-width: 22rem;
}

.ft.ft--minimal .ft-logo img {
  width: clamp(7rem, 16vw, 8.75rem) !important;
  height: auto !important;
  opacity: 0.96;
}

.ft.ft--minimal .ft-tag {
  font-family: var(--font-display) !important;
  font-size: clamp(1.02rem, 1.2vw, 1.18rem) !important;
  font-weight: 400 !important;
  font-style: italic;
  line-height: 1.42 !important;
  color: rgba(213, 203, 184, 0.72) !important;
  margin: 1rem 0 0 !important;
  max-width: 28ch;
}

.ft.ft--minimal .ft-blurb,
.ft.ft--minimal .ft-nap {
  display: none !important;
}

.ft.ft--minimal .ft-cols {
  display: grid !important;
  grid-template-columns: repeat(2, minmax(6.5rem, 1fr)) !important;
  gap: clamp(1.25rem, 3vw, 2.5rem) !important;
  margin: 0 !important;
  align-self: center !important;
}

.ft.ft--minimal .ft-h {
  font-family: var(--font-sans) !important;
  font-size: 0.58rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.22em !important;
  text-transform: uppercase;
  color: rgba(200, 212, 188, 0.75) !important;
  margin: 0 0 0.9rem !important;
}

.ft.ft--minimal .ft-cols a {
  display: block !important;
  padding: 0.28rem 0 !important;
  font-size: 0.9rem !important;
  font-weight: 500 !important;
  color: rgba(247, 243, 235, 0.9) !important;
  text-decoration: none !important;
  transition: color 0.16s ease, padding-left 0.16s ease;
}

.ft.ft--minimal .ft-cols a:hover {
  color: var(--ivory) !important;
  padding-left: 0.35rem !important;
}

.ft.ft--minimal .ft-contact {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
  padding-left: clamp(1rem, 2.5vw, 2rem);
  border-left: 1px solid rgba(247, 243, 235, 0.1);
  align-self: stretch;
  justify-content: center;
}

.ft.ft--minimal .ft-contact-link {
  font-family: var(--font-sans) !important;
  font-size: 0.88rem !important;
  font-weight: 500 !important;
  color: rgba(247, 243, 235, 0.92) !important;
  text-decoration: none !important;
  transition: color 0.16s ease;
}

.ft.ft--minimal .ft-contact-link:hover {
  color: var(--ivory) !important;
}

.ft.ft--minimal .ft-loc {
  margin: 0.35rem 0 0.25rem !important;
  font-size: 0.76rem !important;
  line-height: 1.5 !important;
  color: rgba(247, 243, 235, 0.48) !important;
}

.ft.ft--minimal .ft-social {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 0.5rem !important;
  margin-top: 0.65rem !important;
}

.ft.ft--minimal .ft-social a {
  display: inline-flex !important;
  align-items: center !important;
  padding: 0.42rem 0.7rem !important;
  border: 1px solid rgba(247, 243, 235, 0.14) !important;
  border-radius: 2px !important;
  font-size: 0.58rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.14em !important;
  text-transform: uppercase;
  color: rgba(247, 243, 235, 0.72) !important;
  text-decoration: none !important;
  background: rgba(0, 0, 0, 0.12);
  transition: border-color 0.16s ease, background 0.16s ease, color 0.16s ease;
}

.ft.ft--minimal .ft-social a:hover {
  color: var(--ivory) !important;
  border-color: rgba(201, 168, 124, 0.45) !important;
  background: rgba(247, 243, 235, 0.06) !important;
}

.ft.ft--minimal .ft-bar {
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  justify-content: space-between !important;
  gap: 0.75rem 1.5rem !important;
  padding: 1.35rem 0 0.25rem !important;
  border-top: none !important;
}

.ft.ft--minimal .ft-bar p {
  margin: 0 !important;
  font-size: 0.74rem !important;
  color: rgba(247, 243, 235, 0.45) !important;
}

.ft.ft--minimal .ft-legal {
  display: flex !important;
  flex-wrap: wrap !important;
  gap: 0.3rem 1.1rem !important;
}

.ft.ft--minimal .ft-legal a {
  font-size: 0.74rem !important;
  color: rgba(247, 243, 235, 0.55) !important;
  text-decoration: none !important;
}

.ft.ft--minimal .ft-legal a:hover {
  color: var(--ivory) !important;
}

@media (max-width: 920px) {
  .ft.ft--minimal .ft-top {
    grid-template-columns: 1fr 1fr !important;
  }

  .ft.ft--minimal .ft-brand {
    grid-column: 1 / -1;
    max-width: none;
  }

  .ft.ft--minimal .ft-tag {
    max-width: 34ch;
  }

  .ft.ft--minimal .ft-contact {
    grid-column: 1 / -1;
    border-left: none;
    border-top: 1px solid rgba(247, 243, 235, 0.08);
    padding: 1.35rem 0 0;
    margin-top: 0.25rem;
  }
}

@media (max-width: 520px) {
  .ft.ft--minimal .ft-top {
    grid-template-columns: 1fr !important;
  }

  .ft.ft--minimal .ft-cols {
    grid-template-columns: 1fr 1fr !important;
  }
}

#hd-pan-svc,
#hd-pan-loc,
#hd-pan-gd,
.hd-pan-svc,
.hd-pan-loc,
.hd-pan-gd {
  display: none !important;
  visibility: hidden !important;
  pointer-events: none !important;
}

/* Dark-band: paragraph links stay inline (avoid FAQ CTA rules on /blog in copy) */
section[style*="deep-forest"] .container p a {
  background: transparent !important;
  color: rgba(232, 240, 230, 0.95) !important;
  border: none !important;
  box-shadow: none !important;
  padding: 0 !important;
  font-size: inherit !important;
  font-weight: inherit !important;
  letter-spacing: inherit !important;
  text-transform: none !important;
  border-radius: 0 !important;
  display: inline !important;
  text-decoration: underline !important;
  text-underline-offset: 3px;
  transform: none !important;
}

section[style*="deep-forest"] .container p a:hover {
  color: #ffffff !important;
}

/* CTA row only (flex button group), not mid-paragraph links */
section[style*="deep-forest"] .container div[style*="flex"] > a[href="/blog"],
section[style*="deep-forest"] .container div[style*="flex"] > a[href="/guides"],
section[style*="deep-forest"] .container div[style*="flex"] > a[href="/contact"],
section[style*="deep-forest"] .container div[style*="flex"] > a[style*="background:var(--sage)"],
section[style*="deep-forest"] .container div[style*="flex"] > a.sygma-faq-cta--primary {
  background: #f7f3eb !important;
  color: #141a17 !important;
  border: 1px solid rgba(247, 243, 235, 0.35) !important;
  font-size: 0.8125rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.11em !important;
  padding: 0.95rem 2.35rem !important;
  border-radius: 2px;
  box-shadow: 0 10px 28px rgba(0, 0, 0, 0.22);
  opacity: 1 !important;
  text-decoration: none !important;
  transition: background 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease !important;
}

section[style*="deep-forest"] .container div[style*="flex"] > a[href="/blog"]:hover,
section[style*="deep-forest"] .container div[style*="flex"] > a[href="/contact"]:hover,
section[style*="deep-forest"] .container div[style*="flex"] > a.sygma-faq-cta--primary:hover {
  background: #ffffff !important;
  color: #0d110e !important;
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.28);
  transform: translateY(-1px);
}

section[style*="deep-forest"] .container div[style*="flex"] > a[href^="mailto:"],
section[style*="deep-forest"] .container div[style*="flex"] > a[href="/services"][style*="transparent"],
section[style*="deep-forest"] .container div[style*="flex"] > a.sygma-faq-cta--ghost {
  background: rgba(0, 0, 0, 0.15) !important;
  color: #f7f3eb !important;
  border: 1px solid rgba(247, 243, 235, 0.52) !important;
  font-size: 0.8125rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.11em !important;
  padding: 0.95rem 2.35rem !important;
  border-radius: 2px;
  text-decoration: none !important;
  transition: background 0.2s ease, border-color 0.2s ease !important;
}

section[style*="deep-forest"] .container div[style*="flex"] > a[href^="mailto:"]:hover,
section[style*="deep-forest"] .container div[style*="flex"] > a.sygma-faq-cta--ghost:hover {
  background: rgba(247, 243, 235, 0.1) !important;
  border-color: rgba(201, 168, 124, 0.7) !important;
  color: #ffffff !important;
}

/* Pricing: dark charcoal bands — force light type (theme sets display-heading to black) */
.pr-cta .display-heading,
.pr-cta .pr-cta-h,
.pr-cta h2 {
  color: var(--ivory, #f7f3eb) !important;
}

.pr-cta .section-eyebrow {
  color: rgba(247, 243, 235, 0.72) !important;
}

.pr-cta p {
  color: rgba(247, 243, 235, 0.85) !important;
}

.pr-cta .pr-cta-call {
  color: var(--ivory, #f7f3eb) !important;
  border-bottom-color: rgba(200, 212, 188, 0.55) !important;
}

.pr-billing .display-heading,
.pr-billing h2,
.pr-billing h3,
.pr-billing .section-eyebrow {
  color: var(--ivory, #f7f3eb) !important;
}

.pr-billing p,
.pr-billing li {
  color: rgba(247, 243, 235, 0.82) !important;
}

/* --- Services hub: service cards --- */
.sygma-svc-grid {
  display: grid !important;
  gap: clamp(1.15rem, 2.2vw, 1.75rem) !important;
}

.sygma-svc-card {
  display: flex !important;
  flex-direction: column !important;
  min-height: 100% !important;
  padding: clamp(1.55rem, 2.4vw, 2.1rem) clamp(1.4rem, 2vw, 1.9rem) !important;
  text-decoration: none !important;
  background: linear-gradient(168deg, #ffffff 0%, #f8f4ec 55%, #f1e9dd 100%) !important;
  border: 1px solid rgba(63, 83, 72, 0.11) !important;
  border-radius: 3px !important;
  box-shadow:
    0 1px 0 rgba(255, 255, 255, 0.85) inset,
    0 16px 44px rgba(26, 33, 28, 0.07) !important;
  transition:
    transform 0.22s ease,
    box-shadow 0.22s ease,
    border-color 0.22s ease !important;
  position: relative !important;
  overflow: hidden !important;
}

.sygma-svc-card::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background: linear-gradient(180deg, #6d8778 0%, #3f5348 100%);
}

.sygma-svc-card::after {
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(120% 80% at 100% 0%, rgba(201, 168, 124, 0.08), transparent 55%);
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.22s ease;
}

.sygma-svc-card:hover {
  transform: translateY(-5px) !important;
  border-color: rgba(95, 117, 104, 0.22) !important;
  box-shadow:
    0 22px 56px rgba(26, 33, 28, 0.11),
    0 0 0 1px rgba(95, 117, 104, 0.14) !important;
}

.sygma-svc-card:hover::after {
  opacity: 1;
}

.sygma-svc-card h3 {
  font-family: var(--font-display) !important;
  font-size: clamp(1.22rem, 1.4vw, 1.48rem) !important;
  font-weight: 400 !important;
  line-height: 1.18 !important;
  letter-spacing: -0.022em !important;
  color: var(--charcoal) !important;
  margin: 0 0 0.9rem !important;
  padding-left: 0.65rem;
  position: relative;
  z-index: 1;
}

.sygma-svc-card p {
  font-family: var(--font-sans) !important;
  font-size: clamp(0.9rem, 0.98vw, 0.98rem) !important;
  font-weight: 400 !important;
  line-height: 1.74 !important;
  color: #454540 !important;
  margin: 0 0 1.35rem !important;
  flex: 1 1 auto;
  padding-left: 0.65rem;
  position: relative;
  z-index: 1;
}

.sygma-svc-card > span {
  font-family: var(--font-sans) !important;
  font-size: 0.67rem !important;
  font-weight: 600 !important;
  letter-spacing: 0.16em !important;
  text-transform: uppercase;
  color: var(--sage) !important;
  padding-left: 0.65rem;
  margin-top: auto;
  position: relative;
  z-index: 1;
  transition: color 0.18s ease, letter-spacing 0.18s ease;
}

.sygma-svc-card:hover > span {
  color: var(--charcoal) !important;
  letter-spacing: 0.18em;
}

/* --- Brand CTA #2b3827 (wins over bundle var(--charcoal) fills) --- */
:root {
  --brand-olive-solid: #2b3827;
}

html body a.hd-cta,
html body .hd-cta,
html body .btn-primary,
html body a.btn-primary,
html body button.btn-primary,
html body .sticky-cta__primary,
html body .ap-cta .btn-primary,
html body .ap-cta a.btn-primary,
html body .hd-mob-cta,
html body .hd-mob .hd-mob-cta,
html body .hd-mob-list--minimal .hd-mob-cta,
html body .btn-sage,
html body .cta-button,
html body .btn-cta-solid,
html body .eq-foot .btn-primary,
html body .pr-btn:not(.pr-btn--ghost) {
  --charcoal: #2b3827 !important;
  --charcoal-mid: #354833 !important;
  background-color: #2b3827 !important;
  background-image: var(--brand-olive-gradient) !important;
  border-color: rgba(201, 168, 124, 0.45) !important;
  color: #f7f3eb !important;
}

html body a.hd-cta:hover,
html body .hd-cta:hover,
html body .btn-primary:hover,
html body .sticky-cta__primary:hover,
html body .hd-mob-cta:hover,
html body .pr-btn:not(.pr-btn--ghost):hover {
  background-color: #354833 !important;
  background-image: var(--brand-olive-gradient-hover) !important;
  border-color: rgba(201, 168, 124, 0.62) !important;
  color: #fff !important;
}

html body .btn-primary:before,
html body .btn-outline:before,
html body .btn-sage:before {
  background: #354833 !important;
}

html body .btn-outline,
html body .btn-outline:not(:hover),
html body .sticky-cta__wa {
  --charcoal: #2b3827 !important;
  border-color: #2b3827 !important;
  color: #2b3827 !important;
  background: transparent !important;
}

html body .btn-outline:hover {
  background-color: #2b3827 !important;
  background-image: none !important;
  border-color: #2b3827 !important;
  color: #f7f3eb !important;
}

html body .sticky-cta__wa svg {
  color: #2b3827 !important;
  fill: currentColor !important;
}
"""


def _nav_cls(slug: str, match: str) -> str:
    active = slug == match or (match == "home" and slug in ("", ".", "home"))
    return "hd-k is-on" if active else "hd-k"


def minimal_header(logo_block: str, slug: str) -> str:
    return (
        '<header class="hd hd--minimal" id="top"><div class="hd-in">'
        '<nav class="hd-l" aria-label="Main">'
        '<button type="button" class="hd-burger" aria-label="Open menu" aria-expanded="false" '
        'aria-controls="hd-mob"><i></i><i></i><span class="hd-burger-t" aria-hidden="true">Menu</span></button>'
        f'<a href="/services/" class="{_nav_cls(slug, "services")}">Services</a>'
        f'<a href="/portfolio/" class="{_nav_cls(slug, "portfolio")}">Portfolio</a>'
        f'<a href="/pricing/" class="{_nav_cls(slug, "pricing")}">Pricing</a>'
        "</nav>"
        f"{logo_block}"
        '<nav class="hd-r" aria-label="More">'
        f'<a href="/" class="{_nav_cls(slug, "home")}">Home</a>'
        f'<a href="/about/" class="{_nav_cls(slug, "about")}">About</a>'
        '<a href="/contact/" class="hd-cta">Contact</a>'
        "</nav></div></header>"
    )


def replace_hd_mob(text: str) -> str:
    marker = 'id="hd-mob"'
    start = text.find(marker)
    if start < 0:
        return text
    start = text.rfind("<div", 0, start)
    end = text.find('<div id="hd-pan', start)
    if end < 0:
        end = text.find('<div class="hd-scrim"', start)
    if end < 0:
        return text
    return text[:start] + MINIMAL_HD_MOB + text[end:]


def patch_header(text: str, rel_html: Path, base: Path) -> str:
    logo = RE_LOGO.search(text)
    if not logo:
        return text
    rel = rel_html.relative_to(base)
    slug = "home" if rel.parent == Path(".") else rel.parent.as_posix()
    if slug.startswith("blog/"):
        slug = "blog"
    text = RE_HEADER.sub(minimal_header(logo.group(0), slug), text, count=1)
    return replace_hd_mob(text)


def minimal_footer_from_page(text: str) -> str | None:
    logo = RE_FT_LOGO.search(text)
    bar = RE_FT_BAR.search(text)
    if not logo or not bar:
        return None
    return (
        '<footer class="ft ft--minimal"><div class="ft-in"><div class="ft-shell"><div class="ft-top">'
        f'<div class="ft-brand">{logo.group(0)}'
        '<p class="ft-tag">Built to rank, convert, and scale US aesthetic brands.</p></div>'
        f"{MINIMAL_FT_NAV}{MINIMAL_FT_CONTACT}</div>{bar.group(0)}</div></div></footer>"
    )


RE_SVC_GRID = re.compile(
    r'class="md:grid-cols-2 lg:grid-cols-3"',
)
RE_SVC_CARD = re.compile(
    r'(<a style="display:block;text-decoration:none;padding:2rem[^"]*" '
    r'href="/services/[^"]+" class=")hover:translate-y-\[-2px\](">)'
)


def _remove_balanced_div(text: str, start: int) -> str:
    """Remove one outer <div …>…</div> block starting at ``start``."""
    depth = 0
    i = start
    n = len(text)
    while i < n:
        if text.startswith("<div", i):
            depth += 1
            gt = text.find(">", i)
            if gt < 0:
                break
            i = gt + 1
            continue
        if text.startswith("</div>", i):
            depth -= 1
            i += 6
            if depth == 0:
                return text[:start] + text[i:]
            continue
        i += 1
    return text


def strip_legacy_hd_panels(text: str) -> str:
    """Drop unused mega-menu SSR (old /tools/ links confuse SEO crawlers)."""
    while True:
        m = re.search(r'<div id="hd-pan-', text)
        if not m:
            break
        text = _remove_balanced_div(text, m.start())
    text = re.sub(
        r'<script[^>]+src="[^"]*sygma-hd-pan\.js"[^>]*>\s*</script>\s*',
        "",
        text,
        flags=re.I,
    )
    return text


def patch_broken_tool_links(text: str) -> str:
    for old, new in TOOL_LINK_REPLACEMENTS:
        text = text.replace(old, new)
    return text


def patch_cf_email_obfuscation_skip(text: str) -> str:
    """Cloudflare Email Obfuscation can rewrite mailto → /cdn-cgi/l/email-protection (404 in audit)."""
    if "email_off" in text and "mailto:" in text:
        return text

    def _wrap_mailto(match: re.Match[str]) -> str:
        tag = match.group(0)
        if "<!--email_off-->" in tag:
            return tag
        return f"<!--email_off-->{tag}<!--/email_off-->"

    return re.sub(
        r'<a\b[^>]*href="mailto:[^"]+"[^>]*>[\s\S]*?</a>',
        _wrap_mailto,
        text,
        flags=re.I,
    )


def _blog_path_replacer(match: re.Match[str]) -> str:
    return "/services/"


def patch_canonical_paths(text: str) -> str:
    """Point internal links at final URLs (no 301/308 chains from minimal site redirects)."""
    while True:
        collapsed = re.sub(r"/services/[a-z0-9-]+", "/services/", text)
        if collapsed == text:
            break
        text = collapsed

    text = re.sub(r"/blog/([a-z0-9-]+)(?!/)", _blog_path_replacer, text)
    text = re.sub(r"/blog/([a-z0-9-]+)//+", r"/blog/\1/", text)

    for route in CANONICAL_DIR_ROUTES:
        text = re.sub(
            rf'href="/{route}"',
            f'href="/{route}/"',
            text,
        )
        text = re.sub(
            rf"href='/{route}'",
            f"href='/{route}/'",
            text,
        )
        text = re.sub(
            rf'href="(\.\./)+{route}"',
            rf'href="\1{route}/"',
            text,
        )
        text = re.sub(
            rf"href='(\.\./)+{route}'",
            rf"href='\1{route}/'",
            text,
        )

    text = text.replace('href="/contact"', 'href="/contact/"')
    text = text.replace("href='/contact'", "href='/contact/'")
    text = patch_retired_blog_urls(patch_case_study_urls(text))
    return text


_RE_CASE_STUDY_IMG = re.compile(r"/m/images/case-studies/[^\s\"'<>]+")


def _mask_case_study_image_paths(text: str) -> tuple[str, list[str]]:
    """Keep /m/images/case-studies/* filenames intact while rewriting page routes."""
    tokens: list[str] = []

    def _stash(match: re.Match[str]) -> str:
        tokens.append(match.group(0))
        return f"__SYGMA_CS_IMG_{len(tokens) - 1}__"

    return _RE_CASE_STUDY_IMG.sub(_stash, text), tokens


def _unmask_case_study_image_paths(text: str, tokens: list[str]) -> str:
    for i, path in enumerate(tokens):
        text = text.replace(f"__SYGMA_CS_IMG_{i}__", path)
    return text


# After a portfolio/case-study slug, next char must be a route delimiter (not `-` in filenames).
_CASE_STUDY_ROUTE_TAIL = r"(?=/|\"|'|\?|#|\s|$)"


def patch_case_study_urls(text: str) -> str:
    """Portfolio is canonical — no /case-studies/ URLs in HTML, JSON-LD, or JS."""
    text, img_tokens = _mask_case_study_image_paths(text)
    for old, new in LEGACY_CASE_STUDY_TO_PORTFOLIO.items():
        text = text.replace(f"https://sygmamedia.com/case-studies/{old}/", f"https://sygmamedia.com/portfolio/{new}/")
        text = re.sub(
            rf"https://sygmamedia\.com/case-studies/{re.escape(old)}{_CASE_STUDY_ROUTE_TAIL}",
            f"https://sygmamedia.com/portfolio/{new}/",
            text,
        )
        text = text.replace(f"/case-studies/{old}/", f"/portfolio/{new}/")
        text = re.sub(
            rf"/case-studies/{re.escape(old)}{_CASE_STUDY_ROUTE_TAIL}",
            f"/portfolio/{new}/",
            text,
        )
    for slug in CASE_STUDY_SLUGS:
        text = text.replace(f"/case-studies/{slug}/", f"/portfolio/{slug}/")
        text = text.replace(f'/case-studies/{slug}"', f'/portfolio/{slug}/"')
        text = re.sub(
            rf"/case-studies/{re.escape(slug)}{_CASE_STUDY_ROUTE_TAIL}",
            f"/portfolio/{slug}/",
            text,
        )
    text = text.replace("https://sygmamedia.com/case-studies/", "https://sygmamedia.com/portfolio/")
    text = text.replace("https://sygmamedia.com/case-studies", "https://sygmamedia.com/portfolio/")
    text = text.replace('href="/case-studies/"', 'href="/portfolio/"')
    text = text.replace('href="/case-studies"', 'href="/portfolio/"')
    text = text.replace("href='/case-studies/'", "href='/portfolio/'")
    text = text.replace("href='/case-studies'", "href='/portfolio/'")
    text = text.replace('href:"/case-studies"', 'href:"/portfolio/"')
    text = text.replace('href:"/case-studies/"', 'href:"/portfolio/"')
    text = text.replace("href:'/case-studies'", "href:'/portfolio/'")
    text = text.replace("href:'/case-studies/'", "href:'/portfolio/'")
    text = text.replace('"/case-studies"', '"/portfolio/"')
    text = text.replace('"/case-studies/"', '"/portfolio/"')
    text = text.replace("`/case-studies/${", "`/portfolio/${")
    text = text.replace('{label:"Case Studies",href:"/case-studies"}', '{label:"Portfolio",href:"/portfolio/"}')
    text = re.sub(r'A\(\["/case-studies"\]\)', 'A(["/portfolio/"])', text)
    text = re.sub(r'aria-current:T\("/case-studies"\)', 'aria-current:T("/portfolio/")', text)
    text = text.replace('children:"case studies"}', 'children:"portfolio"}')
    text = text.replace('children:"View Case', 'children:"View Portfol')
    return _unmask_case_study_image_paths(text, img_tokens)


def patch_retired_blog_urls(text: str) -> str:
    """Blog is retired from the minimal site — point stale links at /services/."""
    text = re.sub(r"https://sygmamedia\.com/blog(?:/[a-z0-9-]+)?/?", "https://sygmamedia.com/services/", text)
    text = re.sub(r'href="/blog/[^"]*"', 'href="/services/"', text)
    text = re.sub(r"href='/blog/[^']*'", "href='/services/'", text)
    for old, new in (
        ('href="/blog/"', 'href="/services/"'),
        ('href="/blog"', 'href="/services/"'),
        ("href='/blog/'", "href='/services/'"),
        ("href='/blog'", "href='/services/'"),
        ('href:"/blog"', 'href:"/services/"'),
        ('href:"/blog/"', 'href:"/services/"'),
    ):
        text = text.replace(old, new)
    return text


def patch_services_cards(text: str, path: Path, base: Path) -> str:
    try:
        rel = path.relative_to(base).as_posix()
    except ValueError:
        return text
    if rel != "services/index.html":
        return text
    text = RE_SVC_GRID.sub(
        'class="sygma-svc-grid md:grid-cols-2 lg:grid-cols-3"',
        text,
        count=1,
    )
    text = RE_SVC_CARD.sub(r"\1sygma-svc-card hover:translate-y-[-2px]\2", text)
    return text


RE_CAGR_DD = re.compile(
    r"<dd>13%</dd>",
    re.IGNORECASE,
)

SYGMA_SCRIPT_ANCHOR = '<script src="/assets/sygma-svc-scroll.js" defer></script>'


SPA_BOOTSTRAP_OLD = 'if(!admin&&!home){el.innerHTML="";Hn.createRoot(el).render(e.jsx(Md,{}))}'
SPA_BOOTSTRAP_CUR = (
    'if(!admin&&!home){el.innerHTML="";const bp=p.replace(/\\/+$/,"")||"/";'
    "Hn.createRoot(el).render(e.jsx(Md,{pathname:bp,search:window.location.search.slice(1)}))"
    "}"
)
SPA_BOOTSTRAP_NEW = (
    'if(!admin&&!home){el.innerHTML="";const bp=p.replace(/\\/+$/,"")||"/";'
    "Hn.createRoot(el).render(e.jsx(Md,{pathname:bp,search:window.location.search.slice(1)}))"
    "}"
)
SPA_MD_BROKEN = (
    'function Md({pathname:t,search:n}){const i=wd;return e.jsx(To,{children:e.jsx(Lo,'
    '{defaultTheme:"light",children:e.jsx(Mo,{children:e.jsxs(hn,{hook:i,ssrPath:t,ssrSearch:t?n:void 0,children:'
)
SPA_MD_FIXED = (
    'function Md({pathname:t,search:n}){const i=t?xd(t):wd;return e.jsx(To,{children:e.jsx(Lo,'
    '{defaultTheme:"light",children:e.jsx(Mo,{children:e.jsxs(hn,{hook:i,ssrSearch:t?n:void 0,children:'
)
# Wouter matches in definition order; listing route must not precede detail slugs.
CASE_STUDIES_ROUTES_OLD = (
    'e.jsx(M,{path:"/case-studies",component:jc}),'
    'e.jsx(M,{path:"/case-studies/beverly-hills-surgical",component:Cc}),'
    'e.jsx(M,{path:"/case-studies/scottsdale-wellness",component:Nc}),'
    'e.jsx(M,{path:"/case-studies/austin-medspa-collective",component:Tc}),'
    'e.jsx(M,{path:"/case-studies/chicago-facial-institute",component:Bc}),'
    'e.jsx(M,{path:"/case-studies/dallas-integrative-skin",component:Mc}),'
    'e.jsx(M,{path:"/case-studies/manhattan-dermatology",component:Ec}),'
    'e.jsx(M,{path:"/case-studies/miami-luxe-medspa",component:zc}),'
)
CASE_STUDIES_ROUTES_NEW = (
    'e.jsx(M,{path:"/case-studies/beverly-hills-surgical",component:Cc}),'
    'e.jsx(M,{path:"/case-studies/scottsdale-wellness",component:Nc}),'
    'e.jsx(M,{path:"/case-studies/austin-medspa-collective",component:Tc}),'
    'e.jsx(M,{path:"/case-studies/chicago-facial-institute",component:Bc}),'
    'e.jsx(M,{path:"/case-studies/dallas-integrative-skin",component:Mc}),'
    'e.jsx(M,{path:"/case-studies/manhattan-dermatology",component:Ec}),'
    'e.jsx(M,{path:"/case-studies/miami-luxe-medspa",component:zc}),'
    'e.jsx(M,{path:"/case-studies",component:jc}),'
)
ASSET_CACHE_TAG = "2026031307"


def strip_spa_case_study_routes(text: str) -> tuple[bool, str]:
    """Drop Wouter /case-studies routes so client nav cannot serve duplicate hubs."""
    new = re.sub(
        r'e\.jsx\(M,\{path:"/case-studies[^"]*",component:[A-Za-z]+\}\),',
        "",
        text,
    )
    return new != text, new


def write_cs_hydrate_script(dest: Path) -> None:
    """Hard redirect any legacy /case-studies URL before SPA boots."""
    legacy = LEGACY_CASE_STUDY_TO_PORTFOLIO
    pairs = ",".join(f'"{k}":"{v}"' for k, v in sorted(legacy.items()))
    content = f"""(function(){{
var p=(location.pathname.replace(/\\/+$/,"")||"/");
var m=p.match(/^\\/case-studies(?:\\/([^/]+))?$/);
if(!m)return;
var q=location.search||"",h=location.hash||"";
var slug=m[1];
var legacy={{{pairs}}};
if(slug&&legacy[slug])slug=legacy[slug];
location.replace((slug?"/portfolio/"+slug+"/":"/portfolio/")+q+h);
}})();
"""
    (dest / "assets" / "sygma-cs-hydrate.js").write_text(content, encoding="utf-8")


def patch_spa_bootstrap(dest: Path) -> bool:
    js = dest / "assets" / "index-C7q3mmBk.js"
    if not js.is_file():
        return False
    text = js.read_text(encoding="utf-8")
    changed = False
    for old in (SPA_BOOTSTRAP_OLD, SPA_BOOTSTRAP_CUR):
        if old in text:
            text = text.replace(old, SPA_BOOTSTRAP_NEW, 1)
            changed = True
            break
    if SPA_MD_BROKEN in text:
        text = text.replace(SPA_MD_BROKEN, SPA_MD_FIXED, 1)
        changed = True
    if CASE_STUDIES_ROUTES_OLD in text:
        text = text.replace(CASE_STUDIES_ROUTES_OLD, "", 1)
        changed = True
    elif CASE_STUDIES_ROUTES_NEW in text:
        text = text.replace(CASE_STUDIES_ROUTES_NEW, "", 1)
        changed = True
    stripped, text = strip_spa_case_study_routes(text)
    if stripped:
        changed = True
    patched = patch_case_study_urls(text)
    if patched != text:
        text = patched
        changed = True
    if changed:
        js.write_text(text, encoding="utf-8")
    i = text.find("function Md")
    routes_gone = 'path:"/case-studies"' not in text
    return (
        i >= 0
        and "const i=t?xd(t):wd" in text[i : i + 220]
        and "pathname:bp" in text
        and routes_gone
    )


def bust_js_cache(text: str) -> str:
    """Force browsers to pick up patched bundles after rebuild."""
    needle = 'src="/assets/index-C7q3mmBk.js"'
    tagged = f'src="/assets/index-C7q3mmBk.js?v={ASSET_CACHE_TAG}"'
    return text.replace(needle, tagged) if needle in text else text


def inject_spa_helpers(text: str) -> str:
    if "index-C7q3mmBk.js" not in text or "sygma-cs-hydrate.js" in text:
        return text
    needle = '<script type="module"'
    if needle not in text:
        return text
    return text.replace(
        needle,
        '<script src="/assets/sygma-cs-hydrate.js"></script>\n    ' + needle,
        1,
    )


def inject_motion_scripts(text: str) -> str:
    extra: list[str] = []
    if "data-rv" in text and "sygma-rv.js" not in text:
        extra.append('<script src="/assets/sygma-rv.js" defer></script>')
    if ("hm-nums" in text or 'id="market"' in text) and "sygma-hm-stats.js" not in text:
        extra.append('<script src="/assets/sygma-hm-stats.js" defer></script>')
    if not extra:
        return text
    block = SYGMA_SCRIPT_ANCHOR + "\n    " + "\n    ".join(extra)
    if SYGMA_SCRIPT_ANCHOR in text:
        return text.replace(SYGMA_SCRIPT_ANCHOR, block, 1)
    if "</head>" in text:
        return text.replace("</head>", "    " + "\n    ".join(extra) + "\n  </head>", 1)
    return text


def patch_faq_cta_copy(text: str, path: Path, base: Path) -> str:
    try:
        rel = path.relative_to(base).as_posix()
    except ValueError:
        return text
    if rel != "faq/index.html":
        return text
    return text.replace("Browse All Insights", "Browse the blog")


def patch_home_stats_markup(text: str, path: Path, base: Path) -> str:
    try:
        rel = path.relative_to(base).as_posix()
    except ValueError:
        return text
    if rel != "index.html":
        return text
    return RE_CAGR_DD.sub('<dd data-n="13" data-suf="%">13%</dd>', text, count=1)


HOME_HERO_DISC_OLD = (
    'ap-disc" aria-hidden="true">Brand · SEO · Websites · AI search · Ads</p>'
)
HOME_HERO_DISC_NEW = (
    'ap-disc">Growth · Websites · SEO · AI visibility · Paid media · Content</p>'
)


def patch_home_hero_disc(text: str, path: Path, base: Path) -> str:
    try:
        rel = path.relative_to(base).as_posix()
    except ValueError:
        return text
    if rel != "index.html":
        return text
    if HOME_HERO_DISC_OLD in text:
        return text.replace(HOME_HERO_DISC_OLD, HOME_HERO_DISC_NEW, 1)
    return text


MINIMAL_NAV_OVERRIDE = """    <style id="sygma-minimal-nav-override">
      @media (min-width:1280px){
        .hd.hd--minimal .hd-l .hd-k,.hd.hd--minimal .hd-r .hd-k,.hd.hd--minimal .hd-cta{display:inline-flex!important;align-items:center}
        .hd.hd--minimal .hd-burger{display:none!important}
        .pf-hd.hd--minimal .hd-l .hd-k,.pf-hd.hd--minimal .hd-r .hd-k,.pf-hd.hd--minimal .hd-cta{display:inline-flex!important}
      }
      @media (max-width:1279.98px){
        .hd.hd--minimal .hd-l .hd-k,.hd.hd--minimal .hd-r .hd-k,.hd.hd--minimal .hd-cta{display:none!important}
        .hd.hd--minimal .hd-burger{display:block!important}
        .pf-hd.hd--minimal .hd-l .hd-k,.pf-hd.hd--minimal .hd-r .hd-k,.pf-hd.hd--minimal .hd-cta{display:none!important}
        .pf-hd.hd--minimal .hd-burger{display:block!important}
      }
    </style>
"""


RE_MINIMAL_NAV_OVERRIDE = re.compile(
    r'<style id="sygma-minimal-nav-override">.*?</style>',
    re.DOTALL,
)


def patch_critical_minimal_nav(text: str) -> str:
    """Inline critical CSS hid nav below 1280px — keep .hd--minimal links visible."""
    if "hd--minimal" not in text:
        return text
    if 'id="sygma-minimal-nav-override"' in text:
        text = RE_MINIMAL_NAV_OVERRIDE.sub(
            MINIMAL_NAV_OVERRIDE.strip().replace("\n", "\n    "),
            text,
            count=1,
        )
    text = re.sub(
        r"\.hd-l \.hd-k,\.hd-r \.hd-k,\.hd-cta\{display:\s*none\s*!important\}",
        ".hd:not(.hd--minimal) .hd-l .hd-k,.hd:not(.hd--minimal) .hd-r .hd-k,"
        ".hd:not(.hd--minimal) .hd-cta{display:none!important}",
        text,
        count=1,
    )
    if 'id="sygma-minimal-nav-override"' not in text and 'id="sygma-critical"' in text:
        text = text.replace(
            "</style>\n    <script src=\"/assets/sygma-hd-guard.js\">",
            f"</style>\n{MINIMAL_NAV_OVERRIDE}    <script src=\"/assets/sygma-hd-guard.js\">",
            1,
        )
        text = text.replace(
            "</style>\n<script src=\"/assets/sygma-hd-guard.js\">",
            f"</style>\n{MINIMAL_NAV_OVERRIDE}<script src=\"/assets/sygma-hd-guard.js\">",
            1,
        )
    return text


def patch_one_html(text: str, path: Path, base: Path) -> str:
    text = patch_header(text, path, base)
    text = patch_critical_minimal_nav(text)
    text = patch_services_cards(text, path, base)
    text = patch_faq_cta_copy(text, path, base)
    text = patch_home_stats_markup(text, path, base)
    text = patch_home_hero_disc(text, path, base)
    text = patch_canonical_paths(text)
    text = strip_legacy_hd_panels(text)
    text = patch_broken_tool_links(text)
    text = patch_cf_email_obfuscation_skip(text)
    new_footer = minimal_footer_from_page(text)
    if new_footer:
        text = RE_FOOTER.sub(new_footer, text, count=1)
    for old, new in NAV_REPLACEMENTS:
        text = text.replace(old, new)
    text = inject_motion_scripts(text)
    text = inject_spa_helpers(text)
    text = bust_js_cache(text)
    if "sygma-minimal.css" not in text and "</head>" in text:
        text = text.replace(
            "</head>",
            '    <link rel="stylesheet" href="/assets/sygma-minimal.css" />\n  </head>',
            1,
        )
    return text


THEME_CSS_BUST = "2026111326"
HERO_VEIL_BUST = "2026111322"
MINIMAL_CSS_BUST = "2026111334"


def bump_theme_cache(base: Path) -> int:
    """Keep sygma-theme query string in sync after token/CSS changes."""
    n = 0
    pat = re.compile(r"(sygma-theme\.css\?v=)\d+")
    for path in base.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        new = pat.sub(rf"\g<1>{THEME_CSS_BUST}", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
    return n


def bump_minimal_css_cache(base: Path) -> int:
    pat = re.compile(r'(href="(?:\.\./)*assets/sygma-minimal\.css)(?:\?v=\d+)?(")')
    n = 0
    for path in base.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        new = pat.sub(rf"\1?v={MINIMAL_CSS_BUST}\2", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
    return n


def bump_hero_veil_cache(base: Path) -> int:
    """Cache-bust hero WebP URLs after regenerating /img/home/home-veil-*."""
    n = 0
    pat = re.compile(r"(/img/home/home-veil[^\"'?\\s]+?\.webp)(?:\?v=\d+)?")
    for path in base.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        new = pat.sub(rf"\g<1>?v={HERO_VEIL_BUST}", text)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
    return n


def patch_html_tree(base: Path) -> tuple[int, int]:
    changed = 0
    footers = 0
    for path in base.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        orig = text
        text = patch_one_html(text, path, base)
        if text != orig:
            path.write_text(text, encoding="utf-8")
            changed += 1
            if "ft--minimal" in text:
                footers += 1
    return changed, footers


def finalize_canonical_links(base: Path) -> int:
    """Static pages written after patch_html_tree still need direct final URLs."""
    n = 0
    for path in base.rglob("*.html"):
        text = path.read_text(encoding="utf-8", errors="replace")
        new = patch_canonical_paths(text)
        new = patch_case_study_urls(new)
        new = patch_retired_blog_urls(new)
        new = patch_portfolio_links_text(new)
        new = strip_legacy_hd_panels(new)
        new = patch_broken_tool_links(new)
        new = patch_cf_email_obfuscation_skip(new)
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
    return n


def patch_deploy_assets_for_seo(base: Path) -> int:
    """Rewrite stale tool routes inside copied SPA chunks."""
    n = 0
    assets = base / "assets"
    if not assets.is_dir():
        return 0
    for path in assets.glob("*.js"):
        if path.name.startswith("vendor-"):
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        new = patch_retired_blog_urls(patch_case_study_urls(patch_broken_tool_links(text)))
        if new != text:
            path.write_text(new, encoding="utf-8")
            n += 1
    return n


def strip_root_ssr(html: str) -> str:
    """Case study shells must not ship homepage SSR (hydration sticks on home route)."""
    marker = '<div id="root">'
    start = html.find(marker)
    if start < 0:
        return html
    tail_markers = (
        "<!-- Fill Your Calendar",
        '<script src="/assets/sygma-cs-hydrate',
        '<script type="module"',
    )
    end = len(html)
    for tm in tail_markers:
        pos = html.find(tm, start)
        if pos > start:
            end = min(end, pos)
    if end == len(html):
        return html
    chunk = html[start:end]
    close = chunk.rfind("</div>")
    if close < 0:
        return html
    abs_end = start + close + len("</div>")
    return html[:start] + '<div id="root"></div>\n    ' + html[abs_end:]


def case_study_shell_html(route_shell_html: str) -> str:
    """Same pattern as blog/:slug → blog/index.html SPA shell."""
    text = route_shell_html
    for old, new in (
        ('href="../fonts/', 'href="../../fonts/'),
        ('href="../brand/', 'href="../../brand/'),
        ('href="../favicon', 'href="../../favicon'),
        ('src="../brand/', 'src="../../brand/'),
        ("url(../fonts/", "url(../../fonts/"),
    ):
        text = text.replace(old, new)
    return text


def _load_portfolio_html():
    import importlib.util

    _ensure_scripts_path()
    path = ROOT / "platform" / "scripts" / "portfolio_html.py"
    spec = importlib.util.spec_from_file_location("portfolio_html", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_portfolio_css(dest: Path) -> None:
    src = ROOT / "platform" / "scripts" / "sygma-portfolio.css"
    if src.is_file():
        (dest / "assets" / "sygma-portfolio.css").write_text(
            src.read_text(encoding="utf-8"), encoding="utf-8"
        )


def patch_portfolio_links_text(text: str) -> str:
    for slug in CASE_STUDY_SLUGS:
        text = text.replace(f'"/case-studies/{slug}"', f'"/portfolio/{slug}/"')
        text = text.replace(f'"/case-studies/{slug}/"', f'"/portfolio/{slug}/"')
        text = text.replace(f'href="/case-studies/{slug}"', f'href="/portfolio/{slug}/"')
        text = text.replace(f"href='/case-studies/{slug}'", f"href='/portfolio/{slug}/'")
    for old, new in LEGACY_CASE_STUDY_TO_PORTFOLIO.items():
        text = text.replace(f'href="/case-studies/{old}"', f'href="/portfolio/{new}/"')
        text = text.replace(f'href="/case-studies/{old}/"', f'href="/portfolio/{new}/"')
        text = text.replace(f'"/case-studies/{old}"', f'"/portfolio/{new}/"')
        text = text.replace(f'"/case-studies/{old}/"', f'"/portfolio/{new}/"')

    def _href_case(m: re.Match[str]) -> str:
        slug = m.group(1)
        if slug in CASE_STUDY_SLUGS:
            return f'href="/portfolio/{slug}/"'
        if slug in LEGACY_CASE_STUDY_TO_PORTFOLIO:
            return f'href="/portfolio/{LEGACY_CASE_STUDY_TO_PORTFOLIO[slug]}/"'
        return 'href="/portfolio/"'

    text = re.sub(r'href="/case-studies/([^"/?#]+)/?"', _href_case, text)
    replacements = [
        ('href="/case-studies"', 'href="/portfolio/"'),
        ('href="/case-studies/"', 'href="/portfolio/"'),
        ("href='/case-studies'", "href='/portfolio/'"),
        ('>Case Studies</a>', '>Portfolio</a>'),
        ('class="hd-k is-on">Case Studies', 'class="hd-k is-on">Portfolio'),
        ('sygmamedia.com/case-studies"', 'sygmamedia.com/portfolio/"'),
        ('sygmamedia.com/case-studies/', 'sygmamedia.com/portfolio/'),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def patch_all_portfolio_links(dest: Path) -> int:
    n = 0
    for path in dest.rglob("*.html"):
        rel = path.relative_to(dest).as_posix()
        if rel.startswith("portfolio/") or rel.startswith("case-studies/"):
            if path.name == "index.html" and rel.count("/") >= 1:
                slug_part = rel.split("/")[1]
                if slug_part in CASE_STUDY_SLUGS or slug_part == "index.html":
                    continue
        text = path.read_text(encoding="utf-8", errors="replace")
        patched = patch_portfolio_links_text(text)
        if patched != text:
            path.write_text(patched, encoding="utf-8")
            n += 1
    return n


def patch_home_case_study_links(dest: Path) -> None:
    patch_all_portfolio_links(dest)


def _load_pricing_html():
    import importlib.util

    _ensure_scripts_path()
    path = ROOT / "platform" / "scripts" / "pricing_html.py"
    spec = importlib.util.spec_from_file_location("pricing_html", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_pricing_page(dest: Path) -> None:
    ph = _load_pricing_html()
    src_css = ROOT / "platform" / "scripts" / "sygma-pricing.css"
    if src_css.is_file():
        (dest / "assets" / "sygma-pricing.css").write_text(
            src_css.read_text(encoding="utf-8"), encoding="utf-8"
        )
    (dest / "pricing").mkdir(parents=True, exist_ok=True)
    (dest / "pricing" / "index.html").write_text(ph.render_pricing(depth=1), encoding="utf-8")


def _ensure_scripts_path() -> None:
    import sys

    scripts = ROOT / "platform" / "scripts"
    if str(scripts) not in sys.path:
        sys.path.insert(0, str(scripts))


def _load_about_html():
    import importlib.util

    _ensure_scripts_path()
    path = ROOT / "platform" / "scripts" / "about_html.py"
    spec = importlib.util.spec_from_file_location("about_html", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_about_page(dest: Path) -> None:
    ah = _load_about_html()
    src_css = ROOT / "platform" / "scripts" / "sygma-about.css"
    if src_css.is_file():
        (dest / "assets" / "sygma-about.css").write_text(
            src_css.read_text(encoding="utf-8"), encoding="utf-8"
        )
    (dest / "about").mkdir(parents=True, exist_ok=True)
    (dest / "about" / "index.html").write_text(ah.render_about(depth=1), encoding="utf-8")


def _load_legal_html():
    import importlib.util

    _ensure_scripts_path()
    path = ROOT / "platform" / "scripts" / "legal_html.py"
    spec = importlib.util.spec_from_file_location("legal_html", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def write_legal_pages(dest: Path) -> None:
    lh = _load_legal_html()
    src_css = ROOT / "platform" / "scripts" / "sygma-legal.css"
    if src_css.is_file():
        (dest / "assets" / "sygma-legal.css").write_text(
            src_css.read_text(encoding="utf-8"), encoding="utf-8"
        )
    (dest / "privacy-policy").mkdir(parents=True, exist_ok=True)
    (dest / "terms-of-service").mkdir(parents=True, exist_ok=True)
    (dest / "privacy-policy" / "index.html").write_text(
        lh.render_privacy(depth=1), encoding="utf-8"
    )
    (dest / "terms-of-service" / "index.html").write_text(
        lh.render_terms(depth=1), encoding="utf-8"
    )


def write_case_study_routes(dest: Path) -> int:
    """Static portfolio pages at /portfolio/ only (legacy /case-studies/* → 301 redirects)."""
    ph = _load_portfolio_html()
    write_portfolio_css(dest)
    (dest / "portfolio").mkdir(parents=True, exist_ok=True)
    hub = ph.render_hub(depth=1)
    (dest / "portfolio" / "index.html").write_text(hub, encoding="utf-8")
    written = 1
    for case in ph.PORTFOLIO_CASES:
        slug = case["slug"]
        page = ph.render_detail(case, depth=2)
        out_dir = dest / "portfolio" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(page, encoding="utf-8")
        written += 1
    patch_all_portfolio_links(dest)
    purge_case_studies_tree(dest)
    return written


def purge_case_studies_tree(dest: Path) -> None:
    """Remove duplicate /case-studies static tree (copied from source or old builds)."""
    cs = dest / "case-studies"
    if cs.exists():
        shutil.rmtree(cs)


def purge_blog_tree(dest: Path) -> None:
    """Blog retired — remove static /blog tree so only 301 redirects apply."""
    blog = dest / "blog"
    if blog.exists():
        shutil.rmtree(blog)


def write_redirects(dest: Path) -> None:
    lines = [
        "# Sygma Media — minimal agency site (generated)",
        "# Re-run: python3 platform/scripts/build_minimal_site.py",
        "",
        "# Drop SEO city landings → services hub",
        "/aesthetic-clinic-seo/* /services/ 301",
        "/plastic-surgery-seo/* /services/ 301",
        "",
        "# Individual service landings → services hub (hub page kept)",
        "/services/:slug /services/ 301",
        "",
        "# Legacy / intake / admin",
        "/admin/* /contact/ 301",
        "/intake/* /contact/ 301",
        "/guides/* /services/ 301",
        "/payment-success/* /contact/ 301",
        "",
        "# Retired blog → services hub",
        "/blog /services/ 301",
        "/blog/ /services/ 301",
        "/blog/* /services/ 301",
        "",
        "# Legacy tools → services",
        "/tools/clinic-launch-calculator /services/ 301",
        "/tools/digital-readiness-checklist /services/ 301",
        "/tools/* /services/ 301",
        "",
        "# Legacy case studies → portfolio (hub + detail slugs)",
        "/case-studies /portfolio/ 301",
        "/case-studies/ /portfolio/ 301",
    ]
    for slug in CASE_STUDY_SLUGS:
        lines.append(f"/case-studies/{slug} /portfolio/{slug}/ 301")
        lines.append(f"/case-studies/{slug}/ /portfolio/{slug}/ 301")
    for old, new in LEGACY_CASE_STUDY_TO_PORTFOLIO.items():
        lines.append(f"/case-studies/{old} /portfolio/{new}/ 301")
        lines.append(f"/case-studies/{old}/ /portfolio/{new}/ 301")
    lines.append("/case-studies/* /portfolio/:splat 301")
    content = "\n".join(lines)
    (dest / "_redirects").write_text(content, encoding="utf-8")


def write_robots_txt(dest: Path) -> None:
    """Explicit robots.txt (CF default omits Sitemap — Semrush flags as warning)."""
    content = "\n".join(
        [
            "# Sygma Media — minimal agency site (generated)",
            "# Re-run: python3 platform/scripts/build_minimal_site.py",
            "",
            "User-agent: *",
            "Allow: /",
            "Disallow: /blog",
            "",
            "Sitemap: https://sygmamedia.com/sitemap.xml",
            "",
        ]
    )
    (dest / "robots.txt").write_text(content, encoding="utf-8")


def write_minimal_sitemap(dest: Path) -> None:
    urls = [
        "/",
        "/about/",
        "/contact/",
        "/services/",
        "/pricing/",
        "/portfolio/",
        "/faq/",
        "/privacy-policy/",
        "/terms-of-service/",
    ]
    for slug in CASE_STUDY_SLUGS:
        urls.append(f"/portfolio/{slug}/")
    body = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        body.append(f"  <url><loc>https://sygmamedia.com{u}</loc></url>")
    body.append("</urlset>")
    (dest / "sitemap.xml").write_text("\n".join(body), encoding="utf-8")


def write_minimal_css(dest: Path) -> None:
    (dest / "assets" / "sygma-minimal.css").write_text(MINIMAL_CSS, encoding="utf-8")


def main() -> int:
    if not SOURCE.is_dir():
        print(f"Missing source: {SOURCE}", file=sys.stderr)
        return 1

    if DEST.exists():
        shutil.rmtree(DEST)
    DEST.mkdir(parents=True)

    for name in ASSET_DIRS:
        src = SOURCE / name
        if src.is_dir():
            shutil.copytree(src, DEST / name)

    for name in ROOT_FILES:
        src = SOURCE / name
        if src.is_file():
            shutil.copy2(src, DEST / name)

    for name in ROUTE_DIRS:
        src = SOURCE / name
        if not src.is_dir():
            continue
        if name == "services":
            (DEST / "services").mkdir(parents=True, exist_ok=True)
            for item in ["index.html", "index.raw.html"]:
                p = src / item
                if p.is_file():
                    shutil.copy2(p, DEST / "services" / item)
        else:
            shutil.copytree(src, DEST / name)

    write_redirects(DEST)
    write_minimal_sitemap(DEST)
    write_robots_txt(DEST)
    write_minimal_css(DEST)
    write_cs_hydrate_script(DEST)
    spa_bootstrapped = patch_spa_bootstrap(DEST)
    html_patched, footer_patched = patch_html_tree(DEST)
    case_study_routes = write_case_study_routes(DEST)
    write_pricing_page(DEST)
    write_about_page(DEST)
    write_legal_pages(DEST)
    portfolio_link_patches = patch_all_portfolio_links(DEST)
    canonical_links = finalize_canonical_links(DEST)
    asset_seo_patches = patch_deploy_assets_for_seo(DEST)
    bump_theme_cache(DEST)
    minimal_css_bumped = bump_minimal_css_cache(DEST)
    hero_cache_bumped = bump_hero_veil_cache(DEST)

    _ensure_scripts_path()
    from minify_assets import minify_assets_dir  # noqa: E402

    min_n, min_before, min_after = minify_assets_dir(DEST / "assets")
    purge_case_studies_tree(DEST)
    purge_blog_tree(DEST)
    write_minimal_sitemap(DEST)

    html_routes = sum(1 for _ in DEST.rglob("index.html"))
    readme = DEST / "README.md"
    readme.write_text(
        f"""# Sygma Media — minimal agency build

Generated from `01-sygma-media` without modifying the full site.

- **HTML routes:** {html_routes} (was ~296)
- **Blog:** retired (301 → /services/, not in sitemap)
  - **Portfolio / case study pages:** {case_study_routes} static (before/after charts, no React)
- **Live production:** not deployed until you approve `wrangler pages deploy`

## Preview locally

```bash
cd web-clones/sygma-minimal && python3 -m http.server 8790
```

## Deploy preview (separate Pages project)

```bash
npx wrangler pages deploy . --project-name=sygma-minimal
```
""",
        encoding="utf-8",
    )

    print(f"Built {DEST}")
    print(f"  html_routes={html_routes}")
    print(f"  html_patched={html_patched}")
    print(f"  minimal_footers={footer_patched}")
    print(f"  case_study_routes={case_study_routes}")
    print(f"  spa_bootstrap_patched={spa_bootstrapped}")
    print(f"  canonical_links_patched={canonical_links}")
    print(f"  asset_seo_patches={asset_seo_patches}")
    if min_n:
        saved = min_before - min_after
        pct = (100.0 * saved / min_before) if min_before else 0
        print(f"  assets_minified={min_n} ({min_before:,} → {min_after:,} bytes, −{pct:.1f}%)")
    else:
        print("  assets_minified=0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
