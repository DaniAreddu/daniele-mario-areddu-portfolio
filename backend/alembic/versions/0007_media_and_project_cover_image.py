"""Media library (media_asset table) and Project.cover_image_url.

Revision ID: 0007
Revises: 0006
Create Date: 2026-08-10

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0007"
down_revision: str | None = "0006"
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


def upgrade() -> None:
    op.add_column("project", sa.Column("cover_image_url", sa.String(500), nullable=True))

    op.create_table(
        "media_asset",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("storage_key", sa.String(255), nullable=False),
        sa.Column("original_filename", sa.String(255), nullable=False),
        sa.Column("mime_type", sa.String(100), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("width", sa.Integer(), nullable=True),
        sa.Column("height", sa.Integer(), nullable=True),
        sa.Column("alt_text", sa.String(300), nullable=True),
        sa.Column("caption", sa.String(500), nullable=True),
        sa.Column("variants", sa.JSON(), nullable=False, server_default="{}"),
        sa.Column(
            "uploaded_by_id",
            sa.Integer(),
            sa.ForeignKey("admin_user.id", ondelete="SET NULL"),
            nullable=True,
        ),
        *_timestamps(),
    )
    op.create_index("ix_media_asset_storage_key", "media_asset", ["storage_key"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_media_asset_storage_key", table_name="media_asset")
    op.drop_table("media_asset")
    op.drop_column("project", "cover_image_url")
