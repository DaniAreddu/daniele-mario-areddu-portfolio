"""Publication lifecycle + soft delete for Experience, Education, and
CommunityActivity; experience_tag (backfilled from Experience.technologies,
sharing the Tag vocabulary); enabled/is_featured switches for Skill/
SkillCategory; and the new Recognition table (certifications, awards,
recognition, publications).

Revision ID: 0006
Revises: 0005
Create Date: 2026-08-10

"""

from __future__ import annotations

import re
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0006"
down_revision: str | None = "0005"
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


def _publishable_columns() -> list[sa.Column]:
    return [
        sa.Column(
            "publication_status", sa.String(20), nullable=False, server_default="PUBLISHED"
        ),
        sa.Column("publish_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("unpublish_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("published_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
    ]


def _slugify_tag(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def upgrade() -> None:
    # -- Experience ---------------------------------------------------
    op.add_column("experience", sa.Column("employment_type", sa.String(40), nullable=True))
    op.add_column("experience", sa.Column("location_mode", sa.String(20), nullable=True))
    op.add_column("experience", sa.Column("long_description_en", sa.Text(), nullable=True))
    op.add_column("experience", sa.Column("long_description_it", sa.Text(), nullable=True))
    op.add_column(
        "experience",
        sa.Column("achievements_en", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column(
        "experience",
        sa.Column("achievements_it", sa.JSON(), nullable=False, server_default="[]"),
    )
    op.add_column("experience", sa.Column("company_url", sa.String(255), nullable=True))
    op.add_column("experience", sa.Column("logo_media_url", sa.String(255), nullable=True))
    op.add_column(
        "experience", sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false())
    )
    op.add_column("experience", sa.Column("internal_notes", sa.Text(), nullable=True))
    for column in _publishable_columns():
        op.add_column("experience", column)
    op.create_index("ix_experience_publication_status", "experience", ["publication_status"])
    op.create_index("ix_experience_deleted_at", "experience", ["deleted_at"])

    op.create_table(
        "experience_tag",
        sa.Column(
            "experience_id", sa.Integer(), sa.ForeignKey("experience.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "tag_id", sa.Integer(), sa.ForeignKey("tag.id", ondelete="CASCADE"), primary_key=True
        ),
    )

    # -- Education ------------------------------------------------------
    op.add_column("education", sa.Column("field", sa.String(200), nullable=True))
    op.add_column(
        "education", sa.Column("activities", sa.JSON(), nullable=False, server_default="[]")
    )
    op.add_column("education", sa.Column("url", sa.String(255), nullable=True))
    op.add_column("education", sa.Column("logo_media_url", sa.String(255), nullable=True))
    op.add_column("education", sa.Column("internal_notes", sa.Text(), nullable=True))
    for column in _publishable_columns():
        op.add_column("education", column)
    op.create_index("ix_education_publication_status", "education", ["publication_status"])
    op.create_index("ix_education_deleted_at", "education", ["deleted_at"])

    # -- CommunityActivity -----------------------------------------------
    op.add_column("community_activity", sa.Column("logo_media_url", sa.String(255), nullable=True))
    op.add_column(
        "community_activity",
        sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.add_column("community_activity", sa.Column("internal_notes", sa.Text(), nullable=True))
    for column in _publishable_columns():
        op.add_column("community_activity", column)
    op.create_index(
        "ix_community_activity_publication_status", "community_activity", ["publication_status"]
    )
    op.create_index("ix_community_activity_deleted_at", "community_activity", ["deleted_at"])

    # -- Skills: simple enabled/featured switches, no publish lifecycle ---
    op.add_column(
        "skill_category",
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.add_column(
        "skill", sa.Column("is_featured", sa.Boolean(), nullable=False, server_default=sa.false())
    )
    op.add_column(
        "skill", sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true())
    )

    # -- Recognition (new) ------------------------------------------------
    op.create_table(
        "recognition",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("kind", sa.String(30), nullable=False),
        sa.Column("title_en", sa.String(255), nullable=False),
        sa.Column("title_it", sa.String(255), nullable=False),
        sa.Column("issuer", sa.String(200), nullable=True),
        sa.Column("description_en", sa.Text(), nullable=True),
        sa.Column("description_it", sa.Text(), nullable=True),
        sa.Column("date_awarded", sa.Date(), nullable=True),
        sa.Column("url", sa.String(500), nullable=True),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("internal_notes", sa.Text(), nullable=True),
        *_publishable_columns(),
        *_timestamps(),
    )
    op.create_index("ix_recognition_kind", "recognition", ["kind"])
    op.create_index("ix_recognition_publication_status", "recognition", ["publication_status"])
    op.create_index("ix_recognition_deleted_at", "recognition", ["deleted_at"])

    # -- Data migration: normalize Experience.technologies into Tag rows ---
    connection = op.get_bind()
    experience_table = sa.table(
        "experience", sa.column("id", sa.Integer()), sa.column("technologies", sa.JSON())
    )
    tag_table = sa.table(
        "tag", sa.column("id", sa.Integer()), sa.column("slug", sa.String()),
        sa.column("label", sa.String()),
    )
    experience_tag_table = sa.table(
        "experience_tag",
        sa.column("experience_id", sa.Integer()),
        sa.column("tag_id", sa.Integer()),
    )

    existing_tags = connection.execute(sa.select(tag_table.c.id, tag_table.c.slug)).fetchall()
    slug_to_id: dict[str, int] = {slug: tag_id for tag_id, slug in existing_tags}

    rows = connection.execute(
        sa.select(experience_table.c.id, experience_table.c.technologies)
    ).fetchall()
    for experience_id, technologies in rows:
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
                experience_tag_table.insert().values(experience_id=experience_id, tag_id=tag_id)
            )


def downgrade() -> None:
    op.drop_table("recognition")
    op.drop_column("skill", "enabled")
    op.drop_column("skill", "is_featured")
    op.drop_column("skill_category", "enabled")

    op.drop_index("ix_community_activity_deleted_at", table_name="community_activity")
    op.drop_index("ix_community_activity_publication_status", table_name="community_activity")
    op.drop_column("community_activity", "internal_notes")
    op.drop_column("community_activity", "is_featured")
    op.drop_column("community_activity", "logo_media_url")
    for column in ("deleted_at", "published_at", "unpublish_at", "publish_at", "publication_status"):
        op.drop_column("community_activity", column)

    op.drop_index("ix_education_deleted_at", table_name="education")
    op.drop_index("ix_education_publication_status", table_name="education")
    op.drop_column("education", "internal_notes")
    op.drop_column("education", "logo_media_url")
    op.drop_column("education", "url")
    op.drop_column("education", "activities")
    op.drop_column("education", "field")
    for column in ("deleted_at", "published_at", "unpublish_at", "publish_at", "publication_status"):
        op.drop_column("education", column)

    op.drop_table("experience_tag")
    op.drop_index("ix_experience_deleted_at", table_name="experience")
    op.drop_index("ix_experience_publication_status", table_name="experience")
    for column in ("deleted_at", "published_at", "unpublish_at", "publish_at", "publication_status"):
        op.drop_column("experience", column)
    op.drop_column("experience", "internal_notes")
    op.drop_column("experience", "is_featured")
    op.drop_column("experience", "logo_media_url")
    op.drop_column("experience", "company_url")
    op.drop_column("experience", "achievements_it")
    op.drop_column("experience", "achievements_en")
    op.drop_column("experience", "long_description_it")
    op.drop_column("experience", "long_description_en")
    op.drop_column("experience", "location_mode")
    op.drop_column("experience", "employment_type")
