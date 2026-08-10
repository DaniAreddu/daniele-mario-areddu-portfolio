"""Publication lifecycle + soft delete for Project, project_tag (backfilled
from the existing Project.technologies JSON, sharing the Tag vocabulary
introduced for Event in 0004).

Revision ID: 0005
Revises: 0004
Create Date: 2026-08-10

"""

from __future__ import annotations

import re
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0005"
down_revision: str | None = "0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def _slugify_tag(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def upgrade() -> None:
    op.add_column(
        "project",
        sa.Column(
            "publication_status", sa.String(20), nullable=False, server_default="PUBLISHED"
        ),
    )
    op.add_column("project", sa.Column("publish_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column(
        "project", sa.Column("unpublish_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column(
        "project", sa.Column("published_at", sa.DateTime(timezone=True), nullable=True)
    )
    op.add_column("project", sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("project", sa.Column("internal_notes", sa.Text(), nullable=True))
    op.create_index("ix_project_publication_status", "project", ["publication_status"])
    op.create_index("ix_project_deleted_at", "project", ["deleted_at"])

    op.create_table(
        "project_tag",
        sa.Column(
            "project_id", sa.Integer(), sa.ForeignKey("project.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "tag_id", sa.Integer(), sa.ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
        ),
    )

    # Data migration: normalize existing Project.technologies JSON into Tag
    # rows, reusing any tag already created by the 0004 Event migration
    # (e.g. a project tagged "Python" shares the same row as an event
    # tagged "Python" — that sharing is the entire point of a single Tag
    # vocabulary, see docs/event-management.md).
    connection = op.get_bind()
    project_table = sa.table(
        "project", sa.column("id", sa.Integer()), sa.column("technologies", sa.JSON())
    )
    tag_table = sa.table(
        "tag", sa.column("id", sa.Integer()), sa.column("slug", sa.String()),
        sa.column("label", sa.String()),
    )
    project_tag_table = sa.table(
        "project_tag", sa.column("project_id", sa.Integer()), sa.column("tag_id", sa.Integer())
    )

    existing_tags = connection.execute(sa.select(tag_table.c.id, tag_table.c.slug)).fetchall()
    slug_to_id: dict[str, int] = {slug: tag_id for tag_id, slug in existing_tags}

    rows = connection.execute(
        sa.select(project_table.c.id, project_table.c.technologies)
    ).fetchall()
    for project_id, technologies in rows:
        seen_tag_ids: set[int] = set()
        for raw_label in technologies or []:
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
                project_tag_table.insert().values(project_id=project_id, tag_id=tag_id)
            )


def downgrade() -> None:
    op.drop_table("project_tag")
    op.drop_index("ix_project_deleted_at", table_name="project")
    op.drop_index("ix_project_publication_status", table_name="project")
    op.drop_column("project", "internal_notes")
    op.drop_column("project", "deleted_at")
    op.drop_column("project", "published_at")
    op.drop_column("project", "unpublish_at")
    op.drop_column("project", "publish_at")
    op.drop_column("project", "publication_status")
