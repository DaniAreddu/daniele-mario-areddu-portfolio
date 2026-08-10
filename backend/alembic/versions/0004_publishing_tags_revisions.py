"""Publication lifecycle + soft delete for Event, the Tag/event_tag
normalized vocabulary (backfilled from the existing Event.topics JSON), and
the generic Revision table.

Revision ID: 0004
Revises: 0003
Create Date: 2026-08-10

"""

from __future__ import annotations

import re
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0004"
down_revision: str | None = "0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _timestamps() -> list[sa.Column]:
    return [
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
    ]


def _slugify_tag(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def upgrade() -> None:
    # -- Event: publication lifecycle + soft delete + internal notes -------
    # server_default='PUBLISHED' is deliberate: every row that already
    # exists today is live content that must stay visible the moment this
    # column appears, not silently vanish because it defaulted to DRAFT.
    op.add_column(
        "event",
        sa.Column(
            "publication_status", sa.String(20), nullable=False, server_default="PUBLISHED"
        ),
    )
    op.add_column("event", sa.Column("publish_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("event", sa.Column("unpublish_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("event", sa.Column("published_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("event", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("event", sa.Column("internal_notes", sa.Text(), nullable=True))
    op.create_index("ix_event_publication_status", "event", ["publication_status"])
    op.create_index("ix_event_deleted_at", "event", ["deleted_at"])

    # -- Tag vocabulary + generic Revision log -----------------------------
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False),
        sa.Column("label", sa.String(80), nullable=False),
        *_timestamps(),
    )
    op.create_index("ix_tag_slug", "tag", ["slug"], unique=True)

    op.create_table(
        "event_tag",
        sa.Column(
            "event_id", sa.Integer(), sa.ForeignKey("event.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "tag_id", sa.Integer(), sa.ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
        ),
    )

    op.create_table(
        "revision",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entity_type", sa.String(50), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("schema_version", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("snapshot", sa.JSON(), nullable=False),
        sa.Column(
            "created_by_id",
            sa.Integer(),
            sa.ForeignKey("admin_user.id", ondelete="SET NULL"),
            nullable=True,
        ),
        *_timestamps(),
    )
    op.create_index("ix_revision_entity_type", "revision", ["entity_type"])
    op.create_index("ix_revision_entity_id", "revision", ["entity_id"])

    # -- Data migration: normalize existing Event.topics JSON into Tag rows.
    # Mirrors app/seed/seed.py::_seed_event_tags exactly, so a fresh dev/test
    # database (seeded, not migrated) ends up with equivalent tag data.
    connection = op.get_bind()
    event_table = sa.table("event", sa.column("id", sa.Integer()), sa.column("topics", sa.JSON()))
    tag_table = sa.table(
        "tag", sa.column("id", sa.Integer()), sa.column("slug", sa.String()),
        sa.column("label", sa.String()),
    )
    event_tag_table = sa.table(
        "event_tag", sa.column("event_id", sa.Integer()), sa.column("tag_id", sa.Integer())
    )

    rows = connection.execute(sa.select(event_table.c.id, event_table.c.topics)).fetchall()
    slug_to_id: dict[str, int] = {}
    for event_id, topics in rows:
        seen_tag_ids: set[int] = set()
        for raw_label in topics or []:
            label = raw_label.strip()
            if not label:
                continue
            slug = _slugify_tag(label)
            if not slug:
                continue
            if slug not in slug_to_id:
                inserted = connection.execute(
                    tag_table.insert().values(slug=slug, label=label).returning(tag_table.c.id)
                )
                slug_to_id[slug] = inserted.scalar_one()
            tag_id = slug_to_id[slug]
            if tag_id in seen_tag_ids:
                continue
            seen_tag_ids.add(tag_id)
            connection.execute(
                event_tag_table.insert().values(event_id=event_id, tag_id=tag_id)
            )


def downgrade() -> None:
    op.drop_table("revision")
    op.drop_table("event_tag")
    op.drop_table("tag")
    op.drop_index("ix_event_deleted_at", table_name="event")
    op.drop_index("ix_event_publication_status", table_name="event")
    op.drop_column("event", "internal_notes")
    op.drop_column("event", "deleted_at")
    op.drop_column("event", "published_at")
    op.drop_column("event", "unpublish_at")
    op.drop_column("event", "publish_at")
    op.drop_column("event", "publication_status")
