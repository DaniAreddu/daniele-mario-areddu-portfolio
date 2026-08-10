"""Application settings, loaded from environment variables / .env."""

from functools import lru_cache
from typing import Annotated

from pydantic import EmailStr, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General
    environment: str = "development"
    app_name: str = "Areddu Portfolio API"
    api_v1_prefix: str = "/api/v1"
    log_level: str = "INFO"
    log_json: bool = False

    # Docs (configurable so they can be disabled/restricted in production)
    docs_enabled: bool = True
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    openapi_url: str = "/openapi.json"

    # Database
    database_url: str = "postgresql+asyncpg://portfolio:portfolio@localhost:5432/portfolio"
    db_echo: bool = False
    db_pool_size: int = 5
    db_max_overflow: int = 10

    # CORS
    cors_origins: Annotated[list[str], NoDecode] = [
        "http://localhost:5173",
        "http://localhost:8080",
    ]

    # Trusted proxy / hosts
    trusted_hosts: Annotated[list[str], NoDecode] = ["*"]

    # Contact / SMTP
    contact_recipient_email: EmailStr = "danielemario@areddu.it"
    smtp_host: str = "localhost"
    smtp_port: int = 1025
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_use_tls: bool = False
    smtp_sender: str = "no-reply@areddu.it"
    smtp_configured_explicitly: bool = False

    # Abuse protection
    contact_rate_limit_per_hour: int = 5

    # Public site
    public_site_url: str = "http://localhost:5173"

    default_locale: str = "en"
    supported_locales: Annotated[list[str], NoDecode] = ["en", "it"]

    # Admin / CMS authentication
    admin_session_cookie_name: str = "admin_session"
    admin_session_ttl_hours: int = 12
    admin_mfa_pending_ttl_minutes: int = 10
    admin_login_rate_limit_per_hour: int = 10
    admin_totp_rate_limit_per_10_minutes: int = 8
    # Fernet key protecting TOTP secrets at rest. The default is a fixed,
    # published dev-only key — generate a real one for any non-dev deployment:
    #   python -c "from cryptography.fernet import Fernet as F; print(F.generate_key().decode())"
    admin_totp_encryption_key: str = "fGh_Xp7R2VXN4o-pnC2FE6B7MFIPEhqTIsQGVfujB74="

    @field_validator("cors_origins", "trusted_hosts", "supported_locales", mode="before")
    @classmethod
    def _split_csv(cls, value: object) -> object:
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @property
    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
