"""Static portfolio content for the 7 homepage case studies (no React)."""

from __future__ import annotations

from typing import TypedDict


class Metric(TypedDict):
    label: str
    before: str
    after: str
    before_pct: int
    after_pct: int


class GrowthSignal(TypedDict):
    abbr: str
    title: str
    value: str
    note: str


class _PortfolioCaseCore(TypedDict):
    slug: str
    title: str
    location: str
    subtitle: str
    hero_image: str
    hero_alt: str
    deliverables: list[str]
    brand_story: str
    metrics: list[Metric]


class PortfolioCase(_PortfolioCaseCore, total=False):
    growth_chart_caption: str
    growth_signals: list[GrowthSignal]


PORTFOLIO_CASES: list[PortfolioCase] = [
    {
        "slug": "manhattan-dermatology",
        "title": "Manhattan Dermatology Partner",
        "location": "New York Metro",
        "subtitle": "From invisible on Google to a clinic patients — and AI — recommend.",
        "hero_image": "/m/images/case-studies/hampton-hero.webp",
        "hero_alt": "Manhattan Dermatology Partner reception, Upper East Side, Manhattan",
        "deliverables": [
            "Brand positioning & rebrand",
            "31-page SEO-led website",
            "Local SEO & Google Business Profile",
            "AI search (ChatGPT / Perplexity)",
            "Offer architecture & funnels",
        ],
        "brand_story": (
            "A respected New York Metro clinic had slipped off Google entirely. We rebuilt their "
            "position, visual identity, and site from scratch — then layered local SEO, Maps, and "
            "structured data so they read as one coherent brand across search, maps, and AI answers."
        ),
        "metrics": [
            {
                "label": "Consults booked (90 days)",
                "before": "Baseline",
                "after": "231",
                "before_pct": 12,
                "after_pct": 88,
            },
            {
                "label": "Google visibility (first 2 weeks post-launch)",
                "before": "Near zero",
                "after": "9,235 impressions",
                "before_pct": 8,
                "after_pct": 92,
            },
        ],
    },
    {
        "slug": "miami-luxe-medspa",
        "title": "Miami Luxe MedSpa",
        "location": "Miami, FL",
        "subtitle": "Speed-to-lead, local SEO, and treatment-level visibility.",
        "hero_image": "/img/cases/halcyon-hero.webp",
        "hero_alt": "Aerolase treatment at Miami Luxe MedSpa, Miami, FL",
        "deliverables": [
            "Technical SEO & local fixes",
            "Online booking flows",
            "CRM routing & speed-to-lead",
            "Google Maps optimization",
            "AI search treatment citations",
        ],
        "brand_story": (
            "Their site had been cloned from another market — wrong city signals, weak treatment pages. "
            "We re-pointed technical SEO at Miami, rebuilt key landings, and automated lead routing so "
            "paid and organic traffic converts instead of leaking."
        ),
        "metrics": [
            {
                "label": "Consult show rate",
                "before": "61%",
                "after": "89%",
                "before_pct": 61,
                "after_pct": 89,
            },
            {
                "label": "Body-contouring package ROAS (audited)",
                "before": "1×",
                "after": "11.5×",
                "before_pct": 18,
                "after_pct": 95,
            },
        ],
    },
    {
        "slug": "dallas-integrative-skin",
        "title": "Dallas Integrative Skin",
        "location": "Dallas, TX",
        "subtitle": "Rebrand, 129-page site, and search programme from day one.",
        "hero_image": "/m/images/editorial-2026-10/work/ada-photo.webp",
        "hero_alt": "Dallas Integrative Skin, Dallas, TX",
        "deliverables": [
            "Full rebrand & naming",
            "129-page consultation-first website",
            "SEO migration (zero URL loss)",
            "Local & technical SEO",
            "AI concierge / AI search layer",
        ],
        "brand_story": (
            "Dr Rakib Uddin's practice needed a new name and a digital home that matched clinical depth. "
            "We delivered Dallas Integrative Skin end-to-end: identity, copy-led site, domain migration, "
            "and organic plus AI discovery channels that speak to educated patients."
        ),
        "growth_chart_caption": "Inquiries, SEO indexation, and Maps calls — first 90 days post-rebrand",
        "growth_signals": [
            {
                "abbr": "SEO",
                "title": "Organic search",
                "value": "1,461",
                "note": "Pre-qualified inquiries (Q1)",
            },
            {
                "abbr": "MAP",
                "title": "Google Maps",
                "value": "DFW local pack",
                "note": "Dallas, TX · near-me routing",
            },
            {
                "abbr": "REV",
                "title": "Reviews & trust",
                "value": "4.9★ trajectory",
                "note": "GBP + on-site social proof",
            },
            {
                "abbr": "AI",
                "title": "AI discovery",
                "value": "< 14 days",
                "note": "Concierge + Perplexity citations",
            },
        ],
        "metrics": [
            {
                "label": "Pre-qualified inquiries (Q1)",
                "before": "Sporadic",
                "after": "1,461",
                "before_pct": 15,
                "after_pct": 90,
            },
            {
                "label": "AI concierge live",
                "before": "—",
                "after": "< 14 days",
                "before_pct": 5,
                "after_pct": 85,
            },
        ],
    },
    {
        "slug": "beverly-hills-surgical",
        "title": "Beverly Hills Surgical Aesthetics",
        "location": "Beverly Hills, CA",
        "subtitle": "Custom coded site, offers, and compliant lead workflows.",
        "hero_image": "/img/cases/drharry-hero.webp",
        "hero_alt": "Beverly Hills Surgical Aesthetics, Beverly Hills, CA",
        "deliverables": [
            "Full rebrand",
            "Custom-coded performance site",
            "Offer stack & funnels",
            "HIPAA-safe lead capture",
            "Meta + Google demand gen",
        ],
        "brand_story": (
            "A surgical aesthetics brand needed cinematic web presence without sacrificing speed or compliance. "
            "We rebuilt in code around their photography, wired HIPAA-safe workflows, and aligned paid and organic "
            "so high-ticket consults arrive pre-qualified."
        ),
        "metrics": [
            {
                "label": "Pipeline value",
                "before": "Quarter baseline",
                "after": "3.2× in two quarters",
                "before_pct": 28,
                "after_pct": 96,
            },
            {
                "label": "Qualified consults / month (Meta + Google)",
                "before": "Inconsistent",
                "after": "30–80",
                "before_pct": 22,
                "after_pct": 82,
            },
        ],
    },
    {
        "slug": "scottsdale-wellness",
        "title": "Scottsdale Wellness Clinic",
        "location": "Scottsdale, AZ",
        "subtitle": "Regenerative positioning, premium site, two-year organic roadmap.",
        "hero_image": "/m/images/case-studies/mesglo-aesthetic-clinic-hero.webp",
        "hero_alt": "Scottsdale Wellness Clinic, Scottsdale, AZ",
        "deliverables": [
            "Positioning & full rebrand",
            "Premium website",
            "SEO & content engine",
            "Google Maps programme",
            "Long-horizon organic strategy",
        ],
        "brand_story": (
            "We repositioned them as regenerative aesthetic authorities in Scottsdale — not another medi-spa listing. "
            "Brand, site, and content now tell one story while SEO and maps compound month over month."
        ),
        "metrics": [
            {
                "label": "Organic visibility (target treatments)",
                "before": "Flat",
                "after": "Upward trend",
                "before_pct": 25,
                "after_pct": 78,
            },
            {
                "label": "Content & SEO cadence",
                "before": "Ad hoc",
                "after": "Engine (24 mo)",
                "before_pct": 20,
                "after_pct": 88,
            },
        ],
    },
    {
        "slug": "austin-medspa-collective",
        "title": "Austin MedSpa Collective",
        "location": "Austin, TX",
        "subtitle": "Launch creative, site, and nurture in one ecosystem.",
        "hero_image": "/m/images/case-studies/luxe-skin-aesthetic-clinic-hero.webp",
        "hero_alt": "Austin MedSpa Collective, Austin, TX",
        "deliverables": [
            "Launch brand creative",
            "Website launch",
            "Local SEO foundation",
            "Patient nurture / email",
            "Maps + AI discovery",
        ],
        "brand_story": (
            "A new collective needed launch creative and a digital stack that could run without duct tape. "
            "We shipped brand, site, and nurture together so Austin search, maps, and AI channels reinforce the same offer."
        ),
        "metrics": [
            {
                "label": "Launch readiness",
                "before": "Pre-launch",
                "after": "Live ecosystem",
                "before_pct": 10,
                "after_pct": 92,
            },
            {
                "label": "Discovery channels aligned",
                "before": "1–2",
                "after": "Search + Maps + AI",
                "before_pct": 18,
                "after_pct": 86,
            },
        ],
    },
    {
        "slug": "chicago-facial-institute",
        "title": "Chicago Facial Institute",
        "location": "Chicago, IL",
        "subtitle": "Owned media, paid search, and site ops as one system.",
        "hero_image": "/m/images/case-studies/chicago-facial-institute-case-study-hero.webp",
        "hero_alt": "Chicago Facial Institute, Chicago, IL",
        "deliverables": [
            "SEO & AI search",
            "Website management",
            "Content & design support",
            "Email marketing",
            "Paid search integration",
        ],
        "brand_story": (
            "Dr Nina Bal's clinic needed a single partner for organic growth — not five freelancers. "
            "We run SEO, AI visibility, site, content, design, and paid as one operating system so "
            "Chicago patients find them everywhere they research."
        ),
        "metrics": [
            {
                "label": "Organic touchpoints managed",
                "before": "Fragmented",
                "after": "Unified OS",
                "before_pct": 22,
                "after_pct": 90,
            },
            {
                "label": "Channel coverage",
                "before": "SEO only",
                "after": "SEO + email + paid",
                "before_pct": 30,
                "after_pct": 85,
            },
        ],
    },
]
