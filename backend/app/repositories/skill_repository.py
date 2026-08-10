from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.skill import SkillCategory


class SkillRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_categories(self) -> list[SkillCategory]:
        result = await self.session.execute(
            select(SkillCategory)
            .options(selectinload(SkillCategory.skills))
            .order_by(SkillCategory.sort_order)
        )
        return list(result.scalars().all())
