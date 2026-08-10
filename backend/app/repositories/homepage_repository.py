from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.site_settings import HomepageFeature


class HomepageFeatureRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[HomepageFeature]:
        result = await self.session.execute(
            select(HomepageFeature).order_by(HomepageFeature.sort_order)
        )
        return list(result.scalars().all())

    async def get_by_id(self, feature_id: int) -> HomepageFeature | None:
        return await self.session.get(HomepageFeature, feature_id)

    async def create(self, feature: HomepageFeature) -> HomepageFeature:
        self.session.add(feature)
        await self.session.flush()
        return feature

    async def delete(self, feature: HomepageFeature) -> None:
        await self.session.delete(feature)
