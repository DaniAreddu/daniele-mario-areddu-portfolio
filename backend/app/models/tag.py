from __future__ import annotations

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin

# Generic many-to-many associations, one per content type — all sharing the
# same Tag vocabulary (a "Python" tag on an event and a "Python" tag on a
# project are the same row), per the reusable-tag-system requirement.
event_tag = Table(
    "event_tag",
    Base.metadata,
    Column("event_id", ForeignKey("event.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)

project_tag = Table(
    "project_tag",
    Base.metadata,
    Column("project_id", ForeignKey("project.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True),
)


class Tag(TimestampMixin, Base):
    """A single reusable, admin-managed tag (e.g. "AI", "FastAPI").

    Deliberately a real table with a normalized, unique `slug` rather than
    free-text arrays on each content row — this is what prevents "AI" /
    "Artificial Intelligence" / "artificial-intelligence" from drifting into
    three different tags over time.
    """

    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    label: Mapped[str] = mapped_column(String(80))
