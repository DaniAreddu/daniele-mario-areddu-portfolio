from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.profile import Biography, Profile


class ProfileRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_profile(self) -> Profile | None:
        result = await self.session.execute(select(Profile).limit(1))
        return result.scalars().first()

    async def get_biography(self) -> Biography | None:
        result = await self.session.execute(select(Biography).limit(1))
        return result.scalars().first()
