from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class SiteSettingsAdminWrite(BaseModel):
    site_name: str = "Daniele Mario Areddu"
    public_site_url: str | None = None
    default_timezone: str = "Europe/Rome"
    default_language: str = "en"
    maintenance_mode: bool = False
    show_speaking_map: bool = True
    show_statistics: bool = True
    show_now_section: bool = False
    show_projects: bool = True
    show_community: bool = True
    map_default_zoom: int = 2
    analytics_id: str | None = None


class SiteSettingsAdminOut(ORMModel):
    id: int
    site_name: str
    public_site_url: str | None
    default_timezone: str
    default_language: str
    maintenance_mode: bool
    show_speaking_map: bool
    show_statistics: bool
    show_now_section: bool
    show_projects: bool
    show_community: bool
    map_default_zoom: int
    analytics_id: str | None
    created_at: datetime
    updated_at: datetime
