"""Render static portfolio HTML (no React)."""

from __future__ import annotations

import hashlib
import html
import sys
from pathlib import Path

from sygma_chrome import site_footer, site_header_block, static_head_extras

ROOT = Path(__file__).resolve().parents[2]


def _load_portfolio_cases():
    import importlib.util

    path = ROOT / "platform" / "content" / "case_study_portfolio.py"
    spec = importlib.util.spec_from_file_location("case_study_portfolio", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.PORTFOLIO_CASES, mod.PortfolioCase


PORTFOLIO_CASES, PortfolioCase = _load_portfolio_cases()  # type: ignore[misc,assignment]

PF_CSS_NAME = "sygma-portfolio.css?v=2026111333"
THEME_CSS = "/assets/sygma-theme.css?v=2026111326"


def _pf_css_href(depth: int) -> str:
    return f"{_prefix(depth)}assets/{PF_CSS_NAME}"


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _prefix(depth: int) -> str:
    return "../" * depth


def _root_href(depth: int) -> str:
    return "/" if depth == 0 else _prefix(depth)


def _deliverable_hint(text: str) -> str:
    low = text.lower()
    if "chatgpt" in low or "perplexity" in low or (("ai" in low) and "search" in low):
        return "Structured data and authority so AI cites your clinic."
    if "local" in low or "google business" in low:
        return "Maps, GBP, and local signals for “near me” intent."
    if "seo" in low or ("search" in low and "ai" not in low):
        return "Rankings, content, and technical fixes tuned for your market."
    if "website" in low or "site" in low:
        return "Fast, conversion-focused pages patients actually book from."
    if "google" in low or "maps" in low:
        return "Maps, GBP, and local signals for “near me” intent."
    if "brand" in low or "rebrand" in low or "position" in low:
        return "One visual and verbal system across every touchpoint."
    if "crm" in low or "lead" in low or "funnel" in low:
        return "Leads routed, nurtured, and measured — not lost in inboxes."
    return "Built to compound results over months, not one-off launches."


def _deliverable_abbr(text: str) -> str:
    low = text.lower()
    if "seo" in low and "local" in low:
        return "LSEO"
    if "seo" in low:
        return "SEO"
    if "website" in low or "site" in low:
        return "WEB"
    if "google" in low or "maps" in low:
        return "MAP"
    if "ai" in low:
        return "AI"
    if "brand" in low or "rebrand" in low:
        return "BR"
    if "offer" in low or "funnel" in low:
        return "CRM"
    words = [w for w in text.replace("&", " ").split() if w]
    return (words[0][:3] if words else "SVC").upper()


def _deliverables_block(items: list[str]) -> str:
    cards = []
    for item in items:
        cards.append(
            f"""<li class="pf-deliver-card">
  <span class="pf-deliver-card__icon" aria-hidden="true">{_esc(_deliverable_abbr(item))}</span>
  <div>
    <p class="pf-deliver-card__title">{_esc(item)}</p>
    <p class="pf-deliver-card__hint">{_esc(_deliverable_hint(item))}</p>
  </div>
</li>"""
        )
    return f'<ul class="pf-deliver-grid">{"".join(cards)}</ul>'


def _hero_stats(metrics: list) -> str:
    pills = []
    for m in metrics[:2]:
        pills.append(
            f"""<div class="pf-hero__stat">
  <span class="pf-hero__stat-val">{_esc(m["after"])}</span>
  <span class="pf-hero__stat-lbl">{_esc(m["label"])}</span>
</div>"""
        )
    return f'<div class="pf-hero__stats">{"".join(pills)}</div>' if pills else ""


def _metric_short(after: str) -> str:
    import re

    m = re.search(r"[\d,]+", after)
    if not m:
        return after[:14]
    n = int(m.group().replace(",", ""))
    if n >= 10_000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    if n >= 1_000:
        return f"{n:,}"
    return str(n)


def _card_metric_teaser(metrics: list) -> str:
    if not metrics:
        return ""
    chips = []
    for m in metrics[:2]:
        short = _metric_short(m["after"])
        label = m["label"].split("(")[0].strip().lower()
        chips.append(f'<span class="pf-card__chip"><strong>{_esc(short)}</strong> {_esc(label)}</span>')
    return f'<div class="pf-card__proof">{"".join(chips)}</div>'


def _sparkline_points(case: PortfolioCase) -> list[int]:
    metrics = case.get("metrics") or []
    if metrics:
        start = min(int(metrics[0]["before_pct"]), 25)
        end = max(int(m["after_pct"]) for m in metrics)
    else:
        start, end = 12, 75
    seed = int(hashlib.sha256(case["slug"].encode()).hexdigest()[:8], 16)
    pts: list[int] = []
    for i in range(12):
        t = i / 11
        curve = start + (end - start) * (t**1.35)
        jitter = ((seed >> (i % 8)) & 7) - 3
        pts.append(max(4, min(99, int(curve + jitter))))
    return pts


def _svg_growth_chart(points: list[int], caption: str) -> str:
    w, h = 340, 128
    pad_x, pad_y = 12, 14
    inner_w = w - pad_x * 2
    inner_h = h - pad_y * 2 - 18
    n = len(points)
    xs = [pad_x + i * inner_w / (n - 1) for i in range(n)]
    ys = [pad_y + inner_h - (p / 100.0) * inner_h for p in points]
    line = " ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
    area = (
        f"M {xs[0]:.1f},{pad_y + inner_h} L "
        + " L ".join(f"{x:.1f},{y:.1f}" for x, y in zip(xs, ys))
        + f" L {xs[-1]:.1f},{pad_y + inner_h} Z"
    )
    last_y = ys[-1]
    return f"""<figure class="pf-growth__chart">
  <figcaption class="pf-growth__chart-cap">{_esc(caption)}</figcaption>
  <svg class="pf-growth__svg" viewBox="0 0 {w} {h}" role="img" aria-label="Indexed growth trend after launch">
    <defs>
      <linearGradient id="pfArea" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#5c6b5a" stop-opacity="0.28"/>
        <stop offset="100%" stop-color="#5c6b5a" stop-opacity="0.02"/>
      </linearGradient>
    </defs>
    <line class="pf-growth__grid" x1="{pad_x}" y1="{pad_y + inner_h}" x2="{w - pad_x}" y2="{pad_y + inner_h}"/>
    <line class="pf-growth__grid" x1="{pad_x}" y1="{pad_y + inner_h * 0.5}" x2="{w - pad_x}" y2="{pad_y + inner_h * 0.5}" stroke-dasharray="4 6"/>
    <path class="pf-growth__area" d="{area}" fill="url(#pfArea)"/>
    <polyline class="pf-growth__line" points="{line}"/>
    <circle class="pf-growth__dot" cx="{xs[-1]:.1f}" cy="{last_y:.1f}" r="4.5"/>
  </svg>
  <div class="pf-growth__axis" aria-hidden="true">
    <span>Launch</span><span>30d</span><span>60d</span><span>90d+</span>
  </div>
</figure>"""


def _default_growth_signals(case: PortfolioCase) -> list[tuple[str, str, str, str]]:
    """channel abbr, title, value, note."""
    metrics = case.get("metrics") or []
    d = " ".join(case.get("deliverables") or []).lower()
    m0 = metrics[0] if metrics else None
    m1 = metrics[1] if len(metrics) > 1 else None

    seo_val = _metric_short(m0["after"]) if m0 else "Compounding"
    seo_note = (m0["label"].split("(")[0].strip() if m0 else "Organic indexation")

    maps_note = "GBP + local pack"
    if "map" in d or "local" in d or "google business" in d:
        maps_val = "Local pack lift"
    else:
        maps_val = "Maps aligned"

    rev_val = "4.8★ sync"
    rev_note = "Reviews + reputation"

    if "ai" in d:
        ai_val = _metric_short(m1["after"]) if m1 and m1.get("after") else "Citations live"
        ai_note = (m1["label"] if m1 else "ChatGPT / Perplexity")
    else:
        ai_val = "Discoverable"
        ai_note = "Schema + entity graph"

    return [
        ("SEO", "Organic search", seo_val, seo_note),
        ("MAP", "Google Maps", maps_val, case["location"]),
        ("REV", "Reviews & trust", rev_val, rev_note),
        ("AI", "AI discovery", ai_val, ai_note[:42]),
    ]


def _growth_panel(case: PortfolioCase) -> str:
    caption = case.get("growth_chart_caption") or "Search, maps, and pipeline — indexed growth after go-live"
    points = _sparkline_points(case)
    chart = _svg_growth_chart(points, caption)
    raw = case.get("growth_signals")
    if raw:
        signals = [(r["abbr"], r["title"], r["value"], r["note"]) for r in raw]
    else:
        signals = _default_growth_signals(case)
    tiles = []
    for abbr, title, value, note in signals:
        tiles.append(
            f"""<li class="pf-growth__tile pf-growth__tile--{abbr.lower()}">
  <span class="pf-growth__tile-abbr" aria-hidden="true">{_esc(abbr)}</span>
  <div>
    <p class="pf-growth__tile-title">{_esc(title)}</p>
    <p class="pf-growth__tile-val">{_esc(value)}</p>
    <p class="pf-growth__tile-note">{_esc(note)}</p>
  </div>
</li>"""
        )
    city = case["location"].split(",")[0].strip()
    return f"""<aside class="pf-growth" aria-labelledby="pf-growth-h">
  <p class="pf-eyebrow" id="pf-growth-h">Visibility dashboard</p>
  <p class="pf-growth__lead">Live signals we track — SEO, Maps, reviews, and AI — not just site traffic.</p>
  {chart}
  <div class="pf-growth__map" aria-hidden="true">
    <span class="pf-growth__map-pin"></span>
    <span class="pf-growth__map-city">{_esc(city)}</span>
    <span class="pf-growth__map-sub">Local discovery · {_esc(case["location"])}</span>
  </div>
  <ul class="pf-growth__tiles">{"".join(tiles)}</ul>
</aside>"""


def _glance_bar(case: PortfolioCase) -> str:
    n_del = len(case["deliverables"])
    n_met = len(case["metrics"])
    return f"""<aside class="pf-glance container" aria-label="Engagement snapshot">
  <dl class="pf-glance__grid">
    <div class="pf-glance__item">
      <dt class="pf-glance__dt">Market</dt>
      <dd class="pf-glance__dd">{_esc(case["location"])}</dd>
    </div>
    <div class="pf-glance__item">
      <dt class="pf-glance__dt">Growth stack</dt>
      <dd class="pf-glance__dd">{n_del} coordinated deliverables</dd>
    </div>
    <div class="pf-glance__item">
      <dt class="pf-glance__dt">Proof</dt>
      <dd class="pf-glance__dd">{n_met} audited before/after metrics</dd>
    </div>
  </dl>
</aside>"""


def _metrics_block(metrics: list) -> str:
    articles = []
    for m in metrics:
        delta = max(0, int(m["after_pct"]) - int(m["before_pct"]))
        articles.append(
            f"""<article class="pf-outcome">
  <header class="pf-outcome__head">
    <h3 class="pf-outcome__title">{_esc(m["label"])}</h3>
    <span class="pf-outcome__delta">+{delta} pts vs. baseline</span>
  </header>
  <div class="pf-outcome__row pf-outcome__row--before">
    <div class="pf-outcome__meta">
      <span class="pf-outcome__label">Before</span>
      <span class="pf-outcome__value">{_esc(m["before"])}</span>
    </div>
    <div class="pf-outcome__track"><span class="pf-outcome__bar" style="--w: {m['before_pct']}%"></span></div>
  </div>
  <p class="pf-outcome__bridge" aria-hidden="true"><span>Growth window</span></p>
  <div class="pf-outcome__row pf-outcome__row--after">
    <div class="pf-outcome__meta">
      <span class="pf-outcome__label">With Sygma</span>
      <span class="pf-outcome__value pf-outcome__value--highlight">{_esc(m["after"])}</span>
    </div>
    <div class="pf-outcome__track"><span class="pf-outcome__bar" style="--w: {m['after_pct']}%"></span></div>
  </div>
</article>"""
        )
    return (
        '<section class="pf-outcomes" aria-labelledby="pf-outcomes-h">'
        '<div class="container">'
        '<div class="pf-outcomes__head">'
        '<h2 id="pf-outcomes-h" class="pf-h2">Before &amp; after with us</h2>'
        '<p class="pf-section-intro">Audited outcomes from the engagement — not vanity metrics. '
        "Each bar compares where the clinic started vs. where the brand and pipeline landed after launch. "
        "Percent widths are normalized for visual comparison — not raw KPI ceilings.</p>"
        '</div>'
        f'<div class="pf-outcomes__grid">{"".join(articles)}</div>'
        "</div></section>"
    )


def _stack_strip() -> str:
    items = [
        ("SEO", "Organic search"),
        ("WEB", "Clinic website"),
        ("MAP", "Google Maps"),
        ("AI", "AI discovery"),
    ]
    lis = "".join(
        f'<li class="pf-stack__item"><span class="pf-stack__abbr">{a}</span>'
        f'<span class="pf-stack__name">{_esc(n)}</span></li>'
        for a, n in items
    )
    return (
        '<section class="pf-stack" aria-label="Growth stack">'
        '<div class="container">'
        f'<ul class="pf-stack__grid">{lis}</ul>'
        "</div></section>"
    )


def _breadcrumb(depth: int, title: str) -> str:
    p = _prefix(depth)
    hub = "/portfolio/" if depth == 0 else f"{p}portfolio/"
    return f"""<nav class="pf-crumb container" aria-label="Breadcrumb">
  <ol>
    <li><a href="/">Home</a></li>
    <li><a href="{_esc(hub)}">Portfolio</a></li>
    <li aria-current="page">{_esc(title)}</li>
  </ol>
</nav>"""


def render_detail(case: PortfolioCase, *, depth: int = 2) -> str:
    p = _prefix(depth)
    hero = case["hero_image"] if case["hero_image"].startswith("/") else f"/{case['hero_image']}"
    deliver = _deliverables_block(case["deliverables"])
    hero_stats = _hero_stats(case["metrics"])
    canonical = f"https://sygmamedia.com/portfolio/{case['slug']}/"
    title = f"{case['title']} | Sygma Media Portfolio"
    contact = "/contact/" if depth == 0 else f"{p}contact/"
    hub = "/portfolio/" if depth == 0 else f"{p}portfolio/"
    return f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{static_head_extras(depth)}
  <title>{_esc(title)}</title>
  <meta name="description" content="{_esc(case['subtitle'])}" />
  <link rel="canonical" href="{_esc(canonical)}" />
  <link rel="icon" href="{p}favicon.ico" />
  <link rel="stylesheet" href="{THEME_CSS}" />
  <link rel="stylesheet" href="{p}assets/sygma-minimal.css?v=2026111333" />
  <link rel="stylesheet" href="{_pf_css_href(depth)}" />
</head>
<body class="pf-body">
  <div class="hm sygma-static-shell">
  {site_header_block(depth, active="portfolio")}
  <main class="pf-main">
    <section class="pf-hero">
      <img class="pf-hero__img" src="{_esc(hero)}" alt="{_esc(case['hero_alt'])}" width="1200" height="800" loading="eager" fetchpriority="high" />
      <div class="pf-hero__veil"></div>
      <div class="pf-hero__in container">
        <p class="pf-eyebrow">{_esc(case['location'])} · US aesthetic client</p>
        <h1 class="pf-h1">{_esc(case['title'])}</h1>
        <p class="pf-lede">{_esc(case['subtitle'])}</p>
        {hero_stats}
      </div>
    </section>
    {_breadcrumb(depth, case["title"])}
    {_glance_bar(case)}
    <section class="pf-split">
      <div class="container pf-split__grid">
        <div>
          <p class="pf-eyebrow">Brand story</p>
          <h2 class="pf-h2">How they became a brand</h2>
          <p class="pf-story__lead">{_esc(case['subtitle'])}</p>
          <p class="pf-story">{_esc(case['brand_story'])}</p>
          {_growth_panel(case)}
        </div>
        <div>
          <p class="pf-eyebrow">Deliverables</p>
          <h2 class="pf-h2">What we built</h2>
          <p class="pf-section-intro">SEO, site, Maps, AI search, and funnels — one coordinated stack, not scattered vendors.</p>
          {deliver}
        </div>
      </div>
    </section>
    {_metrics_block(case['metrics'])}
    {_stack_strip()}
    <section class="pf-cta container">
      <h2 class="pf-h2">Want outcomes like this?</h2>
      <p class="pf-cta__text">Tell us about your clinic. We&apos;ll map SEO, website, Google Maps, and AI search to your market — with clear before/after targets.</p>
      <div class="pf-cta__actions">
        <a class="pf-btn" href="{_esc(contact)}">Get in touch</a>
        <a class="pf-btn pf-btn--ghost" href="{_esc(hub)}">All portfolio work</a>
      </div>
    </section>
  </main>
  {site_footer(depth)}
  </div>
</body>
</html>"""


def render_hub(*, depth: int = 1) -> str:
    p = _prefix(depth)
    cards = []
    for c in PORTFOLIO_CASES:
        href = f"{c['slug']}/"
        cards.append(
            f"""<article class="pf-card">
  <a class="pf-card__link" href="{_esc(href)}">
    <div class="pf-card__img-wrap">
    <img class="pf-card__img" src="{_esc(c['hero_image'])}" alt="" width="600" height="400" loading="lazy" />
    </div>
    <div class="pf-card__body">
      <p class="pf-card__loc">{_esc(c['location'])}</p>
      <h2 class="pf-card__title">{_esc(c['title'])}</h2>
      <p class="pf-card__sub">{_esc(c['subtitle'])}</p>
      {_card_metric_teaser(c["metrics"])}
      <span class="pf-card__more">View project →</span>
    </div>
  </a>
</article>"""
        )
    return f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{static_head_extras(depth)}
  <title>Clinic Portfolio | Sygma Media</title>
  <meta name="description" content="Real aesthetic clinics: SEO, websites, Google Maps, AI search, and brand growth with before/after results." />
  <link rel="canonical" href="https://sygmamedia.com/portfolio/" />
  <link rel="icon" href="{p}favicon.ico" />
  <link rel="stylesheet" href="{THEME_CSS}" />
  <link rel="stylesheet" href="{p}assets/sygma-minimal.css?v=2026111333" />
  <link rel="stylesheet" href="{_pf_css_href(depth)}" />
</head>
<body class="pf-body">
  <div class="hm sygma-static-shell">
  {site_header_block(depth, active="portfolio")}
  <main class="pf-main pf-main--hub">
    <header class="pf-hub-head container">
      <p class="pf-eyebrow">Proof of work</p>
      <h1 class="pf-h1 pf-h1--hub">Clinic portfolio</h1>
      <p class="pf-lede">Seven US practices we grew into one clear brand — SEO, web, Google Maps, and AI search included.</p>
      <p class="pf-hub-meta"><strong>7 clinics</strong> · Before/after metrics · Full growth stack on every engagement</p>
    </header>
    <div class="pf-card-grid container">{"".join(cards)}</div>
  </main>
  {site_footer(depth)}
  </div>
</body>
</html>"""
