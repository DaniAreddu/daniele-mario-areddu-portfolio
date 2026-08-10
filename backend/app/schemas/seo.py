from __future__ import annotations

from app.schemas.common import ORMModel


class SeoSettingsOut(ORMModel):
    site_title: str
    title_template: str
    default_description: str
    default_og_image_url: str | None
    twitter_card_type: str
    robots_default: str
    canonical_base_url: str | None
