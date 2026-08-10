from __future__ import annotations

from app.repositories.site_settings_repository import SeoSettingsRepository, SiteSettingsRepository
from app.schemas.seo import SeoSettingsOut
from app.schemas.site_settings import SiteSettingsOut


class SiteSettingsService:
    def __init__(self, repository: SiteSettingsRepository) -> None:
        self.repository = repository

    async def get(self) -> SiteSettingsOut:
        settings = await self.repository.get()
        return SiteSettingsOut(
            maintenance_mode=settings.maintenance_mode,
            show_speaking_map=settings.show_speaking_map,
            show_statistics=settings.show_statistics,
            show_now_section=settings.show_now_section,
            show_projects=settings.show_projects,
            show_community=settings.show_community,
            map_default_zoom=settings.map_default_zoom,
        )


class SeoSettingsService:
    def __init__(self, repository: SeoSettingsRepository) -> None:
        self.repository = repository

    async def get(self) -> SeoSettingsOut:
        settings = await self.repository.get()
        return SeoSettingsOut(
            site_title=settings.site_title,
            title_template=settings.title_template,
            default_description=settings.default_description,
            default_og_image_url=settings.default_og_image_url,
            twitter_card_type=settings.twitter_card_type,
            robots_default=settings.robots_default,
            canonical_base_url=settings.canonical_base_url,
        )
