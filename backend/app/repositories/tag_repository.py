from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.tag import Tag


class TagRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_slug(self, slug: str) -> Tag | None:
        result = await self.session.execute(select(Tag).where(Tag.slug == slug))
        return result.scalars().first()

    async def create(self, tag: Tag) -> Tag:
        self.session.add(tag)
        await self.session.flush()
        return tag

    async def list_all(self) -> list[Tag]:
        result = await self.session.execute(select(Tag).order_by(Tag.label))
        return list(result.scalars().all())
