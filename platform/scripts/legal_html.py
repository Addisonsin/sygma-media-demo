"""Static Privacy Policy and Terms of Service (US, Sygma Media)."""

from __future__ import annotations

import html
from pathlib import Path

from sygma_chrome import site_footer, site_header_block, static_head_extras

ROOT = Path(__file__).resolve().parents[2]

LG_CSS = "sygma-legal.css?v=2026111331"
THEME_CSS = "/assets/sygma-theme.css?v=2026111326"
PF_CSS = "sygma-portfolio.css?v=2026111333"
EFFECTIVE = "November 13, 2026"
ENTITY = "Sygma Media LLC"
BRAND = "Sygma Media"
EMAIL = "exec@sygmamedia.com"
PHONE = "+1 (212) 555-0147"


def _esc(s: str) -> str:
    return html.escape(s, quote=True)


def _prefix(depth: int) -> str:
    return "../" * depth


def _shell(
    depth: int,
    *,
    title: str,
    description: str,
    canonical: str,
    crumb: str,
    h1: str,
    body: str,
) -> str:
    p = _prefix(depth)
    pf_css = f"{p}assets/{PF_CSS}"
    lg_css = f"{p}assets/{LG_CSS}"
    root = "/" if depth == 0 else p
    return f"""<!doctype html>
<html lang="en-US">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
{static_head_extras(depth)}
  <title>{_esc(title)}</title>
  <meta name="description" content="{_esc(description)}" />
  <link rel="canonical" href="{_esc(canonical)}" />
  <meta property="og:title" content="{_esc(title)}" />
  <meta property="og:description" content="{_esc(description)}" />
  <meta property="og:url" content="{_esc(canonical)}" />
  <meta property="og:type" content="website" />
  <link rel="icon" href="{p}favicon.ico" />
  <link rel="stylesheet" href="{THEME_CSS}" />
  <link rel="stylesheet" href="{p}assets/sygma-minimal.css" />
  <link rel="stylesheet" href="{pf_css}" />
  <link rel="stylesheet" href="{lg_css}" />
</head>
<body class="lg-body pf-body">
  <div class="hm sygma-static-shell">
  {site_header_block(depth)}
  <main class="lg-main">
    <header class="lg-hero container">
      <p class="lg-crumb"><a href="{_esc(root)}">Home</a> / {crumb}</p>
      <p class="pf-eyebrow">Legal</p>
      <h1 class="lg-h1">{h1}</h1>
      <p class="lg-updated">Effective date: {EFFECTIVE} · {ENTITY} · United States</p>
      <p class="lg-note">This summary is provided for transparency on our website. It is not legal advice. For questions, contact <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
    </header>
    <div class="lg-prose container">
      {body}
    </div>
  </main>
  {site_footer(depth)}
  </div>
</body>
</html>"""


