"""Add event.month and event.is_international_milestone

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-10

"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column("event", sa.Column("month", sa.Integer(), nullable=True))
    op.add_column(
        "event",
        sa.Column(
            "is_international_milestone",
            sa.Boolean(),
            nullable=False,
            server_default=sa.false(),
        ),
    )


def downgrade() -> None:
    op.drop_column("event", "is_international_milestone")
    op.drop_column("event", "month")
