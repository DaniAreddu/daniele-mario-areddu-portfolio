from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin
from app.models.admin_user import AdminUser


class MediaAsset(TimestampMixin, Base):
    """A single uploaded file. `storage_key` is server-generated
    (uuid4, never derived from the client filename) — see
    app.services.storage for why. `original_filename` is pure display
    metadata and never touches a filesystem path.
    """

    __tablename__ = "media_asset"

    id: Mapped[int] = mapped_column(primary_key=True)
    storage_key: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    original_filename: Mapped[str] = mapped_column(String(255))
    mime_type: Mapped[str] = mapped_column(String(100))
    size_bytes: Mapped[int] = mapped_column(Integer)
    width: Mapped[int | None] = mapped_column(Integer, nullable=True)
    height: Mapped[int | None] = mapped_column(Integer, nullable=True)
    alt_text: Mapped[str | None] = mapped_column(String(300), nullable=True)
    caption: Mapped[str | None] = mapped_column(String(500), nullable=True)
    # e.g. {"thumbnail": "abc-thumb.webp", "medium": "abc-medium.webp"}
    variants: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    uploaded_by_id: Mapped[int | None] = mapped_column(
        ForeignKey("admin_user.id", ondelete="SET NULL"), nullable=True
    )

    uploaded_by: Mapped[AdminUser | None] = relationship()
