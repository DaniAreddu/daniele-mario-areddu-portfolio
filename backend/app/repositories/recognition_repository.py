from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.filters import visible_now
from app.models.recognition import Recognition


class RecognitionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Recognition]:
        result = await self.session.execute(
            select(Recognition).where(visible_now(Recognition)).order_by(Recognition.sort_order)
        )
        return list(result.scalars().all())

    async def list_all_admin(self, *, include_trashed: bool = False) -> list[Recognition]:
        stmt = select(Recognition)
        if not include_trashed:
            stmt = stmt.where(Recognition.deleted_at.is_(None))
        stmt = stmt.order_by(Recognition.sort_order)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, recognition_id: int) -> Recognition | None:
        return await self.session.get(Recognition, recognition_id)

    async def create(self, recognition: Recognition) -> Recognition:
        self.session.add(recognition)
        await self.session.flush()
        return recognition

    async def delete(self, recognition: Recognition) -> None:
        await self.session.delete(recognition)
