from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class Redirect(TimestampMixin, Base):
    """`destination_path` is enforced (at the schema layer) to start with
    `/` — no external redirect targets are supported, which eliminates
    open-redirect risk by construction rather than by allowlisting.
    """

    __tablename__ = "redirect"

    id: Mapped[int] = mapped_column(primary_key=True)
    source_path: Mapped[str] = mapped_column(String(300), unique=True, index=True)
    destination_path: Mapped[str] = mapped_column(String(300), nullable=False)
    status_code: Mapped[int] = mapped_column(Integer, default=301)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
