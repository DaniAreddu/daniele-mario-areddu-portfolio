from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.community import CommunityActivity, CommunityProfile


class CommunityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_profile(self) -> CommunityProfile | None:
        result = await self.session.execute(select(CommunityProfile).limit(1))
        return result.scalars().first()

    async def list_activities(self) -> list[CommunityActivity]:
        result = await self.session.execute(
            select(CommunityActivity).order_by(
                CommunityActivity.sort_order, CommunityActivity.activity_date.desc()
            )
        )
        return list(result.scalars().all())
