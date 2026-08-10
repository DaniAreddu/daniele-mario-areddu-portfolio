from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel


class ExperienceAdminWrite(BaseModel):
    organization: str = Field(min_length=1, max_length=200)
    role_en: str = Field(min_length=1, max_length=200)
    role_it: str = ""
    employment_type: str | None = None
    location: str = ""
    location_mode: str | None = None
    start_date: date
    end_date: date | None = None
    is_current: bool = False
    summary_en: str = ""
    summary_it: str = ""
    long_description_en: str | None = None
    long_description_it: str | None = None
    highlights_en: list[str] = Field(default_factory=list)
    highlights_it: list[str] = Field(default_factory=list)
    achievements_en: list[str] = Field(default_factory=list)
    achievements_it: list[str] = Field(default_factory=list)
    company_url: str | None = None
    logo_media_url: str | None = None
    is_featured: bool = False
    sort_order: int = 0
    internal_notes: str | None = None
    tag_labels: list[str] = Field(default_factory=list)

    @field_validator("company_url")
    @classmethod
    def _validate_url(cls, value: str | None) -> str | None:
        if value and not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return value


class ExperienceAdminOut(ORMModel):
    id: int
    organization: str
    role_en: str
    role_it: str
    employment_type: str | None
    location: str
    location_mode: str | None
    start_date: date
    end_date: date | None
    is_current: bool
    summary_en: str
    summary_it: str
    long_description_en: str | None
    long_description_it: str | None
    highlights_en: list[str]
    highlights_it: list[str]
    achievements_en: list[str]
    achievements_it: list[str]
    company_url: str | None
    logo_media_url: str | None
    is_featured: bool
    sort_order: int
    internal_notes: str | None
    tags: list[str]
    publication_status: str
    publish_at: datetime | None
    unpublish_at: datetime | None
    published_at: datetime | None
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ExperienceListItemAdminOut(ORMModel):
    id: int
    organization: str
    role_en: str
    is_current: bool
    sort_order: int
    publication_status: str
    deleted_at: datetime | None


class ExperienceRevisionOut(ORMModel):
    id: int
    schema_version: int
    snapshot: dict[str, Any]
    created_at: datetime
    created_by_email: str | None
