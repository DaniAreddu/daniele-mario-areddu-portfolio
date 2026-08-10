from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.filters import visible_now
from app.models.experience import Experience

_EAGER = (selectinload(Experience.tags),)


class ExperienceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Experience]:
        result = await self.session.execute(
            select(Experience)
            .options(*_EAGER)
            .where(visible_now(Experience))
            .order_by(Experience.sort_order, Experience.start_date.desc())
        )
        return list(result.scalars().all())

    async def list_all_admin(self, *, include_trashed: bool = False) -> list[Experience]:
        stmt = select(Experience).options(*_EAGER)
        if not include_trashed:
            stmt = stmt.where(Experience.deleted_at.is_(None))
        stmt = stmt.order_by(Experience.sort_order, Experience.start_date.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, experience_id: int) -> Experience | None:
        result = await self.session.execute(
            select(Experience).options(*_EAGER).where(Experience.id == experience_id)
        )
        return result.scalars().first()

    async def create(self, experience: Experience) -> Experience:
        self.session.add(experience)
        await self.session.flush()
        return experience

    async def delete(self, experience: Experience) -> None:
        await self.session.delete(experience)
