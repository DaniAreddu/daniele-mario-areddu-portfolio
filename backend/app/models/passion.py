from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Passion(Base, TimestampMixin):
    __tablename__ = "passion"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True, nullable=False)
    title_en: Mapped[str] = mapped_column(String(160), nullable=False)
    title_it: Mapped[str] = mapped_column(String(160), nullable=False)
    text_en: Mapped[str] = mapped_column(Text, nullable=False)
    text_it: Mapped[str] = mapped_column(Text, nullable=False)
    # Optional editorial detail, e.g. a coordinate pair or route label shown as a visual motif.
    motif_label: Mapped[str | None] = mapped_column(String(160), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
