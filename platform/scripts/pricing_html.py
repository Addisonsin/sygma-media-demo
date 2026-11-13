"""Static pricing page — Breakline-style layout, Sygma tiers (no React)."""

from __future__ import annotations

import html
from pathlib import Path

from sygma_chrome import site_footer, site_header_block, static_head_extras

ROOT = Path(__file__).resolve().parents[2]

PR_CSS_NAME = "sygma-pricing.css?v=2026031407"
THEME_CSS = "/assets/sygma-theme.css?v=2026111326"


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _prefix(depth: int) -> str:
    return "../" * depth


PLANS = [
    {
        "name": "Launch",
        "tag": "Essentials",
        "price": "$1,299",
        "period": "/ month",
        "blurb": "Steady organic growth for a single location — search, Maps, and AI foundations without agency bloat.",
        "best_for": "Best for: one location building rankings and Maps presence before heavy ad spend.",
        "volume": [
            ("GBP posts", "1 / month"),
            ("SEO articles / treatment pages", "1 / month"),
            ("On-page optimisations", "Up to 2 pages / mo"),
        ],
        "deliverables": [
            "Google Business Profile management (hours, services, photos, Q&A hygiene)",
            "One researched SEO blog or treatment page (written, optimised, published)",
            "On-page SEO on up to 2 existing pages (titles, meta, internal links, CTAs)",
            "Technical SEO maintenance (crawl errors, speed flags, indexation checks)",
            "Local SEO signals (NAP consistency, categories, service areas)",
            "Structured data for clinic, services, and FAQ where applicable",
            "AI search baseline (entity copy, schema, citation-ready pages)",
            "Monthly performance report + 30-min strategy check-in",
        ],
        "featured": False,
    },
    {
        "name": "Growth",
        "tag": "Most clinics start here",
        "price": "$1,499",
        "period": "/ month",
        "blurb": "Our core partnership: more content, more Maps activity, and AI visibility tuned for consult volume.",
        "best_for": "Best for: clinics targeting 30–80+ qualified consults/mo from organic + Maps.",
        "volume": [
            ("GBP posts", "2 / month (bi-weekly)"),
            ("SEO articles / treatment pages", "2 / month"),
            ("On-page optimisations", "Up to 4 pages / mo"),
        ],
        "deliverables": [
            "Everything in Launch, plus higher monthly output",
            "Bi-weekly Google Business Profile posts (offers, treatments, seasonal hooks)",
            "Two SEO blogs or treatment pages per month (keyword-led, internal linking)",
            "On-page optimisation on up to 4 pages (landing pages, service hubs, location pages)",
            "AI search optimisation (ChatGPT / Perplexity / Google AI Overviews readiness)",
            "Maps & “near me” tuning (categories, services, photo cadence, review prompts)",
            "Conversion polish on key booking paths (headlines, trust blocks, form UX — no full redesign)",
            "Google Search Console + Maps insights reviewed monthly with action items",
            "Priority email support (business days, 1 business-day response target)",
        ],
        "featured": True,
    },
    {
        "name": "Scale",
        "tag": "Highest output",
        "price": "$2,499",
        "period": "/ month",
        "blurb": "Maximum SEO output, authority, and lead routing for multi-provider or multi-location brands.",
        "best_for": "Best for: busy practices, multiple providers, or aggressive market share goals.",
        "volume": [
            ("GBP posts", "4 / month (weekly)"),
            ("SEO articles / treatment pages", "4 / month"),
            ("On-page optimisations", "Up to 8 pages / mo"),
        ],
        "deliverables": [
            "Everything in Growth, plus our highest monthly cadence",
            "Weekly Google Business Profile posts and offer rotations",
            "Four SEO blogs or treatment pages per month (content cluster expansion)",
            "On-page optimisation on up to 8 pages (new launches, seasonal campaigns, pillars)",
            "Speed-to-lead & nurture touchpoints (missed-call text-back, intake routing guidance)",
            "Review & reputation workflow (GBP review asks, on-site proof alignment)",
            "Quarterly competitor & SERP landscape refresh with roadmap update",
            "Monthly report + 45-min strategy call; optional shared Slack for urgent requests",
            "Coordinated handoff notes if you run paid (creative/landing alignment — ads billed separately)",
        ],
        "featured": False,
    },
]

