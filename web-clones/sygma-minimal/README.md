# Sygma Media — minimal agency build

Generated from `01-sygma-media` without modifying the full site.

- **HTML routes:** 16 (was ~296)
- **Blog:** retired (301 → /services/, not in sitemap)
  - **Portfolio / case study pages:** 8 static (before/after charts, no React)
- **Live production:** not deployed until you approve `wrangler pages deploy`

## Preview locally

```bash
cd web-clones/sygma-minimal && python3 -m http.server 8790
```

## Deploy preview (separate Pages project)

```bash
npx wrangler pages deploy . --project-name=sygma-minimal
```
