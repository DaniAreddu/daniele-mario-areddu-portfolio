from __future__ import annotations

from sqlalchemy import JSON, Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin


class SiteSettings(TimestampMixin, Base):
    """Singleton (one row, like Profile/Biography/CommunityProfile) of
    typed, non-secret site configuration. Secrets never live here — they
    stay in environment variables (see docs/admin-guide.md).
    """

    __tablename__ = "site_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_name: Mapped[str] = mapped_column(String(200), default="Daniele Mario Areddu")
    public_site_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    default_timezone: Mapped[str] = mapped_column(String(60), default="Europe/Rome")
    default_language: Mapped[str] = mapped_column(String(10), default="en")
    maintenance_mode: Mapped[bool] = mapped_column(Boolean, default=False)
    show_speaking_map: Mapped[bool] = mapped_column(Boolean, default=True)
    show_statistics: Mapped[bool] = mapped_column(Boolean, default=True)
    show_now_section: Mapped[bool] = mapped_column(Boolean, default=False)
    show_projects: Mapped[bool] = mapped_column(Boolean, default=True)
    show_community: Mapped[bool] = mapped_column(Boolean, default=True)
    map_default_zoom: Mapped[int] = mapped_column(Integer, default=2)
    analytics_id: Mapped[str | None] = mapped_column(String(60), nullable=True)


class SeoSettings(TimestampMixin, Base):
    """Singleton global SEO defaults; per-content overrides live on the
    content rows themselves via SeoFieldsMixin.
    """

    __tablename__ = "seo_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    site_title: Mapped[str] = mapped_column(String(200), default="Daniele Mario Areddu")
    title_template: Mapped[str] = mapped_column(String(200), default="%s — Daniele Mario Areddu")
    default_description: Mapped[str] = mapped_column(Text, default="")
    default_og_image_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    twitter_card_type: Mapped[str] = mapped_column(String(30), default="summary_large_image")
    robots_default: Mapped[str] = mapped_column(String(60), default="index,follow")
    canonical_base_url: Mapped[str | None] = mapped_column(String(255), nullable=True)


class HomepageSettings(TimestampMixin, Base):
    """Singleton editorial homepage copy + section visibility/ordering.
    Featured entities are NOT duplicated here — see HomepageFeature.
    """

    __tablename__ = "homepage_settings"

    id: Mapped[int] = mapped_column(primary_key=True)
    hero_eyebrow_en: Mapped[str] = mapped_column(String(200), default="")
    hero_eyebrow_it: Mapped[str] = mapped_column(String(200), default="")
    hero_headline_en: Mapped[str] = mapped_column(Text, default="")
    hero_headline_it: Mapped[str] = mapped_column(Text, default="")
    hero_subheadline_en: Mapped[str] = mapped_column(Text, default="")
    hero_subheadline_it: Mapped[str] = mapped_column(Text, default="")
    primary_cta_label_en: Mapped[str | None] = mapped_column(String(80), nullable=True)
    primary_cta_label_it: Mapped[str | None] = mapped_column(String(80), nullable=True)
    primary_cta_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    secondary_cta_label_en: Mapped[str | None] = mapped_column(String(80), nullable=True)
    secondary_cta_label_it: Mapped[str | None] = mapped_column(String(80), nullable=True)
    secondary_cta_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    section_order: Mapped[list[str]] = mapped_column(JSON, default=list)
    section_visibility: Mapped[dict[str, bool]] = mapped_column(JSON, default=dict)


class HomepageFeature(TimestampMixin, Base):
    """Generic "what's pinned to the homepage, in what order" join — one
    table instead of parallel nullable FK columns per entity type.
    """

    __tablename__ = "homepage_feature"

    id: Mapped[int] = mapped_column(primary_key=True)
    entity_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    entity_id: Mapped[int] = mapped_column(Integer, nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
