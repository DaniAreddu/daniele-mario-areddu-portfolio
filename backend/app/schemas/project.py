from __future__ import annotations

from app.schemas.common import ORMModel


class ProjectListItemOut(ORMModel):
    slug: str
    title: str
    summary: str
    technologies: list[str]
    is_featured: bool
    external_url: str | None


class ProjectDetailOut(ORMModel):
    slug: str
    title: str
    summary: str
    problem: str
    challenge: str
    approach: str
    architecture: str
    key_decisions: list[str]
    outcome: str
    lessons: str
    confidentiality_note: str
    technologies: list[str]
    related_skills: list[str]
    external_url: str | None
    is_featured: bool
