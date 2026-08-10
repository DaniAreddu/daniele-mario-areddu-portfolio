from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentAdminUser, DbSession, Locale, require_admin_spa_header
from app.repositories.event_repository import EventRepository
from app.repositories.revision_repository import RevisionRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.event import EventOut
from app.schemas.event_admin import (
    DuplicateCandidateOut,
    EventAdminCreate,
    EventAdminOut,
    EventAdminUpdate,
    EventListItemOut,
    EventScheduleRequest,
    RevisionDiffOut,
    RevisionOut,
)
from app.services.event_admin_service import EventAdminService

router = APIRouter(prefix="/admin/events")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_event_admin_service(session: DbSession) -> EventAdminService:
    return EventAdminService(
        EventRepository(session), TagRepository(session), RevisionRepository(session)
    )


EventAdminServiceDep = Annotated[EventAdminService, Depends(get_event_admin_service)]


@router.get("", response_model=list[EventListItemOut])
async def list_events(
    user: CurrentAdminUser,
    service: EventAdminServiceDep,
    trashed: Annotated[bool, Query()] = False,
) -> list[EventListItemOut]:
    return await service.list_all(include_trashed=trashed)


@router.get("/check-duplicates", response_model=list[DuplicateCandidateOut])
async def check_duplicates(
    user: CurrentAdminUser,
    service: EventAdminServiceDep,
    event_name: Annotated[str, Query(min_length=1)],
    year: Annotated[int, Query()],
    city: Annotated[str | None, Query()] = None,
) -> list[DuplicateCandidateOut]:
    return await service.check_duplicates(event_name, city, year)


@router.get("/{event_id}", response_model=EventAdminOut)
async def get_event(
    event_id: int, user: CurrentAdminUser, service: EventAdminServiceDep
) -> EventAdminOut:
    return await service.get(event_id)


@router.get("/{event_id}/preview", response_model=EventOut)
async def preview_event(
    event_id: int, locale: Locale, user: CurrentAdminUser, service: EventAdminServiceDep
) -> EventOut:
    return await service.preview(event_id, locale)


@router.post("", response_model=EventAdminOut, status_code=201)
async def create_event(
    payload: EventAdminCreate,
    user: CurrentAdminUser,
    service: EventAdminServiceDep,
    _spa: RequireSpaHeader,
) -> EventAdminOut:
    return await service.create(payload, user)


@router.patch("/{event_id}", response_model=EventAdminOut)
async def update_event(
    event_id: int,
    payload: EventAdminUpdate,
    user: CurrentAdminUser,
    service: EventAdminServiceDep,
    _spa: RequireSpaHeader,
) -> EventAdminOut:
    return await service.update(event_id, payload, user)


@router.post("/{event_id}/publish", response_model=EventAdminOut)
async def publish_event(
    event_id: int, user: CurrentAdminUser, service: EventAdminServiceDep, _spa: RequireSpaHeader
) -> EventAdminOut:
    return await service.publish(event_id, user)


@router.post("/{event_id}/schedule", response_model=EventAdminOut)
async def schedule_event(
    event_id: int,
    payload: EventScheduleRequest,
    user: CurrentAdminUser,
    service: EventAdminServiceDep,
    _spa: RequireSpaHeader,
) -> EventAdminOut:
    return await service.schedule(event_id, payload.publish_at, user)


@router.post("/{event_id}/unpublish", response_model=EventAdminOut)
async def unpublish_event(
    event_id: int, user: CurrentAdminUser, service: EventAdminServiceDep, _spa: RequireSpaHeader
) -> EventAdminOut:
    return await service.unpublish(event_id, user)


@router.post("/{event_id}/archive", response_model=EventAdminOut)
async def archive_event(
    event_id: int, user: CurrentAdminUser, service: EventAdminServiceDep, _spa: RequireSpaHeader
) -> EventAdminOut:
    return await service.archive(event_id, user)


@router.post("/{event_id}/trash", response_model=EventAdminOut)
async def trash_event(
    event_id: int, user: CurrentAdminUser, service: EventAdminServiceDep, _spa: RequireSpaHeader
) -> EventAdminOut:
    return await service.soft_delete(event_id, user)


@router.post("/{event_id}/restore", response_model=EventAdminOut)
async def restore_event(
    event_id: int, user: CurrentAdminUser, service: EventAdminServiceDep, _spa: RequireSpaHeader
) -> EventAdminOut:
    return await service.restore_from_trash(event_id, user)


@router.delete("/{event_id}", status_code=204, response_model=None)
async def delete_event_permanently(
    event_id: int, user: CurrentAdminUser, service: EventAdminServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.permanent_delete(event_id, user)


@router.get("/{event_id}/revisions", response_model=list[RevisionOut])
async def list_event_revisions(
    event_id: int, user: CurrentAdminUser, service: EventAdminServiceDep
) -> list[RevisionOut]:
    return await service.list_revisions(event_id)


@router.get("/{event_id}/revisions/{revision_id}/diff", response_model=RevisionDiffOut)
async def preview_revision_diff(
    event_id: int, revision_id: int, user: CurrentAdminUser, service: EventAdminServiceDep
) -> RevisionDiffOut:
    return await service.preview_revision_diff(event_id, revision_id)


@router.post("/{event_id}/revisions/{revision_id}/restore", response_model=EventAdminOut)
async def restore_event_revision(
    event_id: int,
    revision_id: int,
    user: CurrentAdminUser,
    service: EventAdminServiceDep,
    _spa: RequireSpaHeader,
) -> EventAdminOut:
    return await service.restore_revision(event_id, revision_id, user)
