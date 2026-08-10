from __future__ import annotations

from sqlalchemy import JSON, Boolean, Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Experience(Base, TimestampMixin):
    __tablename__ = "experience"

    id: Mapped[int] = mapped_column(primary_key=True)
    organization: Mapped[str] = mapped_column(String(200), nullable=False)
    role_en: Mapped[str] = mapped_column(String(200), nullable=False)
    role_it: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date | None] = mapped_column(Date, nullable=True)
    is_current: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    summary_en: Mapped[str] = mapped_column(Text, nullable=False)
    summary_it: Mapped[str] = mapped_column(Text, nullable=False)
    highlights_en: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    highlights_it: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    technologies: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    sort_order: Mapped[int] = mapped_column(default=0)
