from __future__ import annotations

from sqlalchemy import JSON, Boolean, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, PublishableMixin, SoftDeleteMixin, TimestampMixin
from app.models.tag import Tag, experience_tag


class Experience(TimestampMixin, PublishableMixin, SoftDeleteMixin, Base):
    __tablename__ = "experience"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization: Mapped[str] = mapped_column(String(200), nullable=False)
    role_en: Mapped[str] = mapped_column(String(200), nullable=False)
    role_it: Mapped[str] = mapped_column(String(200), nullable=False)
    employment_type: Mapped[str | None] = mapped_column(String(40), nullable=True)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    location_mode: Mapped[str | None] = mapped_column(String(20), nullable=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    summary_en: Mapped[str] = mapped_column(Text, nullable=False)
    summary_it: Mapped[str] = mapped_column(Text, nullable=False)
    long_description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    long_description_it: Mapped[str | None] = mapped_column(Text, nullable=True)
    highlights_en: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    highlights_it: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    achievements_en: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    achievements_it: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    # Deprecated as the authoritative source (superseded by `tags`) — kept
    # only so the one-time migration can normalize existing data, matching
    # the Event.topics / Project.technologies pattern.
    technologies: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    company_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logo_media_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(default=0)
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)

    tags: Mapped[list[Tag]] = relationship(secondary=experience_tag, order_by="Tag.label")
