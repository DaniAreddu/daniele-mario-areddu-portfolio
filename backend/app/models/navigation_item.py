from __future__ import annotations

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class NavigationItem(TimestampMixin, Base):
    """A single header or footer navigation link. `placement` distinguishes
    the two rather than using two separate tables — the shape is identical.

    `label_en`/`label_it` follow the same bilingual free-text convention as
    every other public-facing string in this codebase (Profile, Biography,
    Project, ...) — a single `label` column would silently drop Italian
    labels, which the site's existing bilingual nav does not do today.
    """

    __tablename__ = "navigation_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    label_en: Mapped[str] = mapped_column(String(80), nullable=False)
    label_it: Mapped[str] = mapped_column(String(80), nullable=False, default="")
    # An internal path (must start with "/") or a full external URL,
    # validated at the schema layer depending on `is_external`.
    target: Mapped[str] = mapped_column(String(255), nullable=False)
    placement: Mapped[str] = mapped_column(String(20), nullable=False, default="header")
    is_external: Mapped[bool] = mapped_column(Boolean, default=False)
    open_in_new_tab: Mapped[bool] = mapped_column(Boolean, default=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
