from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentAdminUser, DbSession, Locale, require_admin_spa_header
from app.core.errors import NotFoundError
from app.models.community import CommunityProfile
from app.repositories.community_repository import CommunityRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.community import CommunityActivityOut
from app.schemas.community_admin import (
    CommunityActivityAdminOut,
    CommunityActivityAdminWrite,
    CommunityActivityListItemAdminOut,
    CommunityActivityRevisionOut,
    CommunityProfileAdminOut,
    CommunityProfileAdminWrite,
)
from app.schemas.event_admin import EventScheduleRequest
from app.services.community_admin_service import CommunityActivityAdminService
from app.services.community_service import to_community_activity_out
from app.services.singleton_admin_service import SingletonAdminService

router = APIRouter(prefix="/admin/community")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_activity_service(session: DbSession) -> CommunityActivityAdminService:
    return CommunityActivityAdminService(CommunityRepository(session), RevisionRepository(session))


def get_profile_singleton_service(
    session: DbSession,
) -> SingletonAdminService[CommunityProfile, CommunityProfileAdminWrite]:
    return SingletonAdminService(
        session, CommunityProfile, "community_profile", RevisionRepository(session)
    )


ActivityServiceDep = Annotated[CommunityActivityAdminService, Depends(get_activity_service)]
ProfileServiceDep = Annotated[
    SingletonAdminService[CommunityProfile, CommunityProfileAdminWrite],
    Depends(get_profile_singleton_service),
]


# -- profile (singleton) ---------------------------------------------------


@router.get("/profile", response_model=CommunityProfileAdminOut)
async def get_community_profile(
    user: CurrentAdminUser, service: ProfileServiceDep
) -> CommunityProfile:
    return await service.get()


@router.put("/profile", response_model=CommunityProfileAdminOut)
async def update_community_profile(
    payload: CommunityProfileAdminWrite,
    user: CurrentAdminUser,
    service: ProfileServiceDep,
    _spa: RequireSpaHeader,
) -> CommunityProfile:
    return await service.update(payload, user)


@router.get("/profile/revisions", response_model=list[dict[str, Any]])
async def list_community_profile_revisions(
    user: CurrentAdminUser, service: ProfileServiceDep
) -> list[dict[str, Any]]:
    return await service.list_revisions()


# -- activities (full lifecycle) -------------------------------------------


@router.get("/activities", response_model=list[CommunityActivityListItemAdminOut])
async def list_activities(
    user: CurrentAdminUser,
    service: ActivityServiceDep,
    trashed: Annotated[bool, Query()] = False,
) -> list[CommunityActivityListItemAdminOut]:
    return await service.list_all(include_trashed=trashed)


@router.get("/activities/{activity_id}", response_model=CommunityActivityAdminOut)
async def get_activity(
    activity_id: int, user: CurrentAdminUser, service: ActivityServiceDep
) -> CommunityActivityAdminOut:
    return await service.get(activity_id)


@router.get("/activities/{activity_id}/preview", response_model=CommunityActivityOut)
async def preview_activity(
    activity_id: int, locale: Locale, user: CurrentAdminUser, service: ActivityServiceDep
) -> CommunityActivityOut:
    activity = await service.community_repository.get_activity_by_id(activity_id)
    if activity is None:
        raise NotFoundError("Activity not found.")
    return to_community_activity_out(activity, locale)


@router.post("/activities", response_model=CommunityActivityAdminOut, status_code=201)
async def create_activity(
    payload: CommunityActivityAdminWrite,
    user: CurrentAdminUser,
    service: ActivityServiceDep,
    _spa: RequireSpaHeader,
) -> CommunityActivityAdminOut:
    return await service.create(payload, user)


@router.patch("/activities/{activity_id}", response_model=CommunityActivityAdminOut)
async def update_activity(
    activity_id: int,
    payload: CommunityActivityAdminWrite,
    user: CurrentAdminUser,
    service: ActivityServiceDep,
    _spa: RequireSpaHeader,
) -> CommunityActivityAdminOut:
    return await service.update(activity_id, payload, user)


@router.post("/activities/{activity_id}/publish", response_model=CommunityActivityAdminOut)
async def publish_activity(
    activity_id: int, user: CurrentAdminUser, service: ActivityServiceDep, _spa: RequireSpaHeader
) -> CommunityActivityAdminOut:
    return await service.publish(activity_id, user)


@router.post("/activities/{activity_id}/schedule", response_model=CommunityActivityAdminOut)
async def schedule_activity(
    activity_id: int,
    payload: EventScheduleRequest,
    user: CurrentAdminUser,
    service: ActivityServiceDep,
    _spa: RequireSpaHeader,
) -> CommunityActivityAdminOut:
    return await service.schedule(activity_id, payload.publish_at, user)


@router.post("/activities/{activity_id}/unpublish", response_model=CommunityActivityAdminOut)
async def unpublish_activity(
    activity_id: int, user: CurrentAdminUser, service: ActivityServiceDep, _spa: RequireSpaHeader
) -> CommunityActivityAdminOut:
    return await service.unpublish(activity_id, user)


@router.post("/activities/{activity_id}/archive", response_model=CommunityActivityAdminOut)
async def archive_activity(
    activity_id: int, user: CurrentAdminUser, service: ActivityServiceDep, _spa: RequireSpaHeader
) -> CommunityActivityAdminOut:
    return await service.archive(activity_id, user)


@router.post("/activities/{activity_id}/trash", response_model=CommunityActivityAdminOut)
async def trash_activity(
    activity_id: int, user: CurrentAdminUser, service: ActivityServiceDep, _spa: RequireSpaHeader
) -> CommunityActivityAdminOut:
    return await service.soft_delete(activity_id, user)


@router.post("/activities/{activity_id}/restore", response_model=CommunityActivityAdminOut)
async def restore_activity(
    activity_id: int, user: CurrentAdminUser, service: ActivityServiceDep, _spa: RequireSpaHeader
) -> CommunityActivityAdminOut:
    return await service.restore_from_trash(activity_id, user)


@router.delete("/activities/{activity_id}", status_code=204, response_model=None)
async def delete_activity_permanently(
    activity_id: int, user: CurrentAdminUser, service: ActivityServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.permanent_delete(activity_id, user)


@router.get(
    "/activities/{activity_id}/revisions", response_model=list[CommunityActivityRevisionOut]
)
async def list_activity_revisions(
    activity_id: int, user: CurrentAdminUser, service: ActivityServiceDep
) -> list[CommunityActivityRevisionOut]:
    return await service.list_revisions(activity_id)


@router.post(
    "/activities/{activity_id}/revisions/{revision_id}/restore",
    response_model=CommunityActivityAdminOut,
)
async def restore_activity_revision(
    activity_id: int,
    revision_id: int,
    user: CurrentAdminUser,
    service: ActivityServiceDep,
    _spa: RequireSpaHeader,
) -> CommunityActivityAdminOut:
    return await service.restore_revision(activity_id, revision_id, user)
