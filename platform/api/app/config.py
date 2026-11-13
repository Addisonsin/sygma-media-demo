from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    database_url: str = "sqlite:///./data/platform.db"
    jwt_secret: str = "dev-only-change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_minutes: int = 60

    media_backend: str = "local"
    media_local_root: Path = Path("./data/media")
    static_site_root: Path = Path("../../web-clones/01-sygma-media")
    publish_output_root: Path = Path("./data/builds")
    schema_root: Path = Path("../../platform/schemas/v1")
    static_ui_root: Path = Path("./static_ui")

    cors_origins: str = "http://localhost:5173,http://localhost:4173,http://127.0.0.1:5173"

    bootstrap_agency_name: str = "Sygma LLC"
    bootstrap_admin_email: str = "admin@example.com"
    bootstrap_admin_password: str = "ChangeMeNow!"

    cloudflare_api_token: Optional[str] = None
    cloudflare_account_id: Optional[str] = None
    cloudflare_pages_project: Optional[str] = None

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def cf_configured(self) -> bool:
        return bool(
            self.cloudflare_api_token and self.cloudflare_account_id and self.cloudflare_pages_project
        )


settings = Settings()