EVERY_PLAN = [
    "Complimentary setup in month one (audit, access, baseline tracking)",
    "Custom SEO + AI visibility roadmap for your market",
    "Keyword research & competitor gap analysis",
    "Website technical SEO monitoring (we work in your CMS — no mystery dashboards only)",
    "Google Analytics 4 + Search Console connected and reviewed",
    "Google Maps / GBP owned and kept accurate",
    "Structured data & brand entity building",
    "Tracking for Google rankings and AI answer mentions (monthly snapshot)",
    "Transparent monthly report: what we shipped, what moved, what’s next",
]

COMPARE_SECTIONS: list[tuple[str, list[tuple[str, str, str, str]]]] = [
    (
        "Setup & strategy (month one)",
        [
            ("Complimentary clinic audit & setup", "✓", "✓", "✓"),
            ("Custom SEO + AI roadmap", "✓", "✓", "✓"),
            ("Keyword & competitor research", "✓", "✓", "✓"),
            ("GA4 + Search Console connected", "✓", "✓", "✓"),
        ],
    ),
    (
        "What you receive every month",
        [
            ("Google Business Profile management", "✓", "✓", "✓"),
            ("GBP posts published", "1", "2 (bi-weekly)", "4 (weekly)"),
            ("SEO blog / treatment pages", "1", "2", "4"),
            ("On-page page optimisations", "2 pages", "4 pages", "8 pages"),
            ("Technical SEO maintenance", "✓", "✓", "✓"),
            ("Local / Maps SEO", "✓", "✓", "✓"),
            ("Structured data & schema", "✓", "✓", "✓"),
            ("AI search optimisation", "Baseline", "Active", "Active + reviews"),
            ("Conversion path tweaks (copy / UX)", "—", "Key paths", "Key paths + tests"),
            ("Speed-to-lead / nurture guidance", "—", "—", "✓"),
        ],
    ),
    (
        "Reporting & support",
        [
            ("Monthly performance report", "✓", "✓", "✓"),
            ("Strategy call", "30 min", "30 min", "45 min"),
            ("Email support", "✓", "Priority", "Priority + Slack opt-in"),
            ("Competitor landscape refresh", "Annual", "Annual", "Quarterly"),
        ],
    ),
]


def _plan_cards(contact_href: str) -> str:
    cards = []
    for plan in PLANS:
        feat = " pr-plan--feat" if plan["featured"] else ""
        vol = "".join(
            f'<li><span class="pr-plan__vol-k">{_esc(k)}</span><strong>{_esc(v)}</strong></li>'
            for k, v in plan["volume"]
        )
        deliver = "".join(f'<li>{_esc(x)}</li>' for x in plan["deliverables"])
        cards.append(
            f"""<article class="pr-plan{feat}">
  <p class="pr-plan__tag">{_esc(plan['tag'])}</p>
  <h2 class="pr-plan__name">{_esc(plan['name'])}</h2>
  <p class="pr-plan__price">{_esc(plan['price'])}<span>{_esc(plan['period'])}</span></p>
  <p class="pr-plan__blurb">{_esc(plan['blurb'])}</p>
  <p class="pr-plan__for">{_esc(plan['best_for'])}</p>
  <div class="pr-plan__vol-wrap">
    <p class="pr-plan__deliver-title">Monthly volume</p>
    <ul class="pr-plan__vol">{vol}</ul>
  </div>
  <div class="pr-plan__deliver-wrap">
    <p class="pr-plan__deliver-title">What your clinic gets each month</p>
    <ul class="pr-plan__deliver">{deliver}</ul>
  </div>
  <a class="pr-btn" href="{_esc(contact_href)}">Get started</a>
</article>"""
        )
    return f'<div class="pr-plans">{"".join(cards)}</div>'


