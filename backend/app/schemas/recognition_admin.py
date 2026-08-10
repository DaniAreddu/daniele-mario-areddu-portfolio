from __future__ import annotations

from datetime import date, datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel

RecognitionKind = Literal["certification", "award", "recognition", "publication"]


class RecognitionAdminWrite(BaseModel):
    kind: RecognitionKind
    title_en: str = Field(min_length=1, max_length=255)
    title_it: str = ""
    issuer: str | None = None
    description_en: str | None = None
    description_it: str | None = None
    date_awarded: date | None = None
    url: str | None = None
    sort_order: int = 0
    internal_notes: str | None = None

    @field_validator("url")
    @classmethod
    def _validate_url(cls, value: str | None) -> str | None:
        if value and not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return value


class RecognitionAdminOut(ORMModel):
    id: int
    kind: str
    title_en: str
    title_it: str
    issuer: str | None
    description_en: str | None
    description_it: str | None
    date_awarded: date | None
    url: str | None
    sort_order: int
    internal_notes: str | None
    publication_status: str
    publish_at: datetime | None
    unpublish_at: datetime | None
    published_at: datetime | None
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class RecognitionListItemAdminOut(ORMModel):
    id: int
    kind: str
    title_en: str
    sort_order: int
    publication_status: str
    deleted_at: datetime | None


class RecognitionRevisionOut(ORMModel):
    id: int
    schema_version: int
    snapshot: dict[str, Any]
    created_at: datetime
    created_by_email: str | None
