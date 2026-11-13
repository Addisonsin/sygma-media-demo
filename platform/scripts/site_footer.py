"""Homepage-matching footer for static Sygma pages."""

from __future__ import annotations


def _prefix(depth: int) -> str:
    return "../" * depth if depth > 0 else ""


def render_site_footer(depth: int = 1) -> str:
    """Same structure as homepage ``ft ft--minimal`` with depth-relative URLs."""
    p = _prefix(depth)
    root = p if depth > 0 else "/"
    logo = f"{p}brand/alb-logo-ivory.png?v=2026111306"
    return f"""<footer class="ft ft--minimal"><div class="ft-in"><div class="ft-shell"><div class="ft-top"><div class="ft-brand"><a aria-label="Sygma Media, home" href="{root}" class="ft-logo"><img src="{logo}" alt="Sygma Media - Growth Partner for US Aesthetic & Medical Clinics" width="190" height="53" loading="lazy" decoding="async"/></a><p class="ft-tag">Built to rank, convert, and scale US aesthetic brands.</p></div><nav class="ft-cols" aria-label="Footer"><div class="ft-col"><div class="ft-h">Explore</div><a href="{p}services/">Services</a><a href="{p}pricing/">Pricing</a><a href="{p}portfolio/">Portfolio</a></div><div class="ft-col"><div class="ft-h">Company</div><a href="{p}about/">About</a><a href="{p}contact/">Contact</a><a href="{p}faq/">FAQ</a></div></nav><div class="ft-contact"><div class="ft-h">Contact</div><a class="ft-contact-link" href="tel:+12125550147">+1 (212) 555-0147</a><a class="ft-contact-link" href="mailto:exec@sygmamedia.com">exec@sygmamedia.com</a><p class="ft-loc">New York, NY · United States</p><div class="ft-social"><a href="https://www.instagram.com/" target="_blank" rel="noopener noreferrer">Instagram</a><a href="https://www.linkedin.com/company/sygmamedia" target="_blank" rel="noopener noreferrer">LinkedIn</a></div></div></div><div class="ft-bar"><p>© 2026 Sygma Media. All rights reserved. Aesthetic marketing agency, U.S.</p><div class="ft-legal"><a href="{p}privacy-policy/">Privacy Policy</a><a href="{p}terms-of-service/">Terms of Service</a><a href="{p}faq/">FAQ</a></div></div></div></div></footer>"""
