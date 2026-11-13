# Sygma Site Platform — Architecture (Phase 1)

## Decision summary

| Layer | Choice | Rationale |
|-------|--------|-----------|
| CMS data store | **PostgreSQL** (SQLite for local dev) | Multi-tenant relational model, revisions, audit, job queue metadata |
| API | **FastAPI** (Python) | Same ecosystem as existing `01-sygma-media` patch tooling; easy static publisher integration |
| Dashboard | **React + Vite + TypeScript** | Separate from public site bundles; agency-grade UI without touching minified ALB JS |
| Auth | **JWT (httpOnly-ready) + bcrypt** | No third-party account required to develop; Clerk/Auth0 adapter documented in ENV.md |
| Media | **Local disk (dev) + R2 adapter (prod)** | Cloudflare-aligned; CDN via custom domain on R2 public bucket or Workers |
| Public sites | **Existing static tree + incremental generator** | Preserves design/HTML; generator patches SSR + structured JSON — does not replace entire React app in Phase 1 |
| Deploy | **Cloudflare Pages API** (server-side only) | Credentials never in browser; jobs run on API worker |

Third-party headless CMS (Sanity/Contentful/Strapi) was **not** chosen: this project needs **tenant isolation, publish jobs, and Cloudflare deploy** as first-class features. A custom headless core with structured JSON schemas is cheaper and matches the static-export constraint.

## System context

```
┌─────────────────────────────────────────────────────────────┐
│  Agency / Client Dashboard (platform/dashboard)              │
│  React SPA → REST API + cookies/JWT                        │
└───────────────────────────┬─────────────────────────────────┘
                            │ HTTPS
┌───────────────────────────▼─────────────────────────────────┐
│  Platform API (platform/api)                                 │
│  Auth · Tenants · Content revisions · Media · Publish jobs   │
└───────┬─────────────────────────────┬─────────────────────┘
        │                             │
        ▼                             ▼
┌───────────────┐            ┌────────────────────┐
│  PostgreSQL   │            │  Media storage      │
│  (or SQLite)  │            │  local / R2         │
└───────────────┘            └────────────────────┘
        │
        ▼
┌───────────────────────────────────────────────────────────────┐
│  Publisher worker (platform/publisher)                          │
│  draft snapshot → validate → static patch/build → deploy job    │
└───────────────────────────┬───────────────────────────────────┘
                            │ CF API (when configured)
                            ▼
┌───────────────────────────────────────────────────────────────┐
│  Client websites (web-clones/01-sygma-media, …) — UNCHANGED     │
│  until an approved publish promotes build output                │
└───────────────────────────────────────────────────────────────┘
```

## Multi-tenancy

- **Agency** (`agencies`) — your organization.
- **Client** (`clients`) — business customer; belongs to one agency.
- **Website** (`websites`) — one static site root + CF project metadata.
- Every `content_documents`, `media_assets`, `publish_jobs`, `audit_logs` row has `website_id`.
- API resolves tenant from JWT claims; **never** from client-supplied `website_id` alone without membership check.

## Content model (single source of truth)

Structured documents keyed by `(website_id, doc_type, doc_key)`:

| doc_type | Examples |
|----------|----------|
| `site_settings` | phone, email, WhatsApp, social, address |
| `navigation` | header/footer link groups |
| `page` | home, about, contact field maps |
| `service` | slug, title, description, price label |
| `case_study` | slug, stats, copy blocks |
| `faq` | question/answer pairs |
| `pricing` | tiers / amounts |
| `blog_post` | title, body MDX/HTML, SEO, featured media |
| `seo` | per-route overrides |

**Revisions**: `content_revisions` stores JSON payload + status (`draft` | `published`).

**Publishing** merges published revisions → publisher manifest → patches static HTML/JSON-LD (Phase 4 expands coverage).

## Security

- Roles: `agency_super_admin`, `agency_staff`, `client_owner`, `client_editor`.
- Password hashing: bcrypt.
- Audit log on login, content save, publish, media delete.
- Preview URLs: signed tokens, short TTL, website-scoped.

## What is NOT in Phase 1

- Live Cloudflare deploy (requires tokens — structure only).
- Full 296-page regeneration (inventory + homepage pilot schema only).
- Replacing `index-C7q3mmBk.js` blog array (Phase 4).

## Repository layout

```
docs/platform/          — architecture, env, checkpoints
platform/api/           — FastAPI application
platform/dashboard/     — Agency + client UI
platform/publisher/     — build & deploy jobs
platform/schemas/       — JSON Schema for content types
web-clones/01-sygma-media/ — untouched live static site
```