def render_privacy(depth: int = 1) -> str:
    p = _prefix(depth)
    terms = f"{p}terms-of-service/"
    contact = f"{p}contact/"
    pricing = f"{p}pricing/"
    body = f"""
      <section id="overview" aria-labelledby="lg-p1">
        <h2 id="lg-p1">Overview</h2>
        <p>{ENTITY} (&ldquo;{BRAND},&rdquo; &ldquo;we,&rdquo; &ldquo;us&rdquo;) provides digital marketing, SEO, website, Google Business Profile, and related services to aesthetic and medical practices in the United States. This Privacy Policy describes how we collect, use, and share information when you visit <strong>sygmamedia.com</strong>, contact us, or use our services as a client or prospective client.</p>
      </section>
      <section id="collect" aria-labelledby="lg-p2">
        <h2 id="lg-p2">Information we collect</h2>
        <h3>Information you provide</h3>
        <ul>
          <li>Contact details (name, email, phone, practice name, city, website URL) when you submit forms or email us.</li>
          <li>Business information needed to deliver services (logins you authorize, brand assets, content approvals, reporting recipients).</li>
          <li>Communications (emails, messages, call notes) related to proposals, onboarding, and ongoing work.</li>
        </ul>
        <h3>Information collected automatically</h3>
        <ul>
          <li>Device and usage data on our website (IP address, browser type, pages viewed, referring URL, approximate location from IP).</li>
          <li>Cookies and similar technologies for site functionality, analytics, and performance (see <a href="#cookies">Cookies</a>).</li>
        </ul>
        <h3>Client marketing data</h3>
        <p>When you hire us, we may access analytics, search consoles, ad accounts, CRM exports, or website CMS data <strong>only with your permission</strong>, to perform the services described on our <a href="{pricing}">pricing</a> page and in your statement of work.</p>
      </section>
      <section id="use" aria-labelledby="lg-p3">
        <h2 id="lg-p3">How we use information</h2>
        <ul>
          <li>Respond to inquiries and provide proposals.</li>
          <li>Perform contracted services (SEO, content, Maps, web updates, reporting).</li>
          <li>Improve our website, security, and client experience.</li>
          <li>Send operational messages (billing, deliverables, account notices).</li>
          <li>Comply with law, enforce our <a href="{terms}">Terms of Service</a>, and protect our rights.</li>
        </ul>
        <p>We do not sell your personal information. We do not use client PHI for our own marketing. If you are a covered entity under HIPAA, any handling of protected health information is governed by your separate Business Associate Agreement (BAA) or client agreement—not this public summary alone.</p>
      </section>
      <section id="share" aria-labelledby="lg-p4">
        <h2 id="lg-p4">How we share information</h2>
        <p>We share information only as needed to run our business:</p>
        <ul>
          <li><strong>Service providers</strong> (hosting, email, analytics, project tools) under confidentiality obligations.</li>
          <li><strong>Platforms you authorize</strong> (Google, Meta, your CMS host) when we manage accounts on your behalf.</li>
          <li><strong>Professional advisors</strong> (legal, accounting) when required.</li>
          <li><strong>Legal disclosures</strong> if required by law, subpoena, or to protect safety and rights.</li>
        </ul>
        <p>Our site is hosted on Cloudflare Pages; analytics or tag managers may process data in the United States and other regions where those providers operate.</p>
      </section>
      <section id="retention" aria-labelledby="lg-p5">
        <h2 id="lg-p5">Retention &amp; security</h2>
        <p>We retain information for as long as needed to provide services, meet legal obligations, and resolve disputes. When a client ends a partnership, we follow the handoff steps in our Terms and client agreement (access documentation; you keep your live assets).</p>
        <p>We use reasonable administrative, technical, and organizational safeguards. No method of transmission or storage is 100% secure; please use strong passwords and limit shared access.</p>
      </section>
      <section id="rights" aria-labelledby="lg-p6">
        <h2 id="lg-p6">Your privacy rights (United States)</h2>
        <p>Depending on your state of residence, you may have rights to access, correct, delete, or obtain a copy of personal information we hold about you, and to opt out of certain processing (including targeted advertising where applicable).</p>
        <p><strong>California residents (CCPA/CPRA):</strong> You may request to know, delete, or correct personal information, and to opt out of the &ldquo;sale&rdquo; or &ldquo;sharing&rdquo; of personal information. We do not sell personal information. To exercise rights, email <a href="mailto:{EMAIL}">{EMAIL}</a> with &ldquo;Privacy Request&rdquo; in the subject. We will verify your request as required by law.</p>
        <p>Residents of Colorado, Connecticut, Virginia, Utah, Texas, Oregon, and other states with comprehensive privacy laws may have similar rights—we will honor applicable requests in line with those laws.</p>
      </section>
      <section id="cookies" aria-labelledby="lg-p7">
        <h2 id="lg-p7">Cookies &amp; analytics</h2>
        <p>We may use cookies and similar technologies for essential site functions, to remember preferences, and to understand traffic (e.g., Google Analytics or similar). You can control cookies through your browser settings; blocking cookies may affect site functionality.</p>
      </section>
      <section id="children" aria-labelledby="lg-p8">
        <h2 id="lg-p8">Children</h2>
        <p>Our services and website are directed to business owners and professionals. We do not knowingly collect personal information from children under 13 (COPPA). If you believe a child has provided information to us, contact us to request deletion.</p>
      </section>
      <section id="changes" aria-labelledby="lg-p9">
        <h2 id="lg-p9">Changes &amp; contact</h2>
        <p>We may update this policy from time to time. We will post the revised version on this page with a new effective date. Material changes may be communicated to active clients by email.</p>
        <p>Questions or requests: <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:+12125550147">{PHONE}</a> · <a href="{contact}">Contact form</a>.</p>
      </section>
    """
    return _shell(
        depth,
        title=f"Privacy Policy | {BRAND}",
        description="How Sygma Media collects, uses, and protects information for US aesthetic clinic marketing clients and website visitors.",
        canonical="https://sygmamedia.com/privacy-policy/",
        crumb="Privacy Policy",
        h1="Privacy Policy",
        body=body,
    )


