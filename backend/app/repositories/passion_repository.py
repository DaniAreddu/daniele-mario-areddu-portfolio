from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.passion import Passion


class PassionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Passion]:
        result = await self.session.execute(select(Passion).order_by(Passion.sort_order))
        return list(result.scalars().all())
