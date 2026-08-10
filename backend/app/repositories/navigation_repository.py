from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.navigation_item import NavigationItem


class NavigationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_enabled(self) -> list[NavigationItem]:
        result = await self.session.execute(
            select(NavigationItem)
            .where(NavigationItem.enabled.is_(True))
            .order_by(NavigationItem.sort_order)
        )
        return list(result.scalars().all())

    async def list_all(self) -> list[NavigationItem]:
        result = await self.session.execute(
            select(NavigationItem).order_by(NavigationItem.placement, NavigationItem.sort_order)
        )
        return list(result.scalars().all())

    async def get_by_id(self, item_id: int) -> NavigationItem | None:
        return await self.session.get(NavigationItem, item_id)

    async def create(self, item: NavigationItem) -> NavigationItem:
        self.session.add(item)
        await self.session.flush()
        return item

    async def delete(self, item: NavigationItem) -> None:
        await self.session.delete(item)
