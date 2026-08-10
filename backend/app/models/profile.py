"""Singleton profile + biography variants."""

from __future__ import annotations

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Profile(Base, TimestampMixin):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    roles: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    base_country: Mapped[str] = mapped_column(String(80), nullable=False)
    availability_en: Mapped[str] = mapped_column(Text, nullable=False)
    availability_it: Mapped[str] = mapped_column(Text, nullable=False)
    tagline_en: Mapped[str] = mapped_column(Text, nullable=False)
    tagline_it: Mapped[str] = mapped_column(Text, nullable=False)
    positioning_statement_en: Mapped[str] = mapped_column(Text, nullable=False)
    positioning_statement_it: Mapped[str] = mapped_column(Text, nullable=False)
    brand_label: Mapped[str] = mapped_column(String(80), nullable=False)
    public_email: Mapped[str] = mapped_column(String(255), nullable=False)

    # Verified external links only; null hides the corresponding UI element.
    github_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    sessionize_url: Mapped[str | None] = mapped_column(String(255), nullable=True)

    talks_count_label: Mapped[str] = mapped_column(String(40), nullable=False, default="30+")
    speaking_years_label: Mapped[str] = mapped_column(String(40), nullable=False, default="2")
    speaking_regions_label: Mapped[str] = mapped_column(
        String(160), nullable=False, default="Europe, North America, Central Asia"
    )


class Biography(Base, TimestampMixin):
    __tablename__ = "biography"

    id: Mapped[int] = mapped_column(primary_key=True)
    micro_en: Mapped[str] = mapped_column(Text, nullable=False)
    micro_it: Mapped[str] = mapped_column(Text, nullable=False)
    short_en: Mapped[str] = mapped_column(Text, nullable=False)
    short_it: Mapped[str] = mapped_column(Text, nullable=False)
    medium_en: Mapped[str] = mapped_column(Text, nullable=False)
    medium_it: Mapped[str] = mapped_column(Text, nullable=False)
    long_en: Mapped[str] = mapped_column(Text, nullable=False)
    long_it: Mapped[str] = mapped_column(Text, nullable=False)
    speaker_bio_en: Mapped[str] = mapped_column(Text, nullable=False)
    speaker_bio_it: Mapped[str] = mapped_column(Text, nullable=False)
