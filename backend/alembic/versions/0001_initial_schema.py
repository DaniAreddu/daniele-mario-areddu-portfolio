"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2026-08-08

"""
from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0001"
down_revision: str | None = None
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
        "profile",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("full_name", sa.String(120), nullable=False),
        sa.Column("roles", sa.JSON(), nullable=False),
        sa.Column("location", sa.String(120), nullable=False),
        sa.Column("base_country", sa.String(80), nullable=False),
        sa.Column("availability_en", sa.Text(), nullable=False),
        sa.Column("availability_it", sa.Text(), nullable=False),
        sa.Column("tagline_en", sa.Text(), nullable=False),
        sa.Column("tagline_it", sa.Text(), nullable=False),
        sa.Column("positioning_statement_en", sa.Text(), nullable=False),
        sa.Column("positioning_statement_it", sa.Text(), nullable=False),
        sa.Column("brand_label", sa.String(80), nullable=False),
        sa.Column("public_email", sa.String(255), nullable=False),
        sa.Column("github_url", sa.String(255), nullable=True),
        sa.Column("linkedin_url", sa.String(255), nullable=True),
        sa.Column("sessionize_url", sa.String(255), nullable=True),
        sa.Column("talks_count_label", sa.String(40), nullable=False),
        sa.Column("speaking_years_label", sa.String(40), nullable=False),
        sa.Column("speaking_regions_label", sa.String(160), nullable=False),
        *_timestamps(),
    )

    op.create_table(
        "biography",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("micro_en", sa.Text(), nullable=False),
        sa.Column("micro_it", sa.Text(), nullable=False),
        sa.Column("short_en", sa.Text(), nullable=False),
        sa.Column("short_it", sa.Text(), nullable=False),
        sa.Column("medium_en", sa.Text(), nullable=False),
        sa.Column("medium_it", sa.Text(), nullable=False),
        sa.Column("long_en", sa.Text(), nullable=False),
        sa.Column("long_it", sa.Text(), nullable=False),
        sa.Column("speaker_bio_en", sa.Text(), nullable=False),
        sa.Column("speaker_bio_it", sa.Text(), nullable=False),
        *_timestamps(),
    )

    op.create_table(
        "education",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("institution", sa.String(200), nullable=False),
        sa.Column("degree_en", sa.String(200), nullable=False),
        sa.Column("degree_it", sa.String(200), nullable=False),
        sa.Column("location", sa.String(120), nullable=False),
        sa.Column("start_year", sa.Integer(), nullable=True),
        sa.Column("end_year", sa.Integer(), nullable=True),
        sa.Column("is_ongoing", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("description_en", sa.Text(), nullable=True),
        sa.Column("description_it", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )

    op.create_table(
        "experience",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("organization", sa.String(200), nullable=False),
        sa.Column("role_en", sa.String(200), nullable=False),
        sa.Column("role_it", sa.String(200), nullable=False),
        sa.Column("location", sa.String(120), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("is_current", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("summary_en", sa.Text(), nullable=False),
        sa.Column("summary_it", sa.Text(), nullable=False),
        sa.Column("highlights_en", sa.JSON(), nullable=False),
        sa.Column("highlights_it", sa.JSON(), nullable=False),
        sa.Column("technologies", sa.JSON(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )

    op.create_table(
        "skill_category",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(80), nullable=False, unique=True),
        sa.Column("name_en", sa.String(120), nullable=False),
        sa.Column("name_it", sa.String(120), nullable=False),
        sa.Column("description_en", sa.Text(), nullable=True),
        sa.Column("description_it", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )
    op.create_index("ix_skill_category_slug", "skill_category", ["slug"])

    op.create_table(
        "skill",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "category_id", sa.Integer(), sa.ForeignKey("skill_category.id"), nullable=False
        ),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("context_en", sa.Text(), nullable=True),
        sa.Column("context_it", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )

    op.create_table(
        "project",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(140), nullable=False, unique=True),
        sa.Column("title_en", sa.String(200), nullable=False),
        sa.Column("title_it", sa.String(200), nullable=False),
        sa.Column("summary_en", sa.Text(), nullable=False),
        sa.Column("summary_it", sa.Text(), nullable=False),
        sa.Column("problem_en", sa.Text(), nullable=False),
        sa.Column("problem_it", sa.Text(), nullable=False),
        sa.Column("challenge_en", sa.Text(), nullable=False),
        sa.Column("challenge_it", sa.Text(), nullable=False),
        sa.Column("approach_en", sa.Text(), nullable=False),
        sa.Column("approach_it", sa.Text(), nullable=False),
        sa.Column("architecture_en", sa.Text(), nullable=False),
        sa.Column("architecture_it", sa.Text(), nullable=False),
        sa.Column("key_decisions_en", sa.JSON(), nullable=False),
        sa.Column("key_decisions_it", sa.JSON(), nullable=False),
        sa.Column("outcome_en", sa.Text(), nullable=False),
        sa.Column("outcome_it", sa.Text(), nullable=False),
        sa.Column("lessons_en", sa.Text(), nullable=False),
        sa.Column("lessons_it", sa.Text(), nullable=False),
        sa.Column("confidentiality_note_en", sa.Text(), nullable=False),
        sa.Column("confidentiality_note_it", sa.Text(), nullable=False),
        sa.Column("technologies", sa.JSON(), nullable=False),
        sa.Column("external_url", sa.String(255), nullable=True),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )
    op.create_index("ix_project_slug", "project", ["slug"])

    op.create_table(
        "project_skill",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("project_id", sa.Integer(), sa.ForeignKey("project.id"), nullable=False),
        sa.Column("skill_name", sa.String(120), nullable=False),
    )

    op.create_table(
        "talk",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(160), nullable=False, unique=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("language", sa.String(10), nullable=False, server_default="en"),
        sa.Column("summary_en", sa.Text(), nullable=True),
        sa.Column("summary_it", sa.Text(), nullable=True),
        sa.Column("topics", sa.JSON(), nullable=False),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_timestamps(),
    )
    op.create_index("ix_talk_slug", "talk", ["slug"])

    op.create_table(
        "event",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(160), nullable=False, unique=True),
        sa.Column("event_name", sa.String(200), nullable=False),
        sa.Column("talk_id", sa.Integer(), sa.ForeignKey("talk.id"), nullable=True),
        sa.Column("session_title", sa.String(255), nullable=True),
        sa.Column("short_description_en", sa.Text(), nullable=True),
        sa.Column("short_description_it", sa.Text(), nullable=True),
        sa.Column("full_description_en", sa.Text(), nullable=True),
        sa.Column("full_description_it", sa.Text(), nullable=True),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("year", sa.Integer(), nullable=False),
        sa.Column("city", sa.String(120), nullable=True),
        sa.Column("country", sa.String(120), nullable=True),
        sa.Column("continent", sa.String(60), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=True),
        sa.Column("longitude", sa.Float(), nullable=True),
        sa.Column("venue", sa.String(200), nullable=True),
        sa.Column("format", sa.String(40), nullable=False, server_default="conference"),
        sa.Column("language", sa.String(10), nullable=False, server_default="en"),
        sa.Column("topics", sa.JSON(), nullable=False),
        sa.Column("event_url", sa.String(255), nullable=True),
        sa.Column("slides_url", sa.String(255), nullable=True),
        sa.Column("recording_url", sa.String(255), nullable=True),
        sa.Column("image", sa.String(255), nullable=True),
        sa.Column("status", sa.String(20), nullable=False, server_default="confirmed"),
        sa.Column("sessions_count", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_timestamps(),
    )
    op.create_index("ix_event_slug", "event", ["slug"])
    op.create_index("ix_event_start_date", "event", ["start_date"])
    op.create_index("ix_event_year", "event", ["year"])
    op.create_index("ix_event_city", "event", ["city"])
    op.create_index("ix_event_country", "event", ["country"])
    op.create_index("ix_event_continent", "event", ["continent"])

    op.create_table(
        "passion",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(120), nullable=False, unique=True),
        sa.Column("title_en", sa.String(160), nullable=False),
        sa.Column("title_it", sa.String(160), nullable=False),
        sa.Column("text_en", sa.Text(), nullable=False),
        sa.Column("text_it", sa.Text(), nullable=False),
        sa.Column("motif_label", sa.String(160), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )
    op.create_index("ix_passion_slug", "passion", ["slug"])

    op.create_table(
        "community_profile",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("role_en", sa.String(120), nullable=False),
        sa.Column("role_it", sa.String(120), nullable=False),
        sa.Column("mission_en", sa.Text(), nullable=False),
        sa.Column("mission_it", sa.Text(), nullable=False),
        sa.Column("description_en", sa.Text(), nullable=False),
        sa.Column("description_it", sa.Text(), nullable=False),
        sa.Column("vision_en", sa.Text(), nullable=False),
        sa.Column("vision_it", sa.Text(), nullable=False),
        sa.Column("collaboration_en", sa.Text(), nullable=False),
        sa.Column("collaboration_it", sa.Text(), nullable=False),
        sa.Column("founded_year", sa.Integer(), nullable=False),
        sa.Column("website_url", sa.String(255), nullable=True),
        *_timestamps(),
    )

    op.create_table(
        "community_activity",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("slug", sa.String(140), nullable=False, unique=True),
        sa.Column("title_en", sa.String(200), nullable=False),
        sa.Column("title_it", sa.String(200), nullable=False),
        sa.Column("description_en", sa.Text(), nullable=False),
        sa.Column("description_it", sa.Text(), nullable=False),
        sa.Column("activity_date", sa.Date(), nullable=True),
        sa.Column("activity_type", sa.String(40), nullable=False, server_default="meetup"),
        sa.Column("url", sa.String(255), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )
    op.create_index("ix_community_activity_slug", "community_activity", ["slug"])

    op.create_table(
        "contact_submission",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(160), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("organization", sa.String(200), nullable=True),
        sa.Column("request_type", sa.String(40), nullable=False),
        sa.Column("event_or_project", sa.String(200), nullable=True),
        sa.Column("indicative_date", sa.String(80), nullable=True),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("consent_given", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("source_ip_hash", sa.String(64), nullable=True),
        sa.Column("email_delivered", sa.Boolean(), nullable=False, server_default=sa.false()),
        *_timestamps(),
    )


def downgrade() -> None:
    op.drop_table("contact_submission")
    op.drop_table("community_activity")
    op.drop_table("community_profile")
    op.drop_table("passion")
    op.drop_index("ix_event_continent", table_name="event")
    op.drop_index("ix_event_country", table_name="event")
    op.drop_index("ix_event_city", table_name="event")
    op.drop_index("ix_event_year", table_name="event")
    op.drop_index("ix_event_start_date", table_name="event")
    op.drop_table("event")
    op.drop_table("talk")
    op.drop_table("project_skill")
    op.drop_table("project")
    op.drop_table("skill")
    op.drop_table("skill_category")
    op.drop_table("experience")
    op.drop_table("education")
    op.drop_table("biography")
    op.drop_table("profile")
