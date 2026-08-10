from __future__ import annotations

from sqlalchemy import JSON, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, PublishableMixin, SoftDeleteMixin, TimestampMixin
from app.models.tag import Tag, project_tag


class Project(TimestampMixin, PublishableMixin, SoftDeleteMixin, Base):
    __tablename__ = "project"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(140), unique=True, index=True, nullable=False)
    title_en: Mapped[str] = mapped_column(String(200), nullable=False)
    title_it: Mapped[str] = mapped_column(String(200), nullable=False)
    summary_en: Mapped[str] = mapped_column(Text, nullable=False)
    summary_it: Mapped[str] = mapped_column(Text, nullable=False)
    problem_en: Mapped[str] = mapped_column(Text, nullable=False)
    problem_it: Mapped[str] = mapped_column(Text, nullable=False)
    challenge_en: Mapped[str] = mapped_column(Text, nullable=False)
    challenge_it: Mapped[str] = mapped_column(Text, nullable=False)
    approach_en: Mapped[str] = mapped_column(Text, nullable=False)
    approach_it: Mapped[str] = mapped_column(Text, nullable=False)
    architecture_en: Mapped[str] = mapped_column(Text, nullable=False)
    architecture_it: Mapped[str] = mapped_column(Text, nullable=False)
    key_decisions_en: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    key_decisions_it: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    outcome_en: Mapped[str] = mapped_column(Text, nullable=False)
    outcome_it: Mapped[str] = mapped_column(Text, nullable=False)
    lessons_en: Mapped[str] = mapped_column(Text, nullable=False)
    lessons_it: Mapped[str] = mapped_column(Text, nullable=False)
    confidentiality_note_en: Mapped[str] = mapped_column(Text, nullable=False)
    confidentiality_note_it: Mapped[str] = mapped_column(Text, nullable=False)
    # Deprecated as the authoritative source (superseded by `tags`, shared
    # with Event via the same Tag vocabulary) but kept, unread by new code
    # paths once tags exist, purely so the one-time migration can normalize
    # existing data without a risky hard cutover — see event.py's `topics`.
    technologies: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    # Only rendered when present; never guessed.
    external_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_featured: Mapped[bool] = mapped_column(default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    # Admin-only — never serialized in any public schema.
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    skills: Mapped[list[ProjectSkill]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    tags: Mapped[list[Tag]] = relationship(secondary=project_tag, order_by="Tag.label")


class ProjectSkill(Base):
    __tablename__ = "project_skill"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), nullable=False)
    skill_name: Mapped[str] = mapped_column(String(120), nullable=False)

    project: Mapped[Project] = relationship(back_populates="skills")
