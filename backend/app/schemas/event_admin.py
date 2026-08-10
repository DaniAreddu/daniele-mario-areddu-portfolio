from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel


def _validate_url(value: str | None) -> str | None:
    if value and not (value.startswith("http://") or value.startswith("https://")):
        raise ValueError("URL must start with http:// or https://")
    return value


class EventAdminWriteBase(BaseModel):
    """Content fields only — publication_status, publish_at/unpublish_at,
    published_at, and deleted_at are deliberately absent here. Lifecycle
    changes go through their own narrow endpoints (see admin_events.py) so
    this schema can never be used to sneak a publish/delete through the
    generic content-update path (a mass-assignment guard, not an oversight).
    """

    event_name: str = Field(min_length=1, max_length=200)
    talk_id: int | None = None
    session_title: str | None = None
    short_description_en: str | None = None
    short_description_it: str | None = None
    full_description_en: str | None = None
    full_description_it: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    year: int = Field(ge=2000, le=2100)
    month: int | None = Field(default=None, ge=1, le=12)
    city: str | None = None
    country: str | None = None
    continent: str | None = None
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)
    venue: str | None = None
    format: str = "conference"
    language: str = "en"
    event_url: str | None = None
    slides_url: str | None = None
    recording_url: str | None = None
    image: str | None = None
    status: str = "confirmed"
    sessions_count: int = Field(default=1, ge=1)
    is_featured: bool = False
    is_international_milestone: bool = False
    internal_notes: str | None = None
    tag_labels: list[str] = Field(default_factory=list)

    _validate_event_url = field_validator("event_url")(_validate_url)
    _validate_slides_url = field_validator("slides_url")(_validate_url)
    _validate_recording_url = field_validator("recording_url")(_validate_url)
    _validate_image = field_validator("image")(_validate_url)


class EventAdminCreate(EventAdminWriteBase):
    slug: str = Field(min_length=1, max_length=160, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class EventAdminUpdate(EventAdminWriteBase):
    pass


class EventScheduleRequest(BaseModel):
    publish_at: datetime


class EventAdminOut(ORMModel):
    id: int
    slug: str
    event_name: str
    talk_id: int | None
    session_title: str | None
    short_description_en: str | None
    short_description_it: str | None
    full_description_en: str | None
    full_description_it: str | None
    start_date: date | None
    end_date: date | None
    year: int
    month: int | None
    city: str | None
    country: str | None
    continent: str | None
    latitude: float | None
    longitude: float | None
    venue: str | None
    format: str
    language: str
    event_url: str | None
    slides_url: str | None
    recording_url: str | None
    image: str | None
    status: str
    sessions_count: int
    is_featured: bool
    is_international_milestone: bool
    internal_notes: str | None
    tags: list[str]
    publication_status: str
    publish_at: datetime | None
    unpublish_at: datetime | None
    published_at: datetime | None
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class EventListItemOut(ORMModel):
    id: int
    slug: str
    event_name: str
    city: str | None
    country: str | None
    year: int
    month: int | None
    status: str
    publication_status: str
    is_featured: bool
    is_international_milestone: bool
    deleted_at: datetime | None


class DuplicateCandidateOut(BaseModel):
    slug: str
    event_name: str
    city: str | None
    year: int


class RevisionOut(ORMModel):
    id: int
    schema_version: int
    snapshot: dict[str, Any]
    created_at: datetime
    created_by_email: str | None


class RevisionDiffOut(BaseModel):
    current: dict[str, Any]
    snapshot: dict[str, Any]
