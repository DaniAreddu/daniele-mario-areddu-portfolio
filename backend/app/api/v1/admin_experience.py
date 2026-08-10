from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentAdminUser, DbSession, Locale, require_admin_spa_header
from app.core.errors import NotFoundError
from app.repositories.experience_repository import ExperienceRepository
from app.repositories.revision_repository import RevisionRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.event_admin import EventScheduleRequest
from app.schemas.experience import ExperienceOut
from app.schemas.experience_admin import (
    ExperienceAdminOut,
    ExperienceAdminWrite,
    ExperienceListItemAdminOut,
    ExperienceRevisionOut,
)
from app.services.experience_admin_service import ExperienceAdminService
from app.services.experience_service import to_experience_out

router = APIRouter(prefix="/admin/experience")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_experience_admin_service(session: DbSession) -> ExperienceAdminService:
    return ExperienceAdminService(
        ExperienceRepository(session), TagRepository(session), RevisionRepository(session)
    )


ServiceDep = Annotated[ExperienceAdminService, Depends(get_experience_admin_service)]


@router.get("", response_model=list[ExperienceListItemAdminOut])
async def list_experience(
    user: CurrentAdminUser, service: ServiceDep, trashed: Annotated[bool, Query()] = False
) -> list[ExperienceListItemAdminOut]:
    return await service.list_all(include_trashed=trashed)


@router.get("/{experience_id}", response_model=ExperienceAdminOut)
async def get_experience(
    experience_id: int, user: CurrentAdminUser, service: ServiceDep
) -> ExperienceAdminOut:
    return await service.get(experience_id)


@router.get("/{experience_id}/preview", response_model=ExperienceOut)
async def preview_experience(
    experience_id: int, locale: Locale, user: CurrentAdminUser, service: ServiceDep
) -> ExperienceOut:
    experience = await service.repository.get_by_id(experience_id)
    if experience is None:
        raise NotFoundError("Experience not found.")
    return to_experience_out(experience, locale)


@router.post("", response_model=ExperienceAdminOut, status_code=201)
async def create_experience(
    payload: ExperienceAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> ExperienceAdminOut:
    return await service.create(payload, user)


@router.patch("/{experience_id}", response_model=ExperienceAdminOut)
async def update_experience(
    experience_id: int,
    payload: ExperienceAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> ExperienceAdminOut:
    return await service.update(experience_id, payload, user)


@router.post("/{experience_id}/publish", response_model=ExperienceAdminOut)
async def publish_experience(
    experience_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> ExperienceAdminOut:
    return await service.publish(experience_id, user)


@router.post("/{experience_id}/schedule", response_model=ExperienceAdminOut)
async def schedule_experience(
    experience_id: int,
    payload: EventScheduleRequest,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> ExperienceAdminOut:
    return await service.schedule(experience_id, payload.publish_at, user)


@router.post("/{experience_id}/unpublish", response_model=ExperienceAdminOut)
async def unpublish_experience(
    experience_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> ExperienceAdminOut:
    return await service.unpublish(experience_id, user)


@router.post("/{experience_id}/archive", response_model=ExperienceAdminOut)
async def archive_experience(
    experience_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> ExperienceAdminOut:
    return await service.archive(experience_id, user)


@router.post("/{experience_id}/trash", response_model=ExperienceAdminOut)
async def trash_experience(
    experience_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> ExperienceAdminOut:
    return await service.soft_delete(experience_id, user)


@router.post("/{experience_id}/restore", response_model=ExperienceAdminOut)
async def restore_experience(
    experience_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> ExperienceAdminOut:
    return await service.restore_from_trash(experience_id, user)


@router.delete("/{experience_id}", status_code=204, response_model=None)
async def delete_experience_permanently(
    experience_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.permanent_delete(experience_id, user)


@router.get("/{experience_id}/revisions", response_model=list[ExperienceRevisionOut])
async def list_experience_revisions(
    experience_id: int, user: CurrentAdminUser, service: ServiceDep
) -> list[ExperienceRevisionOut]:
    return await service.list_revisions(experience_id)


@router.post("/{experience_id}/revisions/{revision_id}/restore", response_model=ExperienceAdminOut)
async def restore_experience_revision(
    experience_id: int,
    revision_id: int,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> ExperienceAdminOut:
    return await service.restore_revision(experience_id, revision_id, user)
