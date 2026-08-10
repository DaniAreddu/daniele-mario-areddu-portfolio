from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession, require_admin_spa_header
from app.models.site_settings import SeoSettings, SiteSettings
from app.repositories.revision_repository import RevisionRepository
from app.schemas.seo_admin import SeoSettingsAdminOut, SeoSettingsAdminWrite
from app.schemas.site_settings_admin import SiteSettingsAdminOut, SiteSettingsAdminWrite
from app.services.singleton_admin_service import SingletonAdminService

router = APIRouter(prefix="/admin")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_site_settings_service(
    session: DbSession,
) -> SingletonAdminService[SiteSettings, SiteSettingsAdminWrite]:
    return SingletonAdminService(
        session, SiteSettings, "site_settings", RevisionRepository(session)
    )


def get_seo_settings_service(
    session: DbSession,
) -> SingletonAdminService[SeoSettings, SeoSettingsAdminWrite]:
    return SingletonAdminService(session, SeoSettings, "seo_settings", RevisionRepository(session))


SiteSettingsServiceDep = Annotated[
    SingletonAdminService[SiteSettings, SiteSettingsAdminWrite], Depends(get_site_settings_service)
]
SeoSettingsServiceDep = Annotated[
    SingletonAdminService[SeoSettings, SeoSettingsAdminWrite], Depends(get_seo_settings_service)
]


@router.get("/site-settings", response_model=SiteSettingsAdminOut)
async def get_site_settings(
    user: CurrentAdminUser, service: SiteSettingsServiceDep
) -> SiteSettings:
    return await service.get()


@router.put("/site-settings", response_model=SiteSettingsAdminOut)
async def update_site_settings(
    payload: SiteSettingsAdminWrite,
    user: CurrentAdminUser,
    service: SiteSettingsServiceDep,
    _spa: RequireSpaHeader,
) -> SiteSettings:
    return await service.update(payload, user)


@router.get("/site-settings/revisions", response_model=list[dict[str, Any]])
async def list_site_settings_revisions(
    user: CurrentAdminUser, service: SiteSettingsServiceDep
) -> list[dict[str, Any]]:
    return await service.list_revisions()


@router.get("/seo-settings", response_model=SeoSettingsAdminOut)
async def get_seo_settings(user: CurrentAdminUser, service: SeoSettingsServiceDep) -> SeoSettings:
    return await service.get()


@router.put("/seo-settings", response_model=SeoSettingsAdminOut)
async def update_seo_settings(
    payload: SeoSettingsAdminWrite,
    user: CurrentAdminUser,
    service: SeoSettingsServiceDep,
    _spa: RequireSpaHeader,
) -> SeoSettings:
    return await service.update(payload, user)


@router.get("/seo-settings/revisions", response_model=list[dict[str, Any]])
async def list_seo_settings_revisions(
    user: CurrentAdminUser, service: SeoSettingsServiceDep
) -> list[dict[str, Any]]:
    return await service.list_revisions()
