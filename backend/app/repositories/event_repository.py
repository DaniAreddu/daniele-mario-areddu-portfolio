from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.event import Event


class EventRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Event]:
        result = await self.session.execute(
            select(Event)
            .options(selectinload(Event.talk))
            .order_by(Event.start_date.is_(None), Event.start_date.desc(), Event.year.desc())
        )
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> Event | None:
        result = await self.session.execute(
            select(Event).options(selectinload(Event.talk)).where(Event.slug == slug)
        )
        return result.scalars().first()

    async def list_with_coordinates(self) -> list[Event]:
        result = await self.session.execute(
            select(Event)
            .options(selectinload(Event.talk))
            .where(Event.latitude.is_not(None), Event.longitude.is_not(None))
        )
        return list(result.scalars().all())
