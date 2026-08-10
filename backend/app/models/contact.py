from __future__ import annotations

from sqlalchemy import Boolean, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class ContactSubmission(Base, TimestampMixin):
    """Stores contact requests. Never exposed via a public read endpoint."""

    __tablename__ = "contact_submission"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    organization: Mapped[str | None] = mapped_column(String(200), nullable=True)
    request_type: Mapped[str] = mapped_column(String(40), nullable=False)
    event_or_project: Mapped[str | None] = mapped_column(String(200), nullable=True)
    indicative_date: Mapped[str | None] = mapped_column(String(80), nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    consent_given: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    source_ip_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    email_delivered: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
