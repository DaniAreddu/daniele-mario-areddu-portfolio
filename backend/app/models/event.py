from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.talk import Talk


class Event(Base, TimestampMixin):
    """A single speaking engagement (conference, meetup, workshop...)."""

    __tablename__ = "event"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)

    event_name: Mapped[str] = mapped_column(String(200), nullable=False)
    talk_id: Mapped[int | None] = mapped_column(ForeignKey("talk.id"), nullable=True)
    session_title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    short_description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    short_description_it: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    full_description_it: Mapped[str | None] = mapped_column(Text, nullable=True)

    start_date: Mapped[date | None] = mapped_column(Date, nullable=True, index=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    # Many real engagements are only known to the month ("September 2026"),
    # without a confirmed exact day. Kept separate from start_date so partial
    # precision can be represented honestly instead of guessing a day.
    month: Mapped[int | None] = mapped_column(Integer, nullable=True)

    city: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    country: Mapped[str | None] = mapped_column(String(120), nullable=True, index=True)
    continent: Mapped[str | None] = mapped_column(String(60), nullable=True, index=True)
    latitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    longitude: Mapped[float | None] = mapped_column(Float, nullable=True)
    venue: Mapped[str | None] = mapped_column(String(200), nullable=True)

    format: Mapped[str] = mapped_column(String(40), nullable=False, default="conference")
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    topics: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)

    event_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    slides_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    recording_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image: Mapped[str | None] = mapped_column(String(255), nullable=True)

    status: Mapped[str] = mapped_column(String(20), nullable=False, default="confirmed")
    sessions_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    # A small, deliberately curated subset of "featured" — major geographic
    # expansion moments (first talk in a new country/region) rather than
    # talks with especially notable session content.
    is_international_milestone: Mapped[bool] = mapped_column(Boolean, default=False)

    talk: Mapped[Talk | None] = relationship(back_populates="events")

    @property
    def has_coordinates(self) -> bool:
        return self.latitude is not None and self.longitude is not None
