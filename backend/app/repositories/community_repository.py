from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.filters import visible_now
from app.models.community import CommunityActivity, CommunityProfile


class CommunityRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_profile(self) -> CommunityProfile | None:
        result = await self.session.execute(select(CommunityProfile).limit(1))
        return result.scalars().first()

    async def list_activities(self) -> list[CommunityActivity]:
        result = await self.session.execute(
            select(CommunityActivity)
            .where(visible_now(CommunityActivity))
            .order_by(CommunityActivity.sort_order, CommunityActivity.activity_date.desc())
        )
        return list(result.scalars().all())

    # -- admin --------------------------------------------------------

    async def list_activities_admin(
        self, *, include_trashed: bool = False
    ) -> list[CommunityActivity]:
        stmt = select(CommunityActivity)
        if not include_trashed:
            stmt = stmt.where(CommunityActivity.deleted_at.is_(None))
        stmt = stmt.order_by(CommunityActivity.sort_order, CommunityActivity.activity_date.desc())
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_activity_by_id(self, activity_id: int) -> CommunityActivity | None:
        return await self.session.get(CommunityActivity, activity_id)

    async def get_activity_by_slug_any(self, slug: str) -> CommunityActivity | None:
        result = await self.session.execute(
            select(CommunityActivity).where(CommunityActivity.slug == slug)
        )
        return result.scalars().first()

    async def create_activity(self, activity: CommunityActivity) -> CommunityActivity:
        self.session.add(activity)
        await self.session.flush()
        return activity

    async def delete_activity(self, activity: CommunityActivity) -> None:
        await self.session.delete(activity)
