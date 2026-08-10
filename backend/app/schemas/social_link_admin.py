from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel

# Kept intentionally small and explicit — the icon name is rendered by
# looking up a lucide-react component on the frontend, so an unrecognized
# value must never reach the client unvalidated.
ALLOWED_ICONS = {
    "github",
    "linkedin",
    "twitter",
    "mastodon",
    "youtube",
    "instagram",
    "rss",
    "mail",
    "globe",
    "sessionize",
}


class SocialLinkAdminWrite(BaseModel):
    label: str = Field(min_length=1, max_length=80)
    url: str = Field(min_length=1, max_length=500)
    icon: str | None = None
    enabled: bool = True
    sort_order: int = 0

    @field_validator("url")
    @classmethod
    def _validate_url(cls, value: str) -> str:
        allowed_prefixes = ("http://", "https://", "mailto:")
        if not value.startswith(allowed_prefixes):
            raise ValueError("URL must start with http://, https://, or mailto:")
        return value

    @field_validator("icon")
    @classmethod
    def _validate_icon(cls, value: str | None) -> str | None:
        if value and value not in ALLOWED_ICONS:
            raise ValueError(f"Unknown icon '{value}'. Allowed: {', '.join(sorted(ALLOWED_ICONS))}")
        return value


class SocialLinkAdminOut(ORMModel):
    id: int
    label: str
    url: str
    icon: str | None
    enabled: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
