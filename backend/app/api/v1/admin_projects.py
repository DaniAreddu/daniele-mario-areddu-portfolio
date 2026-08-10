from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentAdminUser, DbSession, Locale, require_admin_spa_header
from app.core.errors import NotFoundError
from app.repositories.project_repository import ProjectRepository
from app.repositories.revision_repository import RevisionRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.event_admin import EventScheduleRequest
from app.schemas.project import ProjectDetailOut
from app.schemas.project_admin import (
    ProjectAdminCreate,
    ProjectAdminOut,
    ProjectAdminUpdate,
    ProjectListItemAdminOut,
    ProjectRevisionOut,
)
from app.services.project_admin_service import ProjectAdminService
from app.services.project_service import to_project_detail

router = APIRouter(prefix="/admin/projects")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_project_admin_service(session: DbSession) -> ProjectAdminService:
    return ProjectAdminService(
        ProjectRepository(session), TagRepository(session), RevisionRepository(session)
    )


ProjectAdminServiceDep = Annotated[ProjectAdminService, Depends(get_project_admin_service)]


@router.get("", response_model=list[ProjectListItemAdminOut])
async def list_projects(
    user: CurrentAdminUser,
    service: ProjectAdminServiceDep,
    trashed: Annotated[bool, Query()] = False,
) -> list[ProjectListItemAdminOut]:
    return await service.list_all(include_trashed=trashed)


@router.get("/{project_id}", response_model=ProjectAdminOut)
async def get_project(
    project_id: int, user: CurrentAdminUser, service: ProjectAdminServiceDep
) -> ProjectAdminOut:
    return await service.get(project_id)


@router.get("/{project_id}/preview", response_model=ProjectDetailOut)
async def preview_project(
    project_id: int, locale: Locale, user: CurrentAdminUser, service: ProjectAdminServiceDep
) -> ProjectDetailOut:
    # Reuses the exact public mapper, so preview matches what publishing
    # will actually produce, rather than a bespoke preview shape.
    project = await service.repository.get_by_id(project_id)
    if project is None:
        raise NotFoundError("Project not found.")
    return to_project_detail(project, locale)


@router.post("", response_model=ProjectAdminOut, status_code=201)
async def create_project(
    payload: ProjectAdminCreate,
    user: CurrentAdminUser,
    service: ProjectAdminServiceDep,
    _spa: RequireSpaHeader,
) -> ProjectAdminOut:
    return await service.create(payload, user)


@router.patch("/{project_id}", response_model=ProjectAdminOut)
async def update_project(
    project_id: int,
    payload: ProjectAdminUpdate,
    user: CurrentAdminUser,
    service: ProjectAdminServiceDep,
    _spa: RequireSpaHeader,
) -> ProjectAdminOut:
    return await service.update(project_id, payload, user)


@router.post("/{project_id}/publish", response_model=ProjectAdminOut)
async def publish_project(
    project_id: int, user: CurrentAdminUser, service: ProjectAdminServiceDep, _spa: RequireSpaHeader
) -> ProjectAdminOut:
    return await service.publish(project_id, user)


@router.post("/{project_id}/schedule", response_model=ProjectAdminOut)
async def schedule_project(
    project_id: int,
    payload: EventScheduleRequest,
    user: CurrentAdminUser,
    service: ProjectAdminServiceDep,
    _spa: RequireSpaHeader,
) -> ProjectAdminOut:
    return await service.schedule(project_id, payload.publish_at, user)


@router.post("/{project_id}/unpublish", response_model=ProjectAdminOut)
async def unpublish_project(
    project_id: int, user: CurrentAdminUser, service: ProjectAdminServiceDep, _spa: RequireSpaHeader
) -> ProjectAdminOut:
    return await service.unpublish(project_id, user)


@router.post("/{project_id}/archive", response_model=ProjectAdminOut)
async def archive_project(
    project_id: int, user: CurrentAdminUser, service: ProjectAdminServiceDep, _spa: RequireSpaHeader
) -> ProjectAdminOut:
    return await service.archive(project_id, user)


@router.post("/{project_id}/trash", response_model=ProjectAdminOut)
async def trash_project(
    project_id: int, user: CurrentAdminUser, service: ProjectAdminServiceDep, _spa: RequireSpaHeader
) -> ProjectAdminOut:
    return await service.soft_delete(project_id, user)


@router.post("/{project_id}/restore", response_model=ProjectAdminOut)
async def restore_project(
    project_id: int, user: CurrentAdminUser, service: ProjectAdminServiceDep, _spa: RequireSpaHeader
) -> ProjectAdminOut:
    return await service.restore_from_trash(project_id, user)


@router.delete("/{project_id}", status_code=204, response_model=None)
async def delete_project_permanently(
    project_id: int, user: CurrentAdminUser, service: ProjectAdminServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.permanent_delete(project_id, user)


@router.get("/{project_id}/revisions", response_model=list[ProjectRevisionOut])
async def list_project_revisions(
    project_id: int, user: CurrentAdminUser, service: ProjectAdminServiceDep
) -> list[ProjectRevisionOut]:
    return await service.list_revisions(project_id)


@router.post("/{project_id}/revisions/{revision_id}/restore", response_model=ProjectAdminOut)
async def restore_project_revision(
    project_id: int,
    revision_id: int,
    user: CurrentAdminUser,
    service: ProjectAdminServiceDep,
    _spa: RequireSpaHeader,
) -> ProjectAdminOut:
    return await service.restore_revision(project_id, revision_id, user)