def _compare_table() -> str:
    rows: list[str] = []
    for section, items in COMPARE_SECTIONS:
        rows.append(
            f'<tr class="pr-table__group"><th colspan="4" scope="colgroup">{_esc(section)}</th></tr>'
        )
        for label, a, b, c in items:
            rows.append(
                f'<tr><th scope="row">{_esc(label)}</th><td>{_esc(a)}</td><td>{_esc(b)}</td><td>{_esc(c)}</td></tr>'
            )
    body = "".join(rows)
    return f"""<div class="pr-table-wrap">
  <table class="pr-table">
    <caption class="sr-only">Compare plans — everything included for your clinic</caption>
    <thead>
      <tr><th scope="col">Deliverable</th><th scope="col">Launch</th><th scope="col">Growth</th><th scope="col">Scale</th></tr>
    </thead>
    <tbody>{body}</tbody>
  </table>
</div>"""


def render_pricing(*, depth: int = 1) -> str:
    p = _prefix(depth)
    css_href = f"{p}assets/{PR_CSS_NAME}"
    pf_css = f"{p}assets/sygma-portfolio.css?v=2026111333"
    inc = "".join(f"<li>{x}</li>" for x in EVERY_PLAN)
    contact = f"{p}contact/" if depth else "/contact/"
    portfolio = f"{p}portfolio/" if depth else "/portfolio/"
    return f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{static_head_extras(depth)}
  <title>Pricing — SEO & growth for US aesthetic clinics | Sygma Media</title>
  <meta name="description" content="Clear monthly pricing: what your aesthetic clinic gets each month — SEO, Google Maps, content, AI search, and reporting." />
  <link rel="canonical" href="https://sygmamedia.com/pricing/" />
  <link rel="icon" href="{p}favicon.ico" />
  <link rel="stylesheet" href="{THEME_CSS}" />
  <link rel="stylesheet" href="{p}assets/sygma-minimal.css" />
  <link rel="stylesheet" href="{pf_css}" />
  <link rel="stylesheet" href="{css_href}" />
