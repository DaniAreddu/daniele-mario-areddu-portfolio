from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class SeoSettingsAdminWrite(BaseModel):
    site_title: str = "Daniele Mario Areddu"
    title_template: str = "%s — Daniele Mario Areddu"
    default_description: str = ""
    default_og_image_url: str | None = None
    twitter_card_type: str = "summary_large_image"
    robots_default: str = "index,follow"
    canonical_base_url: str | None = None


class SeoSettingsAdminOut(ORMModel):
    id: int
    site_title: str
    title_template: str
    default_description: str
    default_og_image_url: str | None
    twitter_card_type: str
    robots_default: str
    canonical_base_url: str | None
    created_at: datetime
    updated_at: datetime
