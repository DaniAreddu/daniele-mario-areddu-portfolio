from __future__ import annotations

from datetime import date as date_type

from sqlalchemy import Date, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, PublishableMixin, SoftDeleteMixin, TimestampMixin


class Recognition(TimestampMixin, PublishableMixin, SoftDeleteMixin, Base):
    """Certifications, awards, recognition, and publications — one table
    with a `kind` discriminator rather than four near-identical tables (they
    share every field that matters: a title, an issuer, an optional date and
    URL). The public site only renders a section once it has at least one
    published entry of that kind.
    """

    __tablename__ = "recognition"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    title_en: Mapped[str] = mapped_column(String(255), nullable=False)
    title_it: Mapped[str] = mapped_column(String(255), nullable=False)
    issuer: Mapped[str | None] = mapped_column(String(200), nullable=True)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_it: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_awarded: Mapped[date_type | None] = mapped_column(Date, nullable=True)
    url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
