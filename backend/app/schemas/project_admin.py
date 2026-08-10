from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator

from app.schemas.common import ORMModel


class ProjectAdminWriteBase(BaseModel):
    title_en: str = Field(min_length=1, max_length=200)
    title_it: str = ""
    summary_en: str = ""
    summary_it: str = ""
    problem_en: str = ""
    problem_it: str = ""
    challenge_en: str = ""
    challenge_it: str = ""
    approach_en: str = ""
    approach_it: str = ""
    architecture_en: str = ""
    architecture_it: str = ""
    key_decisions_en: list[str] = Field(default_factory=list)
    key_decisions_it: list[str] = Field(default_factory=list)
    outcome_en: str = ""
    outcome_it: str = ""
    lessons_en: str = ""
    lessons_it: str = ""
    confidentiality_note_en: str = ""
    confidentiality_note_it: str = ""
    external_url: str | None = None
    cover_image_url: str | None = None
    is_featured: bool = False
    sort_order: int = 0
    internal_notes: str | None = None
    tag_labels: list[str] = Field(default_factory=list)

    @field_validator("external_url", "cover_image_url")
    @classmethod
    def _validate_url(cls, value: str | None) -> str | None:
        if value and not (value.startswith("http://") or value.startswith("https://")):
            raise ValueError("URL must start with http:// or https://")
        return value


class ProjectAdminCreate(ProjectAdminWriteBase):
    slug: str = Field(min_length=1, max_length=140, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


class ProjectAdminUpdate(ProjectAdminWriteBase):
    pass


class ProjectAdminOut(ORMModel):
    id: int
    slug: str
    title_en: str
    title_it: str
    summary_en: str
    summary_it: str
    problem_en: str
    problem_it: str
    challenge_en: str
    challenge_it: str
    approach_en: str
    approach_it: str
    architecture_en: str
    architecture_it: str
    key_decisions_en: list[str]
    key_decisions_it: list[str]
    outcome_en: str
    outcome_it: str
    lessons_en: str
    lessons_it: str
    confidentiality_note_en: str
    confidentiality_note_it: str
    external_url: str | None
    cover_image_url: str | None
    is_featured: bool
    sort_order: int
    internal_notes: str | None
    tags: list[str]
    related_skills: list[str]
    publication_status: str
    publish_at: datetime | None
    unpublish_at: datetime | None
    published_at: datetime | None
    deleted_at: datetime | None
    created_at: datetime
    updated_at: datetime


class ProjectListItemAdminOut(ORMModel):
    id: int
    slug: str
    title_en: str
    is_featured: bool
    sort_order: int
    publication_status: str
    deleted_at: datetime | None


class ProjectRevisionOut(ORMModel):
    id: int
    schema_version: int
    snapshot: dict[str, Any]
    created_at: datetime
    created_by_email: str | None
