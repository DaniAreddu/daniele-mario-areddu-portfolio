from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.site_settings import SeoSettings, SiteSettings
from app.services.singleton_admin_service import get_or_create_singleton


class SiteSettingsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self) -> SiteSettings:
        return await get_or_create_singleton(self.session, SiteSettings)


class SeoSettingsRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self) -> SeoSettings:
        return await get_or_create_singleton(self.session, SeoSettings)
