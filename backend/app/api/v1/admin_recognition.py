from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentAdminUser, DbSession, Locale, require_admin_spa_header
from app.core.errors import NotFoundError
from app.repositories.recognition_repository import RecognitionRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.event_admin import EventScheduleRequest
from app.schemas.recognition import RecognitionOut
from app.schemas.recognition_admin import (
    RecognitionAdminOut,
    RecognitionAdminWrite,
    RecognitionListItemAdminOut,
    RecognitionRevisionOut,
)
from app.services.recognition_admin_service import RecognitionAdminService
from app.services.recognition_service import to_recognition_out

router = APIRouter(prefix="/admin/recognition")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_recognition_admin_service(session: DbSession) -> RecognitionAdminService:
    return RecognitionAdminService(RecognitionRepository(session), RevisionRepository(session))


ServiceDep = Annotated[RecognitionAdminService, Depends(get_recognition_admin_service)]


@router.get("", response_model=list[RecognitionListItemAdminOut])
async def list_recognition(
    user: CurrentAdminUser, service: ServiceDep, trashed: Annotated[bool, Query()] = False
) -> list[RecognitionListItemAdminOut]:
    return await service.list_all(include_trashed=trashed)


@router.get("/{recognition_id}", response_model=RecognitionAdminOut)
async def get_recognition(
    recognition_id: int, user: CurrentAdminUser, service: ServiceDep
) -> RecognitionAdminOut:
    return await service.get(recognition_id)


@router.get("/{recognition_id}/preview", response_model=RecognitionOut)
async def preview_recognition(
    recognition_id: int, locale: Locale, user: CurrentAdminUser, service: ServiceDep
) -> RecognitionOut:
    recognition = await service.repository.get_by_id(recognition_id)
    if recognition is None:
        raise NotFoundError("Recognition not found.")
    return to_recognition_out(recognition, locale)


@router.post("", response_model=RecognitionAdminOut, status_code=201)
async def create_recognition(
    payload: RecognitionAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> RecognitionAdminOut:
    return await service.create(payload, user)


@router.patch("/{recognition_id}", response_model=RecognitionAdminOut)
async def update_recognition(
    recognition_id: int,
    payload: RecognitionAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> RecognitionAdminOut:
    return await service.update(recognition_id, payload, user)


@router.post("/{recognition_id}/publish", response_model=RecognitionAdminOut)
async def publish_recognition(
    recognition_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> RecognitionAdminOut:
    return await service.publish(recognition_id, user)


@router.post("/{recognition_id}/schedule", response_model=RecognitionAdminOut)
async def schedule_recognition(
    recognition_id: int,
    payload: EventScheduleRequest,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> RecognitionAdminOut:
    return await service.schedule(recognition_id, payload.publish_at, user)


@router.post("/{recognition_id}/unpublish", response_model=RecognitionAdminOut)
async def unpublish_recognition(
    recognition_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> RecognitionAdminOut:
    return await service.unpublish(recognition_id, user)


@router.post("/{recognition_id}/archive", response_model=RecognitionAdminOut)
async def archive_recognition(
    recognition_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> RecognitionAdminOut:
    return await service.archive(recognition_id, user)


@router.post("/{recognition_id}/trash", response_model=RecognitionAdminOut)
async def trash_recognition(
    recognition_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> RecognitionAdminOut:
    return await service.soft_delete(recognition_id, user)


@router.post("/{recognition_id}/restore", response_model=RecognitionAdminOut)
async def restore_recognition(
    recognition_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> RecognitionAdminOut:
    return await service.restore_from_trash(recognition_id, user)


@router.delete("/{recognition_id}", status_code=204, response_model=None)
async def delete_recognition_permanently(
    recognition_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.permanent_delete(recognition_id, user)


@router.get("/{recognition_id}/revisions", response_model=list[RecognitionRevisionOut])
async def list_recognition_revisions(
    recognition_id: int, user: CurrentAdminUser, service: ServiceDep
) -> list[RecognitionRevisionOut]:
    return await service.list_revisions(recognition_id)


@router.post(
    "/{recognition_id}/revisions/{revision_id}/restore", response_model=RecognitionAdminOut
)
async def restore_recognition_revision(
    recognition_id: int,
    revision_id: int,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> RecognitionAdminOut:
    return await service.restore_revision(recognition_id, revision_id, user)
