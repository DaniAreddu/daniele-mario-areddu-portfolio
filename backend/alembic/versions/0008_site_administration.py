"""Site administration layer: SiteSettings, SeoSettings, HomepageSettings +
HomepageFeature, NavigationItem, SocialLink, Redirect.

Revision ID: 0008
Revises: 0007
Create Date: 2026-08-10

"""

from __future__ import annotations

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

revision: str = "0008"
down_revision: str | None = "0007"
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
        "site_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_name", sa.String(200), nullable=False, server_default="Daniele Mario Areddu"),
        sa.Column("public_site_url", sa.String(255), nullable=True),
        sa.Column("default_timezone", sa.String(60), nullable=False, server_default="Europe/Rome"),
        sa.Column("default_language", sa.String(10), nullable=False, server_default="en"),
        sa.Column("maintenance_mode", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("show_speaking_map", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("show_statistics", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("show_now_section", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("show_projects", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("show_community", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("map_default_zoom", sa.Integer(), nullable=False, server_default="2"),
        sa.Column("analytics_id", sa.String(60), nullable=True),
        *_timestamps(),
    )

    op.create_table(
        "seo_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("site_title", sa.String(200), nullable=False, server_default="Daniele Mario Areddu"),
        sa.Column(
            "title_template",
            sa.String(200),
            nullable=False,
            server_default="%s — Daniele Mario Areddu",
        ),
        sa.Column("default_description", sa.Text(), nullable=False, server_default=""),
        sa.Column("default_og_image_url", sa.String(500), nullable=True),
        sa.Column(
            "twitter_card_type", sa.String(30), nullable=False, server_default="summary_large_image"
        ),
        sa.Column("robots_default", sa.String(60), nullable=False, server_default="index,follow"),
        sa.Column("canonical_base_url", sa.String(255), nullable=True),
        *_timestamps(),
    )

    op.create_table(
        "homepage_settings",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("hero_eyebrow_en", sa.String(200), nullable=False, server_default=""),
        sa.Column("hero_eyebrow_it", sa.String(200), nullable=False, server_default=""),
        sa.Column("hero_headline_en", sa.Text(), nullable=False, server_default=""),
        sa.Column("hero_headline_it", sa.Text(), nullable=False, server_default=""),
        sa.Column("hero_subheadline_en", sa.Text(), nullable=False, server_default=""),
        sa.Column("hero_subheadline_it", sa.Text(), nullable=False, server_default=""),
        sa.Column("primary_cta_label_en", sa.String(80), nullable=True),
        sa.Column("primary_cta_label_it", sa.String(80), nullable=True),
        sa.Column("primary_cta_url", sa.String(255), nullable=True),
        sa.Column("secondary_cta_label_en", sa.String(80), nullable=True),
        sa.Column("secondary_cta_label_it", sa.String(80), nullable=True),
        sa.Column("secondary_cta_url", sa.String(255), nullable=True),
        sa.Column("section_order", sa.JSON(), nullable=False, server_default="[]"),
        sa.Column("section_visibility", sa.JSON(), nullable=False, server_default="{}"),
        *_timestamps(),
    )

    op.create_table(
        "homepage_feature",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("entity_type", sa.String(30), nullable=False),
        sa.Column("entity_id", sa.Integer(), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )
    op.create_index("ix_homepage_feature_entity_type", "homepage_feature", ["entity_type"])

    op.create_table(
        "navigation_item",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("label_en", sa.String(80), nullable=False),
        sa.Column("label_it", sa.String(80), nullable=False, server_default=""),
        sa.Column("target", sa.String(255), nullable=False),
        sa.Column("placement", sa.String(20), nullable=False, server_default="header"),
        sa.Column("is_external", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("open_in_new_tab", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )

    op.create_table(
        "social_link",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("label", sa.String(80), nullable=False),
        sa.Column("url", sa.String(500), nullable=False),
        sa.Column("icon", sa.String(50), nullable=True),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        *_timestamps(),
    )

    op.create_table(
        "redirect",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_path", sa.String(300), nullable=False),
        sa.Column("destination_path", sa.String(300), nullable=False),
        sa.Column("status_code", sa.Integer(), nullable=False, server_default="301"),
        sa.Column("enabled", sa.Boolean(), nullable=False, server_default=sa.true()),
        *_timestamps(),
    )
    op.create_index("ix_redirect_source_path", "redirect", ["source_path"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_redirect_source_path", table_name="redirect")
    op.drop_table("redirect")
    op.drop_table("social_link")
    op.drop_table("navigation_item")
    op.drop_index("ix_homepage_feature_entity_type", table_name="homepage_feature")
    op.drop_table("homepage_feature")
    op.drop_table("homepage_settings")
    op.drop_table("seo_settings")
    op.drop_table("site_settings")
