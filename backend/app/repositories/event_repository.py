from __future__ import annotations

import re

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.filters import visible_now
from app.models.event import Event

_EAGER = (selectinload(Event.talk), selectinload(Event.tags))


def _normalize(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower())


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # -- public (published, non-deleted content only) ---------------------

    async def list_all(self) -> list[Event]:
        result = await self.session.execute(
            select(Event)
            .options(*_EAGER)
            .where(visible_now(Event))
            .order_by(Event.start_date.is_(None), Event.start_date.desc(), Event.year.desc())
        )
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> Event | None:
        result = await self.session.execute(
            select(Event)
            .options(*_EAGER)
            .where(Event.slug == slug, visible_now(Event))
        )
        return result.scalars().first()

    async def list_with_coordinates(self) -> list[Event]:
        result = await self.session.execute(
            select(Event)
            .options(*_EAGER)
            .where(Event.latitude.is_not(None), Event.longitude.is_not(None), visible_now(Event))
        )
        return list(result.scalars().all())

    # -- admin (everything, including drafts/trashed) ---------------------

    async def list_all_admin(self, *, include_trashed: bool = False) -> list[Event]:
        stmt = select(Event).options(*_EAGER)
        if not include_trashed:
            stmt = stmt.where(Event.deleted_at.is_(None))
        stmt = stmt.order_by(Event.created_at.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, event_id: int) -> Event | None:
        result = await self.session.execute(
            select(Event).options(*_EAGER).where(Event.id == event_id)
        )
        return result.scalars().first()

    async def get_by_slug_any(self, slug: str) -> Event | None:
        """Includes drafts/trashed rows — used for slug-uniqueness checks."""
        result = await self.session.execute(select(Event).where(Event.slug == slug))
        return result.scalars().first()

    async def create(self, event: Event) -> Event:
        self.session.add(event)
        await self.session.flush()
        return event

    async def delete(self, event: Event) -> None:
        await self.session.delete(event)

    async def find_similar(self, event_name: str, city: str | None, year: int) -> list[Event]:
        """Heuristic duplicate-appearance detection: same year, plus a close
        name or an exact city match on normalized (lowercased,
        punctuation-stripped) text. Good enough for a single-operator dataset
        of a few dozen rows a year — not a fuzzy-matching library.
        """
        result = await self.session.execute(
            select(Event).where(Event.year == year, Event.deleted_at.is_(None))
        )
        normalized_name = _normalize(event_name)
        normalized_city = _normalize(city) if city else None
        matches = []
        for candidate in result.scalars():
            candidate_name = _normalize(candidate.event_name)
            name_close = bool(normalized_name) and (
                normalized_name in candidate_name or candidate_name in normalized_name
            )
            city_match = (
                normalized_city is not None
                and candidate.city is not None
                and normalized_city == _normalize(candidate.city)
            )
            if name_close or city_match:
                matches.append(candidate)
        return matches
