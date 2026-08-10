from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel


class CommunityActivityAdminWrite(BaseModel):
    slug: str = Field(min_length=1, max_length=140, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    title_en: str = Field(min_length=1, max_length=200)
    title_it: str = ""
    description_en: str = ""
    description_it: str = ""
    activity_date: date | None = None
    activity_type: str = "meetup"
    url: str | None = None
    logo_media_url: str | None = None
    is_featured: bool = False
    sort_order: int = 0
    internal_notes: str | None = None

    @field_validator("url")
    @classmethod
    def _validate_url(cls, value: str | None) -> str | None:
        if value and not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return value


class CommunityActivityAdminOut(ORMModel):
    id: int
    slug: str
    title_en: str
    title_it: str
    description_en: str
    description_it: str
    activity_date: date | None
    activity_type: str
    url: str | None
    logo_media_url: str | None
    is_featured: bool
    sort_order: int
    internal_notes: str | None
    publication_status: str
    publish_at: datetime | None
    unpublish_at: datetime | None
    published_at: datetime | None
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class CommunityActivityListItemAdminOut(ORMModel):
    id: int
    slug: str
    title_en: str
    activity_type: str
    sort_order: int
    publication_status: str
    deleted_at: datetime | None


class CommunityActivityRevisionOut(ORMModel):
    id: int
    schema_version: int
    snapshot: dict[str, Any]
    created_at: datetime
    created_by_email: str | None


class CommunityProfileAdminWrite(BaseModel):
    name: str = "Velletri.dev"
    role_en: str = ""
    role_it: str = ""
    mission_en: str = ""
    mission_it: str = ""
    description_en: str = ""
    description_it: str = ""
    vision_en: str = ""
    vision_it: str = ""
    collaboration_en: str = ""
    collaboration_it: str = ""
    founded_year: int = 2023
    website_url: str | None = None


class CommunityProfileAdminOut(ORMModel):
    id: int
    name: str
    role_en: str
    role_it: str
    mission_en: str
    mission_it: str
    description_en: str
    description_it: str
    vision_en: str
    vision_it: str
    collaboration_en: str
    collaboration_it: str
    founded_year: int
    website_url: str | None
    created_at: datetime
    updated_at: datetime
