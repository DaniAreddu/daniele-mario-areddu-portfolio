from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class AdminSession(TimestampMixin, Base):
    """A single browser session, identified by the SHA-256 hash of an opaque
    cookie token — the raw token is never persisted (see app.core.security).

    ``status`` models the two-step login flow: a session starts as
    ``mfa_pending`` (password verified, TOTP not yet verified — rejected by
    ``get_current_admin_user``) and only becomes ``active`` once a required
    second factor passes, or immediately for accounts without TOTP enabled.
    """

    __tablename__ = "admin_session"

    id: Mapped[int] = mapped_column(primary_key=True)
    admin_user_id: Mapped[int] = mapped_column(
        ForeignKey("admin_user.id", ondelete="CASCADE"), index=True
    )
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="mfa_pending")
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    ip_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)
    user_agent: Mapped[str | None] = mapped_column(String(255), nullable=True)
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)


class AdminLoginAttempt(Base):
    """A single password or TOTP verification attempt, used purely to throttle
    brute-force attempts (never joined into any public-facing view).
    """

    __tablename__ = "admin_login_attempt"

    id: Mapped[int] = mapped_column(primary_key=True)
    kind: Mapped[str] = mapped_column(String(20))  # "password" | "totp"
    email: Mapped[str | None] = mapped_column(String(320), nullable=True, index=True)
    admin_user_id: Mapped[int | None] = mapped_column(
        ForeignKey("admin_user.id", ondelete="CASCADE"), nullable=True, index=True
    )
    ip_hash: Mapped[str] = mapped_column(String(64), index=True)
    succeeded: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
