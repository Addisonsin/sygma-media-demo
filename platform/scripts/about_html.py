"""Static About page — persuasive US clinic narrative (no React)."""

from __future__ import annotations

import html
from pathlib import Path

from sygma_chrome import site_footer, site_header_block, static_head_extras

ROOT = Path(__file__).resolve().parents[2]

AB_CSS = "sygma-about.css?v=2026111325"
THEME_CSS = "/assets/sygma-theme.css?v=2026111326"
PF_CSS = "sygma-portfolio.css?v=2026111333"


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _prefix(depth: int) -> str:
    return "../" * depth


def render_about(depth: int = 1) -> str:
    p = _prefix(depth)
    pf_css = f"{p}assets/{PF_CSS}"
    ab_css = f"{p}assets/{AB_CSS}"
    img_base = f"{p}img/about"
    img_srcset = (
        f"{img_base}/about-hero-640.webp 640w, "
        f"{img_base}/about-hero-1000.webp 1000w, "
        f"{img_base}/about-hero-1440.webp 1440w"
    )
    canonical = "https://sygmamedia.com/about/"
    og_img = f"https://sygmamedia.com/img/about/about-hero-1000.webp"

    return f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{static_head_extras(depth)}
  <title>About Sygma Media — US aesthetic clinic growth partner</title>
  <meta name="description" content="Sygma Media helps US med spas and aesthetic practices turn search, Maps, web, and AI visibility into booked consults — with a senior three-founder delivery team and month-to-month partnerships." />
  <link rel="canonical" href="{_esc(canonical)}" />
  <meta property="og:title" content="About Sygma Media — US aesthetic clinic growth partner" />
  <meta property="og:description" content="Specialist SEO, Google Maps, websites, and AI search for US aesthetic clinics — built by founders who ship every month." />
  <meta property="og:url" content="{_esc(canonical)}" />
  <meta property="og:image" content="{_esc(og_img)}" />
  <meta property="og:type" content="website" />
  <link rel="icon" href="{p}favicon.ico" />
  <link rel="preload" as="image" type="image/webp" href="{img_base}/about-hero-1000.webp" imagesrcset="{img_srcset}" imagesizes="(min-width: 960px) 42vw, 100vw" fetchpriority="high" />
  <link rel="stylesheet" href="{THEME_CSS}" />
  <link rel="stylesheet" href="{p}assets/sygma-minimal.css" />
  <link rel="stylesheet" href="{pf_css}" />
  <link rel="stylesheet" href="{ab_css}" />
  <script type="application/ld+json">{{"@context":"https://schema.org","@type":"AboutPage","name":"About Sygma Media","url":"https://sygmamedia.com/about/","description":"US aesthetic clinic marketing agency — SEO, Maps, web, AI search.","publisher":{{"@type":"Organization","name":"Sygma Media","url":"https://sygmamedia.com"}}}}</script>
