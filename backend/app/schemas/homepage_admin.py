from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel

HOMEPAGE_FEATURE_ENTITY_TYPES = {"project", "event"}


class HomepageSettingsAdminWrite(BaseModel):
    hero_eyebrow_en: str = ""
    hero_eyebrow_it: str = ""
    hero_headline_en: str = ""
    hero_headline_it: str = ""
    hero_subheadline_en: str = ""
    hero_subheadline_it: str = ""
    primary_cta_label_en: str | None = None
    primary_cta_label_it: str | None = None
    primary_cta_url: str | None = None
    secondary_cta_label_en: str | None = None
    secondary_cta_label_it: str | None = None
    secondary_cta_url: str | None = None
    section_order: list[str] = Field(default_factory=list)
    section_visibility: dict[str, bool] = Field(default_factory=dict)


class HomepageSettingsAdminOut(ORMModel):
    id: int
    hero_eyebrow_en: str
    hero_eyebrow_it: str
    hero_headline_en: str
    hero_headline_it: str
    hero_subheadline_en: str
    hero_subheadline_it: str
    primary_cta_label_en: str | None
    primary_cta_label_it: str | None
    primary_cta_url: str | None
    secondary_cta_label_en: str | None
    secondary_cta_label_it: str | None
    secondary_cta_url: str | None
    section_order: list[str]
    section_visibility: dict[str, bool]
    created_at: datetime
    updated_at: datetime


class HomepageFeatureAdminWrite(BaseModel):
    entity_type: str = Field(
        pattern="^(" + "|".join(sorted(HOMEPAGE_FEATURE_ENTITY_TYPES)) + ")$"
    )
    entity_id: int
    sort_order: int = 0


class HomepageFeatureAdminOut(ORMModel):
    id: int
    entity_type: str
    entity_id: int
    sort_order: int
