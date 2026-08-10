"""Declarative base and shared column mixins."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class PublishableMixin:
    """Adds a CMS publication lifecycle independent of any domain-specific
    status a model may already have (e.g. ``Event.status``). A plain string
    column, not a DB enum, matching this codebase's existing convention for
    status-like fields — adding a new value never requires an ``ALTER TYPE``.

    Values: ``DRAFT`` (default), ``SCHEDULED``, ``PUBLISHED``, ``ARCHIVED``.
    Apply ``app.db.filters.visible_now()`` in every public-facing repository
    query against a model using this mixin.
    """

    publication_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="DRAFT", server_default="DRAFT"
    )
    publish_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    unpublish_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # Set once, the first time an item actually goes live — distinct from
    # publish_at (the scheduled target), kept for display/audit purposes.
    published_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class SoftDeleteMixin:
    """A nullable ``deleted_at`` timestamp — content is trashed, not
    immediately destroyed. Permanent deletion is a separate, explicit
    operation requiring the row to already be trashed.
    """

    deleted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
