from __future__ import annotations

from app.repositories.event_repository import EventRepository
from app.repositories.project_repository import ProjectRepository


async def test_event_repository_list_with_coordinates(db_session):
    repo = EventRepository(db_session)
    events = await repo.list_with_coordinates()
    assert len(events) > 0
    assert all(event.latitude is not None and event.longitude is not None for event in events)


async def test_event_repository_get_by_slug_returns_none_when_missing(db_session):
    repo = EventRepository(db_session)
    assert await repo.get_by_slug("does-not-exist") is None


async def test_project_repository_loads_related_skills(db_session):
    repo = ProjectRepository(db_session)
    project = await repo.get_by_slug("municipal-data-reconciliation-platform")
    assert project is not None
    assert len(project.skills) > 0
