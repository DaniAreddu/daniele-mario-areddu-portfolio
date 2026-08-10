from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.revision import Revision


class RevisionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_for_entity(self, entity_type: str, entity_id: int) -> list[Revision]:
        result = await self.session.execute(
            select(Revision)
            .options(selectinload(Revision.created_by))
            .where(Revision.entity_type == entity_type, Revision.entity_id == entity_id)
            .order_by(Revision.created_at.desc())
        )
        return list(result.scalars().all())

    async def list_recent(self, limit: int = 10) -> list[Revision]:
        result = await self.session.execute(
            select(Revision)
            .options(selectinload(Revision.created_by))
            .order_by(Revision.created_at.desc())
            .limit(limit)
        )
        return list(result.scalars().all())

    async def get(self, revision_id: int) -> Revision | None:
        result = await self.session.execute(
            select(Revision)
            .options(selectinload(Revision.created_by))
            .where(Revision.id == revision_id)
        )
        return result.scalars().first()
