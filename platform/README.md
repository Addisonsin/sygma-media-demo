# Sygma Site Platform (multi-client CMS)

Isolated from `web-clones/01-sygma-media` — does **not** modify the live static site until you approve a production publish.

## Local development

### API

```bash
cd platform/api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export STATIC_SITE_ROOT="$(cd ../../web-clones/01-sygma-media && pwd)"
uvicorn app.main:app --reload --port 8000
```

Default bootstrap admin: see `docs/platform/ENV.md`.

### Dashboard

```bash
cd platform/dashboard
npm install
npm run dev
```

Open http://localhost:5173 — API proxied to :8000.

### Tests

```bash
cd platform/api
source .venv/bin/activate
export STATIC_SITE_ROOT="$(cd ../../web-clones/01-sygma-media && pwd)"
pytest -q
```

### Content inventory

```bash
python3 platform/scripts/inventory_sygma_content.py
```

## Phase status

| Phase | Status |
|-------|--------|
| 1 Foundation | Done |
| 2 Agency dashboard | Done (UI + publish monitor) |
| 3 Client dashboard | In progress — workspace, media, preview |
| 4 Sygma integration | In progress — homepage + contact HTML patch |
| 5 Testing | 8 API tests |
| 6 Docs | Architecture + ENV |

**External systems touched:** NO (no Cloudflare deploy, no production DB).
