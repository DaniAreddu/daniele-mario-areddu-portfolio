from __future__ import annotations

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Education(Base, TimestampMixin):
    __tablename__ = "education"

    id: Mapped[int] = mapped_column(primary_key=True)
    institution: Mapped[str] = mapped_column(String(200), nullable=False)
    degree_en: Mapped[str] = mapped_column(String(200), nullable=False)
    degree_it: Mapped[str] = mapped_column(String(200), nullable=False)
    location: Mapped[str] = mapped_column(String(120), nullable=False)
    start_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    end_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    is_ongoing: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_it: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
