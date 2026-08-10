from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class AdminRecoveryCode(TimestampMixin, Base):
    """A single one-time TOTP recovery code, hashed like a session token.

    Modeled as one row per code (not a JSON list column) so consuming a code
    is a plain atomic ``UPDATE ... WHERE used_at IS NULL`` rather than a
    read-modify-write race on a shared blob.
    """

    __tablename__ = "admin_recovery_code"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_user_id: Mapped[int] = mapped_column(
        ForeignKey("admin_user.id", ondelete="CASCADE"), index=True
    )
    code_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
