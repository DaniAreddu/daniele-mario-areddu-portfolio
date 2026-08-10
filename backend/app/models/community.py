from __future__ import annotations

from datetime import date

from sqlalchemy import Boolean, Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, PublishableMixin, SoftDeleteMixin, TimestampMixin


class CommunityProfile(Base, TimestampMixin):
    """Singleton row describing Velletri.dev as an initiative."""

    __tablename__ = "community_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False, default="Velletri.dev")
    role_en: Mapped[str] = mapped_column(String(120), nullable=False)
    role_it: Mapped[str] = mapped_column(String(120), nullable=False)
    mission_en: Mapped[str] = mapped_column(Text, nullable=False)
    mission_it: Mapped[str] = mapped_column(Text, nullable=False)
    description_en: Mapped[str] = mapped_column(Text, nullable=False)
    description_it: Mapped[str] = mapped_column(Text, nullable=False)
    vision_en: Mapped[str] = mapped_column(Text, nullable=False)
    vision_it: Mapped[str] = mapped_column(Text, nullable=False)
    collaboration_en: Mapped[str] = mapped_column(Text, nullable=False)
    collaboration_it: Mapped[str] = mapped_column(Text, nullable=False)
    founded_year: Mapped[int] = mapped_column(Integer, nullable=False)
    website_url: Mapped[str | None] = mapped_column(String(255), nullable=True)


class CommunityActivity(TimestampMixin, PublishableMixin, SoftDeleteMixin, Base):
    __tablename__ = "community_activity"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(140), unique=True, index=True, nullable=False)
    title_en: Mapped[str] = mapped_column(String(200), nullable=False)
    title_it: Mapped[str] = mapped_column(String(200), nullable=False)
    description_en: Mapped[str] = mapped_column(Text, nullable=False)
    description_it: Mapped[str] = mapped_column(Text, nullable=False)
    activity_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    activity_type: Mapped[str] = mapped_column(String(40), nullable=False, default="meetup")
    url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    logo_media_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
