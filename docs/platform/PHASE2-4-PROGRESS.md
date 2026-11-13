# Phases 2–4 progress (in flight)

**Live production site:** still untouched  
**Cloudflare deploy:** not enabled  

## Phase 2 — Agency dashboard

| Item | Status |
|------|--------|
| Add client (UI + API) | Done |
| Register website (UI + API) | Done |
| Invite client user (UI + API) | Done |
| Publishing monitor (all sites) | Done |
| Audit log API | Done (website-scoped events) |
| Disable client editing (API toggle) | Pending |

## Phase 3 — Client dashboard

| Item | Status |
|------|--------|
| Website workspace tabs | Done |
| Homepage editor | Done |
| Contact / site settings | Done |
| Media upload (local) | Done |
| Page manager (curated list) | Done |
| Publish + preview tab | Done (JWT query preview) |
| Blog editor | Not started |

## Phase 4 — Sygma integration

| Item | Status |
|------|--------|
| Bootstrap CMS from live hero/SEO/contact | Done |
| HTML patch: `index.html` hero + meta | Done |
| HTML patch: `contact/index.html` JSON-LD (partial) | Done |
| Bundle `index-*.js` sync | Not started |
| Full route coverage | Not started |

## Tests

Run: `cd platform/api && pytest -q` (includes `test_html_patch.py`)

## Next atomic work

1. Blog post schema + editor (slug preserve).  
2. Image logical_key → path map for replace-in-HTML.  
3. Cloudflare staging deploy adapter (owner credentials).  
4. `client_editing_enabled` toggle in agency UI.
