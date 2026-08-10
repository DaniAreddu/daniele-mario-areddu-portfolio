from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.talk import Talk


class TalkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Talk]:
        result = await self.session.execute(
            select(Talk)
            .options(selectinload(Talk.events))
            .order_by(Talk.is_featured.desc(), Talk.title)
        )
        return list(result.scalars().all())
