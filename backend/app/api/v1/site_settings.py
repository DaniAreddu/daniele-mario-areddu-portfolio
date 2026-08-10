from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession
from app.repositories.site_settings_repository import SeoSettingsRepository, SiteSettingsRepository
from app.schemas.seo import SeoSettingsOut
from app.schemas.site_settings import SiteSettingsOut
from app.services.site_settings_service import SeoSettingsService, SiteSettingsService

router = APIRouter()


def get_site_settings_service(session: DbSession) -> SiteSettingsService:
    return SiteSettingsService(SiteSettingsRepository(session))


def get_seo_settings_service(session: DbSession) -> SeoSettingsService:
    return SeoSettingsService(SeoSettingsRepository(session))


SiteServiceDep = Annotated[SiteSettingsService, Depends(get_site_settings_service)]
SeoServiceDep = Annotated[SeoSettingsService, Depends(get_seo_settings_service)]


@router.get("/site-settings", response_model=SiteSettingsOut)
async def get_site_settings(service: SiteServiceDep) -> SiteSettingsOut:
    return await service.get()


@router.get("/seo-settings", response_model=SeoSettingsOut)
async def get_seo_settings(service: SeoServiceDep) -> SeoSettingsOut:
    return await service.get()
