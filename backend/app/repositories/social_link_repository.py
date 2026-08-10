from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.social_link import SocialLink


class SocialLinkRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_enabled(self) -> list[SocialLink]:
        result = await self.session.execute(
            select(SocialLink).where(SocialLink.enabled.is_(True)).order_by(SocialLink.sort_order)
        )
        return list(result.scalars().all())

    async def list_all(self) -> list[SocialLink]:
        result = await self.session.execute(select(SocialLink).order_by(SocialLink.sort_order))
        return list(result.scalars().all())

    async def get_by_id(self, link_id: int) -> SocialLink | None:
        return await self.session.get(SocialLink, link_id)

    async def create(self, link: SocialLink) -> SocialLink:
        self.session.add(link)
        await self.session.flush()
        return link

    async def delete(self, link: SocialLink) -> None:
        await self.session.delete(link)
