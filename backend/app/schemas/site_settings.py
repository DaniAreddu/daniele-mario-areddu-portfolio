from __future__ import annotations

from app.schemas.common import ORMModel


class SiteSettingsOut(ORMModel):
    """Public, non-secret subset of SiteSettings — feature flags the
    frontend needs to decide what to render. Never includes analytics_id
    or anything else with even mild operational sensitivity.
    """

    maintenance_mode: bool
    show_speaking_map: bool
    show_statistics: bool
    show_now_section: bool
    show_projects: bool
    show_community: bool
    map_default_zoom: int
