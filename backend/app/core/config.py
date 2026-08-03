"""Application configuration — the single source of truth for all settings."""
from functools import lru_cache
from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "CareCode API"
    environment: str = "development"
    secret_key: str = "change-me"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    reset_token_expire_minutes: int = 30

    database_url: str = "sqlite:///./carecode.db"
    frontend_url: str = "http://localhost:5173"
    public_base_url: str = ""
    storage_dir: str = "./storage"

    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_from_name: str = "CareCode"
    smtp_from_email: str = "noreply@carecode.example"
    smtp_use_tls: bool = True

    rate_limit_enabled: bool = True

    # -- helpers -----------------------------------------------------------
    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"

    @property
    def smtp_configured(self) -> bool:
        return bool(self.smtp_host and self.smtp_user and self.smtp_password)

    @property
    def public_url(self) -> str:
        return self.public_base_url.rstrip("/") if self.public_base_url else ""

    @property
    def storage_path(self) -> Path:
        path = Path(self.storage_dir)
        path.mkdir(parents=True, exist_ok=True)
        return path

    @field_validator("frontend_url", "public_base_url", "storage_dir", mode="before")
    @classmethod
    def strip_value(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("database_url", mode="before")
    @classmethod
    def fallback_database(cls, v):
        return v.strip() if isinstance(v, str) and v.strip() else "sqlite:///./carecode.db"


@lru_cache
def get_settings() -> Settings:
    return Settings()
