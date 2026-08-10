from __future__ import annotations

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class AdminUser(TimestampMixin, Base):
    """A webmaster/CMS operator account.

    ``role`` is a plain string (not a DB enum) for the same reason other
    status columns in this codebase are — adding a role later never requires
    an ``ALTER TYPE``. Only ``OWNER`` is used today; ``ADMIN``/``EDITOR`` are
    reserved so multi-user support doesn't require a schema change.
    """

    __tablename__ = "admin_user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="OWNER")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    totp_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    # Fernet-encrypted TOTP seed — never stored or logged in plaintext.
    totp_secret_encrypted: Mapped[str | None] = mapped_column(String(255), nullable=True)