def render_terms(depth: int = 1) -> str:
    p = _prefix(depth)
    privacy = f"{p}privacy-policy/"
    pricing = f"{p}pricing/"
    contact = f"{p}contact/"
    body = f"""
      <section id="agreement" aria-labelledby="lg-t1">
        <h2 id="lg-t1">Agreement</h2>
        <p>These Terms of Service (&ldquo;Terms&rdquo;) govern your use of <strong>sygmamedia.com</strong> and any marketing, SEO, web, or related services provided by {ENTITY} (&ldquo;{BRAND},&rdquo; &ldquo;we,&rdquo; &ldquo;us&rdquo;). By using the site or engaging us as a client, you agree to these Terms and our <a href="{privacy}">Privacy Policy</a>.</p>
        <p>If you sign a separate master services agreement, statement of work, or order form, those documents control where they conflict with these general Terms.</p>
      </section>
      <section id="services" aria-labelledby="lg-t2">
        <h2 id="lg-t2">Services</h2>
        <p>{BRAND} provides digital growth services for U.S. aesthetic, dermatology, and plastic surgery practices, including organic search, Google Business Profile management, website optimization, structured data, AI search readiness, content, and optional paid media support as described on our <a href="{pricing}">pricing</a> page and in your contract.</p>
        <p>We do not provide medical advice, diagnose conditions, or guarantee specific clinical outcomes. You remain responsible for clinical care, informed consent, and regulatory compliance.</p>
      </section>
      <section id="client" aria-labelledby="lg-t3">
        <h2 id="lg-t3">Client responsibilities</h2>
        <ul>
          <li>Provide timely approvals, accurate business information, and authorized access to tools we need to perform work.</li>
          <li>Ensure marketing claims comply with FTC truth-in-advertising standards, FDA guidance for cosmetics/devices where applicable, and state medical board rules.</li>
          <li>Maintain licenses, insurance, and HIPAA/program requirements for your practice. Do not send us unnecessary patient health information unless covered by a signed BAA.</li>
          <li>Review published content and ads; you are ultimately responsible for what goes live under your brand.</li>
        </ul>
      </section>
      <section id="fees" aria-labelledby="lg-t4">
        <h2 id="lg-t4">Fees, billing &amp; cancellation</h2>
        <p>Monthly plans are billed in advance unless your contract states otherwise. Setup or one-time project fees are described in your proposal. Unless a signed contract says otherwise, monthly SEO partnerships are <strong>month-to-month</strong> with <strong>30 days&rsquo; written notice</strong> to cancel, as described on our pricing page.</p>
        <p>Late payments may pause work. You are responsible for third-party costs (ad spend, stock assets, premium plugins) unless we include them in writing.</p>
      </section>
      <section id="ip" aria-labelledby="lg-t5">
        <h2 id="lg-t5">Intellectual property</h2>
        <p>You own your pre-existing brand assets, trademarks, and content you supply. Upon full payment, deliverables created specifically for you (e.g., copy we wrote for your site, graphics we produced under contract) are assigned to you as stated in your agreement.</p>
        <p>{BRAND} retains ownership of our methodologies, templates, internal tools, and general know-how. We may showcase non-confidential work in our portfolio unless you opt out in writing.</p>
      </section>
      <section id="results" aria-labelledby="lg-t6">
        <h2 id="lg-t6">No guaranteed results</h2>
        <p>Search rankings, traffic, consult volume, and ad performance depend on competition, budget, seasonality, platform algorithms, and your operations. We report in good faith and follow industry best practices, but <strong>we do not guarantee</strong> specific positions, revenue, or patient counts.</p>
      </section>
      <section id="warranty" aria-labelledby="lg-t7">
        <h2 id="lg-t7">Disclaimers &amp; limitation of liability</h2>
        <p>The website and services are provided &ldquo;as is&rdquo; and &ldquo;as available.&rdquo; To the fullest extent permitted by law, we disclaim implied warranties of merchantability, fitness for a particular purpose, and non-infringement.</p>
        <p>To the maximum extent permitted by applicable law, {ENTITY}&rsquo;s total liability arising from these Terms or the services will not exceed the fees you paid to us in the <strong>three (3) months</strong> before the event giving rise to the claim. We are not liable for indirect, incidental, consequential, or punitive damages, or for third-party platform outages.</p>
      </section>
      <section id="indemnity" aria-labelledby="lg-t8">
        <h2 id="lg-t8">Indemnification</h2>
        <p>You agree to indemnify and hold harmless {BRAND} and its members, employees, and contractors from claims arising from your content, your clinical services, your violation of law, or your breach of these Terms, except to the extent caused by our gross negligence or willful misconduct.</p>
      </section>
      <section id="law" aria-labelledby="lg-t9">
        <h2 id="lg-t9">Governing law &amp; disputes</h2>
        <p>These Terms are governed by the laws of the <strong>State of New York</strong>, without regard to conflict-of-law rules. Exclusive venue for disputes shall be state or federal courts located in New York County, New York, unless applicable law requires otherwise.</p>
        <p>Before filing suit, the parties agree to attempt good-faith resolution by contacting <a href="mailto:{EMAIL}">{EMAIL}</a>.</p>
      </section>
      <section id="site" aria-labelledby="lg-t10">
        <h2 id="lg-t10">Website use</h2>
        <p>You may not scrape, reverse engineer, or interfere with site security. You may not use our materials to misrepresent affiliation with {BRAND}. We may modify or discontinue site content at any time.</p>
      </section>
      <section id="contact" aria-labelledby="lg-t11">
        <h2 id="lg-t11">Contact</h2>
        <p>{ENTITY}<br />New York, NY · United States<br />
        <a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="tel:+12125550147">{PHONE}</a><br />
        <a href="{contact}">Contact page</a></p>
      </section>
    """
    return _shell(
        depth,
        title=f"Terms of Service | {BRAND}",
        description="Terms of Service for Sygma Media — US aesthetic clinic marketing, SEO, and digital services.",
        canonical="https://sygmamedia.com/terms-of-service/",
        crumb="Terms of Service",
        h1="Terms of Service",
        body=body,
    )
