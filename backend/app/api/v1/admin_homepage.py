from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession, require_admin_spa_header
from app.models.site_settings import HomepageSettings
from app.repositories.event_repository import EventRepository
from app.repositories.homepage_repository import HomepageFeatureRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.homepage_admin import (
    HomepageFeatureAdminOut,
    HomepageFeatureAdminWrite,
    HomepageSettingsAdminOut,
    HomepageSettingsAdminWrite,
)
from app.services.homepage_admin_service import HomepageFeatureAdminService
from app.services.singleton_admin_service import SingletonAdminService

router = APIRouter(prefix="/admin/homepage")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_homepage_settings_service(
    session: DbSession,
) -> SingletonAdminService[HomepageSettings, HomepageSettingsAdminWrite]:
    return SingletonAdminService(
        session, HomepageSettings, "homepage_settings", RevisionRepository(session)
    )


def get_homepage_feature_service(session: DbSession) -> HomepageFeatureAdminService:
    return HomepageFeatureAdminService(
        HomepageFeatureRepository(session), ProjectRepository(session), EventRepository(session)
    )


SettingsServiceDep = Annotated[
    SingletonAdminService[HomepageSettings, HomepageSettingsAdminWrite],
    Depends(get_homepage_settings_service),
]
FeatureServiceDep = Annotated[HomepageFeatureAdminService, Depends(get_homepage_feature_service)]


@router.get("/settings", response_model=HomepageSettingsAdminOut)
async def get_homepage_settings(
    user: CurrentAdminUser, service: SettingsServiceDep
) -> HomepageSettings:
    return await service.get()


@router.put("/settings", response_model=HomepageSettingsAdminOut)
async def update_homepage_settings(
    payload: HomepageSettingsAdminWrite,
    user: CurrentAdminUser,
    service: SettingsServiceDep,
    _spa: RequireSpaHeader,
) -> HomepageSettings:
    return await service.update(payload, user)


@router.get("/settings/revisions", response_model=list[dict[str, Any]])
async def list_homepage_settings_revisions(
    user: CurrentAdminUser, service: SettingsServiceDep
) -> list[dict[str, Any]]:
    return await service.list_revisions()


@router.get("/features", response_model=list[HomepageFeatureAdminOut])
async def list_homepage_features(
    user: CurrentAdminUser, service: FeatureServiceDep
) -> list[HomepageFeatureAdminOut]:
    return await service.list_all()


@router.post("/features", response_model=HomepageFeatureAdminOut, status_code=201)
async def create_homepage_feature(
    payload: HomepageFeatureAdminWrite,
    user: CurrentAdminUser,
    service: FeatureServiceDep,
    _spa: RequireSpaHeader,
) -> HomepageFeatureAdminOut:
    return await service.create(payload, user)


@router.delete("/features/{feature_id}", status_code=204, response_model=None)
async def delete_homepage_feature(
    feature_id: int, user: CurrentAdminUser, service: FeatureServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.delete(feature_id, user)
