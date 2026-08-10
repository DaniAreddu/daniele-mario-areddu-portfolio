from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel


class EducationAdminWrite(BaseModel):
    institution: str = Field(min_length=1, max_length=200)
    degree_en: str = Field(min_length=1, max_length=200)
    degree_it: str = ""
    field: str | None = None
    location: str = ""
    start_year: int | None = Field(default=None, ge=1950, le=2100)
    end_year: int | None = Field(default=None, ge=1950, le=2100)
    is_ongoing: bool = False
    description_en: str | None = None
    description_it: str | None = None
    activities: list[str] = Field(default_factory=list)
    url: str | None = None
    logo_media_url: str | None = None
    sort_order: int = 0
    internal_notes: str | None = None

    @field_validator("url")
    @classmethod
    def _validate_url(cls, value: str | None) -> str | None:
        if value and not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return value


class EducationAdminOut(ORMModel):
    id: int
    institution: str
    degree_en: str
    degree_it: str
    field: str | None
    location: str
    start_year: int | None
    end_year: int | None
    is_ongoing: bool
    description_en: str | None
    description_it: str | None
    activities: list[str]
    url: str | None
    logo_media_url: str | None
    sort_order: int
    internal_notes: str | None
    publication_status: str
    publish_at: datetime | None
    unpublish_at: datetime | None
    published_at: datetime | None
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class EducationListItemAdminOut(ORMModel):
    id: int
    institution: str
    degree_en: str
    sort_order: int
    publication_status: str
    deleted_at: datetime | None


class EducationRevisionOut(ORMModel):
    id: int
    schema_version: int
    snapshot: dict[str, Any]
    created_at: datetime
    created_by_email: str | None
