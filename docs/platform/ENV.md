# Platform environment variables

Copy to `platform/api/.env` for local development. **Never commit secrets.**

## Required (local dev)

| Variable | Example | Purpose |
|----------|---------|---------|
| `DATABASE_URL` | `sqlite:///./data/platform.db` | SQLAlchemy URL (Postgres in prod) |
| `JWT_SECRET` | *(random 32+ bytes)* | Sign access tokens |
| `JWT_ACCESS_MINUTES` | `60` | Access token TTL |
| `MEDIA_BACKEND` | `local` | `local` or `r2` |
| `MEDIA_LOCAL_ROOT` | `./data/media` | Per-website subfolders |
| `STATIC_SITE_ROOT` | `../../web-clones/01-sygma-media` | Read-only source for publisher |
| `PUBLISH_OUTPUT_ROOT` | `./data/builds` | Generated artifacts (not live site) |
| `CORS_ORIGINS` | `http://localhost:5173` | Dashboard origin |

## Optional — production

| Variable | Purpose |
|----------|---------|
| `CLOUDFLARE_API_TOKEN` | Pages direct upload deploy |
| `CLOUDFLARE_ACCOUNT_ID` | Account for Pages |
| `CLOUDFLARE_PAGES_PROJECT` | e.g. `sygma-media` |
| `R2_ACCOUNT_ID` | Media storage |
| `R2_ACCESS_KEY_ID` | S3-compatible key |
| `R2_SECRET_ACCESS_KEY` | S3-compatible secret |
| `R2_BUCKET` | Bucket name |
| `R2_PUBLIC_BASE_URL` | CDN URL prefix for media |
| `PREVIEW_BASE_URL` | e.g. `https://preview.sygmamedia.com` |

## Bootstrap admin (dev only)

| Variable | Purpose |
|----------|---------|
| `BOOTSTRAP_AGENCY_NAME` | Default agency label |
| `BOOTSTRAP_ADMIN_EMAIL` | First super-admin (use a valid domain, e.g. `@sygma.test`) |
| `BOOTSTRAP_ADMIN_PASSWORD` | **Change immediately** |

Without Cloudflare/R2 variables, **publish and R2 upload endpoints return structured `503 CONFIG_MISSING`** — not fake success.
