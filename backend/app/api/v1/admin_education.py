from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentAdminUser, DbSession, Locale, require_admin_spa_header
from app.core.errors import NotFoundError
from app.repositories.education_repository import EducationRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.education import EducationOut
from app.schemas.education_admin import (
    EducationAdminOut,
    EducationAdminWrite,
    EducationListItemAdminOut,
    EducationRevisionOut,
)
from app.schemas.event_admin import EventScheduleRequest
from app.services.education_admin_service import EducationAdminService
from app.services.education_service import to_education_out

router = APIRouter(prefix="/admin/education")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_education_admin_service(session: DbSession) -> EducationAdminService:
    return EducationAdminService(EducationRepository(session), RevisionRepository(session))


ServiceDep = Annotated[EducationAdminService, Depends(get_education_admin_service)]


@router.get("", response_model=list[EducationListItemAdminOut])
async def list_education(
    user: CurrentAdminUser, service: ServiceDep, trashed: Annotated[bool, Query()] = False
) -> list[EducationListItemAdminOut]:
    return await service.list_all(include_trashed=trashed)


@router.get("/{education_id}", response_model=EducationAdminOut)
async def get_education(
    education_id: int, user: CurrentAdminUser, service: ServiceDep
) -> EducationAdminOut:
    return await service.get(education_id)


@router.get("/{education_id}/preview", response_model=EducationOut)
async def preview_education(
    education_id: int, locale: Locale, user: CurrentAdminUser, service: ServiceDep
) -> EducationOut:
    education = await service.repository.get_by_id(education_id)
    if education is None:
        raise NotFoundError("Education not found.")
    return to_education_out(education, locale)


@router.post("", response_model=EducationAdminOut, status_code=201)
async def create_education(
    payload: EducationAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> EducationAdminOut:
    return await service.create(payload, user)


@router.patch("/{education_id}", response_model=EducationAdminOut)
async def update_education(
    education_id: int,
    payload: EducationAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> EducationAdminOut:
    return await service.update(education_id, payload, user)


@router.post("/{education_id}/publish", response_model=EducationAdminOut)
async def publish_education(
    education_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> EducationAdminOut:
    return await service.publish(education_id, user)


@router.post("/{education_id}/schedule", response_model=EducationAdminOut)
async def schedule_education(
    education_id: int,
    payload: EventScheduleRequest,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> EducationAdminOut:
    return await service.schedule(education_id, payload.publish_at, user)


@router.post("/{education_id}/unpublish", response_model=EducationAdminOut)
async def unpublish_education(
    education_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> EducationAdminOut:
    return await service.unpublish(education_id, user)


@router.post("/{education_id}/archive", response_model=EducationAdminOut)
async def archive_education(
    education_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> EducationAdminOut:
    return await service.archive(education_id, user)


@router.post("/{education_id}/trash", response_model=EducationAdminOut)
async def trash_education(
    education_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> EducationAdminOut:
    return await service.soft_delete(education_id, user)


@router.post("/{education_id}/restore", response_model=EducationAdminOut)
async def restore_education(
    education_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> EducationAdminOut:
    return await service.restore_from_trash(education_id, user)


@router.delete("/{education_id}", status_code=204, response_model=None)
async def delete_education_permanently(
    education_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.permanent_delete(education_id, user)


@router.get("/{education_id}/revisions", response_model=list[EducationRevisionOut])
async def list_education_revisions(
    education_id: int, user: CurrentAdminUser, service: ServiceDep
) -> list[EducationRevisionOut]:
    return await service.list_revisions(education_id)


@router.post("/{education_id}/revisions/{revision_id}/restore", response_model=EducationAdminOut)
async def restore_education_revision(
    education_id: int,
    revision_id: int,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> EducationAdminOut:
    return await service.restore_revision(education_id, revision_id, user)
