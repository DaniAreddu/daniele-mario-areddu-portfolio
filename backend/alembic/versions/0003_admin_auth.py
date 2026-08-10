"""Admin authentication: users, sessions, login attempts, recovery codes,
and the audit log.

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-10

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0003"
down_revision: str | None = "0002"
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
    op.create_table(
        "admin_user",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(320), nullable=False),
        sa.Column("password_hash", sa.String(255), nullable=False),
        sa.Column("role", sa.String(20), nullable=False, server_default="OWNER"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("totp_enabled", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("totp_secret_encrypted", sa.String(255), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_admin_user_email", "admin_user", ["email"], unique=True)

    op.create_table(
        "admin_session",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "admin_user_id",
            sa.Integer(),
            sa.ForeignKey("admin_user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("token_hash", sa.String(64), nullable=False),
        sa.Column("status", sa.String(20), nullable=False, server_default="mfa_pending"),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("last_seen_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("ip_hash", sa.String(64), nullable=True),
        sa.Column("user_agent", sa.String(255), nullable=True),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_index("ix_admin_session_admin_user_id", "admin_session", ["admin_user_id"])
    op.create_index("ix_admin_session_token_hash", "admin_session", ["token_hash"], unique=True)

    op.create_table(
        "admin_login_attempt",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("kind", sa.String(20), nullable=False),
        sa.Column("email", sa.String(320), nullable=True),
        sa.Column(
            "admin_user_id",
            sa.Integer(),
            sa.ForeignKey("admin_user.id", ondelete="CASCADE"),
            nullable=True,
        ),
        sa.Column("ip_hash", sa.String(64), nullable=False),
        sa.Column("succeeded", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )
    op.create_index("ix_admin_login_attempt_email", "admin_login_attempt", ["email"])
    op.create_index(
        "ix_admin_login_attempt_admin_user_id", "admin_login_attempt", ["admin_user_id"]
    )
    op.create_index("ix_admin_login_attempt_ip_hash", "admin_login_attempt", ["ip_hash"])

    op.create_table(
        "admin_recovery_code",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "admin_user_id",
            sa.Integer(),
            sa.ForeignKey("admin_user.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("code_hash", sa.String(64), nullable=False),
        sa.Column("used_at", sa.DateTime(timezone=True), nullable=True),
        *_timestamps(),
    )
    op.create_index(
        "ix_admin_recovery_code_admin_user_id", "admin_recovery_code", ["admin_user_id"]
    )
    op.create_index(
        "ix_admin_recovery_code_code_hash", "admin_recovery_code", ["code_hash"], unique=True
    )

    op.create_table(
        "audit_event",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "actor_id",
            sa.Integer(),
            sa.ForeignKey("admin_user.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("entity_type", sa.String(50), nullable=True),
        sa.Column("entity_id", sa.Integer(), nullable=True),
        sa.Column("summary", sa.Text(), nullable=False, server_default=""),
        sa.Column("context", sa.JSON(), nullable=False, server_default="{}"),
        *_timestamps(),
    )
    op.create_index("ix_audit_event_actor_id", "audit_event", ["actor_id"])
    op.create_index("ix_audit_event_action", "audit_event", ["action"])
    op.create_index("ix_audit_event_entity_type", "audit_event", ["entity_type"])


def downgrade() -> None:
    op.drop_table("audit_event")
    op.drop_table("admin_recovery_code")
    op.drop_table("admin_login_attempt")
    op.drop_table("admin_session")
    op.drop_table("admin_user")
