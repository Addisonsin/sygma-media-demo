from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.bootstrap import init_db_schema, seed_if_empty
from app.config import settings
from app.db import SessionLocal, engine
from app.routers import agency, auth, content, media, overview, pages, preview, publish, websites


@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db_schema(engine)
    with SessionLocal() as db:
        seed_if_empty(db)
    yield


app = FastAPI(title="Sygma Site Platform API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(agency.router, prefix="/api/v1")
app.include_router(websites.router, prefix="/api/v1")
app.include_router(content.router, prefix="/api/v1")
app.include_router(media.router, prefix="/api/v1")
app.include_router(publish.router, prefix="/api/v1")
app.include_router(pages.router, prefix="/api/v1")
app.include_router(preview.router, prefix="/api/v1")
app.include_router(overview.router, prefix="/api/v1")


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "cf_deploy_configured": settings.cf_configured}


def _mount_dashboard() -> None:
    ui = settings.static_ui_root.resolve()
    if not ui.is_dir():
        return
    assets = ui / "assets"
    if assets.is_dir():
        app.mount("/assets", StaticFiles(directory=assets), name="ui-assets")

    @app.get("/")
    def ui_index() -> FileResponse:
        return FileResponse(ui / "index.html")

    @app.get("/{spa_path:path}")
    def ui_spa(spa_path: str) -> FileResponse:
        if spa_path.startswith("api/") or spa_path == "health":
            raise HTTPException(status_code=404)
        target = ui / spa_path
        if target.is_file():
            return FileResponse(target)
        return FileResponse(ui / "index.html")


_mount_dashboard()
