from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.experience import Experience


class ExperienceRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Experience]:
        result = await self.session.execute(
            select(Experience).order_by(Experience.sort_order, Experience.start_date.desc())
        )
        return list(result.scalars().all())
