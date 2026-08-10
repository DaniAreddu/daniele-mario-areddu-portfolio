from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import JSON, Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin

if TYPE_CHECKING:
    from app.models.event import Event


class Talk(Base, TimestampMixin):
    """A reusable talk/session title, potentially delivered at several events."""

    __tablename__ = "talk"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    language: Mapped[str] = mapped_column(String(10), nullable=False, default="en")
    summary_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    summary_it: Mapped[str | None] = mapped_column(Text, nullable=True)
    topics: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)

    events: Mapped[list[Event]] = relationship(back_populates="talk")
