from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.admin_user import AdminUser


class Revision(TimestampMixin, Base):
    """A point-in-time snapshot of one revisable entity's scalar column
    values, taken immediately before an update is applied. Generic across
    every content type — ``entity_type``/``entity_id`` identify what it
    belongs to, the same pattern as ``AuditEvent``.

    Relationships are never snapshotted (see
    app.services._admin_common.snapshot_entity) — only plain columns.
    ``schema_version`` lets a future restore detect when a snapshot predates
    a breaking model change instead of failing silently.
    """

    __tablename__ = "revision"

    id: Mapped[int] = mapped_column(primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(50), index=True)
    entity_id: Mapped[int] = mapped_column(Integer, index=True)
    schema_version: Mapped[int] = mapped_column(Integer, default=1, server_default="1")
    snapshot: Mapped[dict[str, Any]] = mapped_column(JSON)
    created_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("admin_user.id", ondelete="SET NULL"), nullable=True
    )

    created_by: Mapped[AdminUser | None] = relationship()