</head>
<body class="ab-body pf-body">
  <div class="hm sygma-static-shell">
  {site_header_block(depth, active="about")}
  <main class="ab-main">
    <section class="ab-hero container">
      <div class="ab-hero__copy">
        <p class="ab-crumb"><a href="{_esc('/' if depth == 0 else p)}">Home</a> / About</p>
        <p class="pf-eyebrow">About us</p>
        <h1 class="ab-h1">We build the digital engine that fills your consult calendar</h1>
        <p class="ab-lede"><strong>Sygma Media</strong> is a U.S.-focused growth partner for med spas, dermatology, and plastic surgery practices. We don&apos;t sell generic &quot;marketing packages&quot; — we ship the search, Maps, website, and AI visibility patients use <em>before</em> they ever call your front desk.</p>
        <p class="ab-lede">If you&apos;re tired of agencies that report impressions while consults stay flat, you&apos;re exactly who we built this for.</p>
        <div class="ab-hero__cta">
          <a class="ab-btn" href="{p}contact/">Start a conversation</a>
          <a class="ab-btn ab-btn--ghost" href="{p}pricing/">See pricing</a>
        </div>
      </div>
      <figure class="ab-hero__media">
        <img src="{img_base}/about-hero-1000.webp" srcset="{img_srcset}" sizes="(min-width: 960px) 42vw, 100vw" width="1000" height="1250" alt="Editorial portrait — Sygma Media aesthetic brand" fetchpriority="high" decoding="async" />
      </figure>
    </section>

    <section class="ab-panel container" aria-labelledby="ab-why-h">
      <h2 id="ab-why-h" class="ab-h2">Why clinic owners choose Sygma</h2>
      <p class="ab-intro">You&apos;re not buying slides. You&apos;re buying a pipeline: rankings that match how patients search, a site that earns trust in seconds, and Maps presence that wins &quot;near me&quot; — with reporting that ties work to consults, not vanity metrics.</p>
      <div class="ab-grid ab-grid--3">
        <article class="ab-card">
          <h3>Only aesthetics</h3>
          <p>We don&apos;t split focus across restaurants, law firms, and e‑commerce. Every playbook is tuned to treatment research, compliance-aware copy, and how patients actually choose a provider.</p>
        </article>
        <article class="ab-card">
          <h3>Senior delivery</h3>
          <p>Three U.S.-based founders cover strategy, SEO/web, and social execution — so your account never disappears into a junior queue.</p>
        </article>
        <article class="ab-card">
          <h3>No handcuffs</h3>
          <p>Month-to-month after onboarding. Cancel with 30 days&apos; notice. We&apos;d rather earn the next retainer with results than trap you in a multi-year contract.</p>
        </article>
      </div>
    </section>

    <section class="ab-panel container" aria-labelledby="ab-ship-h">
      <h2 id="ab-ship-h" class="ab-h2">What we ship every month</h2>
      <ul class="ab-list ab-grid ab-grid--2">
        <li><strong>Local &amp; organic SEO</strong> — treatment pages, blogs, and on-page fixes that match how patients search in your city.</li>
        <li><strong>Google Business Profile</strong> — posts, categories, photos, and Q&amp;A so Maps reflects a premium practice.</li>
        <li><strong>Website conversion</strong> — speed, trust blocks, and booking paths that turn traffic into form fills and calls.</li>
        <li><strong>AI &amp; structured data</strong> — entity copy and schema so ChatGPT, Perplexity, and Google AI can cite you accurately.</li>
        <li><strong>Transparent reporting</strong> — what went live, what moved in Search Console and Maps, and what we&apos;re doing next.</li>
        <li><strong>Portfolio-proof mindset</strong> — we document before/after visibility and consult trends like the cases in our <a href="{p}portfolio/">portfolio</a>.</li>
      </ul>
    </section>

    <section class="ab-panel container">
      <blockquote class="ab-quote">
        &ldquo;The right agency doesn&apos;t make you feel sold — it makes you feel understood. We learn your market, your competitors, and your consult goals, then we show you the work every month.&rdquo;
        <cite>How we partner with US practices</cite>
      </blockquote>
    </section>

    <section class="ab-panel container" aria-labelledby="ab-team-h">
      <h2 id="ab-team-h" class="ab-h2">Three founders, one accountable team</h2>
      <p class="ab-intro">Sygma Media was built by three founders based in the United States — one owns client strategy and delivery, one leads search, web, and technical SEO, and one runs social and content execution. You get direct senior attention without a single-person bottleneck or a rotating cast of account managers.</p>
      <p class="ab-intro">We&apos;re happy to introduce the team on a call before you commit. Names and photos can live on a dedicated team page when you&apos;re ready to publish them.</p>
    </section>

    <section class="ab-panel container" aria-labelledby="ab-fit-h">
      <h2 id="ab-fit-h" class="ab-h2">You&apos;re a great fit if&hellip;</h2>
      <ul class="ab-list">
        <li>You run (or are launching) a med spa, dermatology, or plastic surgery practice in the U.S.</li>
        <li>You want consult growth from organic search and Maps — not only paid ads.</li>
        <li>You value clear monthly deliverables over endless strategy decks.</li>
        <li>You&apos;re willing to approve content and give us CMS/GBP access so we can actually ship.</li>
      </ul>
    </section>

    <section class="ab-cta container" aria-labelledby="ab-cta-h">
      <p class="pf-eyebrow" id="ab-cta-h">Next step</p>
      <h2 class="ab-h2">Tell us about your clinic</h2>
      <p>Share your city, treatments, and consult goals. We&apos;ll map Launch, Growth, or Scale to your market — or tell you honestly if we&apos;re not the right fit.</p>
      <div class="ab-hero__cta" style="justify-content: center">
        <a class="ab-btn" href="{p}contact/">Book an intro call</a>
        <a class="ab-btn ab-btn--ghost" href="{p}portfolio/">View client work</a>
      </div>
    </section>
  </main>
  {site_footer(depth)}
  </div>
</body>
</html>"""
