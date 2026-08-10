from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession, require_admin_spa_header
from app.models.profile import Biography, Profile
from app.repositories.revision_repository import RevisionRepository
from app.schemas.profile_admin import (
    BiographyAdminOut,
    BiographyAdminWrite,
    ProfileAdminOut,
    ProfileAdminWrite,
)
from app.services.singleton_admin_service import SingletonAdminService

router = APIRouter(prefix="/admin")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_profile_service(session: DbSession) -> SingletonAdminService[Profile, ProfileAdminWrite]:
    return SingletonAdminService(session, Profile, "profile", RevisionRepository(session))


def get_biography_service(
    session: DbSession,
) -> SingletonAdminService[Biography, BiographyAdminWrite]:
    return SingletonAdminService(session, Biography, "biography", RevisionRepository(session))


ProfileServiceDep = Annotated[
    SingletonAdminService[Profile, ProfileAdminWrite], Depends(get_profile_service)
]
BiographyServiceDep = Annotated[
    SingletonAdminService[Biography, BiographyAdminWrite], Depends(get_biography_service)
]


@router.get("/profile", response_model=ProfileAdminOut)
async def get_profile(user: CurrentAdminUser, service: ProfileServiceDep) -> Profile:
    return await service.get()


@router.put("/profile", response_model=ProfileAdminOut)
async def update_profile(
    payload: ProfileAdminWrite,
    user: CurrentAdminUser,
    service: ProfileServiceDep,
    _spa: RequireSpaHeader,
) -> Profile:
    return await service.update(payload, user)


@router.get("/profile/revisions", response_model=list[dict[str, Any]])
async def list_profile_revisions(
    user: CurrentAdminUser, service: ProfileServiceDep
) -> list[dict[str, Any]]:
    return await service.list_revisions()


@router.get("/biography", response_model=BiographyAdminOut)
async def get_biography(user: CurrentAdminUser, service: BiographyServiceDep) -> Biography:
    return await service.get()


@router.put("/biography", response_model=BiographyAdminOut)
async def update_biography(
    payload: BiographyAdminWrite,
    user: CurrentAdminUser,
    service: BiographyServiceDep,
    _spa: RequireSpaHeader,
) -> Biography:
    return await service.update(payload, user)


@router.get("/biography/revisions", response_model=list[dict[str, Any]])
async def list_biography_revisions(
    user: CurrentAdminUser, service: BiographyServiceDep
) -> list[dict[str, Any]]:
    return await service.list_revisions()