</head>
<body class="pr-body pf-body">
  <div class="hm sygma-static-shell">
  {site_header_block(depth, active="pricing")}
  <main class="pr-main">
    <header class="pr-hero container">
      <p class="pf-eyebrow">Clear monthly pricing</p>
      <h1 class="pr-h1">What your clinic gets — every month</h1>
      <p class="pr-lede">Same strategic stack on every plan: SEO, Google Maps, your website, structured data, and AI visibility. <strong>Higher tiers = more pages, posts, and hands-on work shipped each month.</strong></p>
      <ul class="pr-badges" aria-label="Partnership terms">
        <li>Month-to-month</li>
        <li>Cancel with 30-day notice</li>
        <li>No annual lock-in</li>
        <li>Complimentary setup</li>
      </ul>
    </header>
    <aside class="pr-trust container" aria-labelledby="pr-trust-h">
      <div class="pr-trust__panel">
        <p class="pr-trust__eyebrow" id="pr-trust-h">Our promise to clinic owners</p>
        <blockquote class="pr-trust__quote">
          We don&apos;t win clients with handcuffs. You&apos;re on a <strong>rolling monthly partnership</strong> — if we&apos;re not delivering clear value, you may <strong>end with 30 days&apos; written notice</strong>. No multi-year trap, no surprise exit fees, no pressure calls. Most practices stay because consults and visibility grow — not because they&apos;re stuck.
        </blockquote>
        <ul class="pr-trust__points">
          <li><strong>You keep your assets</strong> — site, content we published, GBP access, and your data stay yours.</li>
          <li><strong>Transparent billing</strong> — one monthly fee per tier; scope is listed on this page.</li>
          <li><strong>Honest handoff</strong> — if you leave, we document logins, what&apos;s live, and what&apos;s scheduled.</li>
        </ul>
      </div>
    </aside>
    <section class="container" aria-labelledby="pr-plans-h">
      <h2 id="pr-plans-h" class="pr-h2 pr-h2--section">Choose your plan</h2>
      <p class="pr-section-intro pr-section-intro--center">Below is the full client deliverable list — not a teaser. If it’s listed, we ship it.</p>
      {_plan_cards(contact)}
    </section>
    <section class="pr-includes container">
      <h2 class="pr-h2">Included on every plan (baseline)</h2>
      <p class="pr-section-intro">These run in the background even when your tier focuses on content volume.</p>
      <ul class="pr-includes__list">{inc}</ul>
      <p class="pr-note"><strong>Foundation site build (one-time)</strong> — from <strong>$999</strong> if you need launch creative, high-conversion landing pages, pixels, and HIPAA-safe intake <em>before</em> monthly SEO. <a href="{_esc(contact)}">Ask us</a>.</p>
      <p class="pr-note"><strong>Growth Protocol add-on</strong> — Google & Meta ad management available on top of any SEO tier (ad spend paid by your clinic; we recommend $1,500+/mo minimum for learning).</p>
      <p class="pr-note pr-note--muted">You’ll always know what was done: every month’s report lists deliverables completed, rankings movement, Maps activity, and next-month priorities.</p>
    </section>
    <section class="container pr-compare">
      <h2 class="pr-h2">Full comparison</h2>
      <p class="pr-section-intro">Use this table when you’re deciding with a partner or surgeon — quantities are per month after onboarding.</p>
      {_compare_table()}
    </section>
    <section class="pr-steps container">
      <h2 class="pr-h2">What happens after you sign</h2>
      <ol class="pr-steps__list">
        <li><span class="pr-steps__n">1</span><div><h3>Choose your plan</h3><p>We confirm scope, access, and who owns GBP, site CMS, and forms.</p></div></li>
        <li><span class="pr-steps__n">2</span><div><h3>Week 1 onboarding</h3><p>Audit, tracking, roadmap, and your first month’s content calendar.</p></div></li>
        <li><span class="pr-steps__n">3</span><div><h3>Monthly rhythm</h3><p>Deliverables above ship on schedule; report + call; adjust tier if market demands it.</p></div></li>
      </ol>
    </section>
    <section class="pr-proof container">
      <h2 class="pr-h2">See clinics on these plans</h2>
      <p class="pr-section-intro">Portfolio pages show SEO, site, Maps, and before/after metrics.</p>
      <a class="pr-btn pr-btn--ghost" href="{_esc(portfolio)}">View portfolio →</a>
    </section>
    <section class="pr-faq container">
      <h2 class="pr-h2">Pricing questions</h2>
      <details class="pr-faq__item"><summary>Who writes and publishes the blog posts?</summary><p>We research, write, optimise, and publish in your CMS (or provide ready-to-publish drafts if you prefer approval first). You don’t need to supply briefs unless you want to.</p></details>
      <details class="pr-faq__item"><summary>What’s the difference between Launch, Growth, and Scale?</summary><p>The strategy stack is the same. Scale changes how much we produce each month: GBP posts, new pages, on-page optimisations, and support intensity.</p></details>
      <details class="pr-faq__item"><summary>Do we need a new website?</summary><p>No. Plans assume an existing site we can optimise. If you need a rebuild, start with the one-time Foundation build, then move to monthly SEO.</p></details>
      <details class="pr-faq__item"><summary>How does cancellation work?</summary><p>Plans are month-to-month after onboarding. To cancel, send written notice (email is fine) at least <strong>30 days</strong> before you want the partnership to end. You&apos;re billed for any work in that notice period; we don&apos;t charge separate &quot;break-up&quot; fees. We&apos;d rather earn next month&apos;s retainer than argue about fine print.</p></details>
      <details class="pr-faq__item"><summary>Do I sign a long contract?</summary><p>No annual or multi-year agreement required. Some clinics choose Growth or Scale for years — that&apos;s because results compound, not because a contract forces it.</p></details>
    </section>
    <section class="pf-cta container">
      <h2 class="pf-h2">Want a line-item proposal?</h2>
      <p class="pf-cta__text">Tell us your city, treatments, and consult goals. We’ll map deliverables to Launch, Growth, or Scale and send a scoped PDF.</p>
      <div class="pf-cta__actions">
        <a class="pf-btn" href="{_esc(contact)}">Get in touch</a>
        <a class="pf-btn pf-btn--ghost" href="{_esc(portfolio)}">Portfolio</a>
      </div>
    </section>
  </main>
  {site_footer(depth)}
  </div>
</body>
</html>"""
