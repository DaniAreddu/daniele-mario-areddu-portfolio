from __future__ import annotations

from app.schemas.common import ORMModel


class HomepageFeatureItemOut(ORMModel):
    entity_type: str
    title: str
    summary: str
    url_path: str
    image_url: str | None


class HomepageOut(ORMModel):
    hero_eyebrow: str
    hero_headline: str
    hero_subheadline: str
    primary_cta_label: str | None
    primary_cta_url: str | None
    secondary_cta_label: str | None
    secondary_cta_url: str | None
    section_order: list[str]
    section_visibility: dict[str, bool]
    features: list[HomepageFeatureItemOut]
