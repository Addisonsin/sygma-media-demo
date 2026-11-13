# Web clones (Sygma LLC)

Multiple static site mirrors / rebrands live side by side. Each folder is one **option** you can run, deploy, or hand to a client.

## Projects

| Folder | Site | Local URL | Notes |
|--------|------|-----------|--------|
| [`01-sygma-media`](01-sygma-media/) | Sygma Media LLC (US rebrand of Aesthetic Launch Lab) | http://127.0.0.1:8765/ | **Stable** — mobile nav, services images, `serve.py` routing |
| [`02-social-shepherd`](02-social-shepherd/) | [thesocialshepherd.com](https://thesocialshepherd.com/) → Sygma rebrand | http://127.0.0.1:8766/ | **Saved** — see [`CHECKPOINT`](02-social-shepherd/docs/CHECKPOINT-2026-11-12.md) |
| [`02-next-site`](02-next-site/) | *(legacy scaffold)* | — | Placeholder for the next clone |

Legacy path: [`../aesthetic-launch-lab`](../aesthetic-launch-lab) → symlink to `01-sygma-media` (old bookmarks still work).

## Run any project

```bash
cd "/Users/VickyMayo/Downloads/Sygma LLC/web-clones/01-sygma-media"
python3 serve.py
```

Always use **`serve.py`** (not `python -m http.server`) so `/img/` and `/m/` CDN proxy + SPA deep links work.

## Add a new clone (`02-next-site`, `03-…`)

1. Copy the upstream static export (or duplicate `01-sygma-media` as a starting point) into a new numbered folder.
2. Run rebrand scripts from that folder’s README (if copied from Sygma Media).
3. Set a **unique port** in `serve.py` if you run two sites at once (e.g. `8765` vs `8766`).
4. Add a row to the table above.

Detailed checklist: [`02-next-site/README.md`](02-next-site/README.md).

## Saved state (Sygma Media)

Checkpoint: [`01-sygma-media/docs/CHECKPOINT-2026-11-12.md`](01-sygma-media/docs/CHECKPOINT-2026-11-12.md).
