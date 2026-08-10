from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.education import Education


class EducationRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Education]:
        result = await self.session.execute(
            select(Education).order_by(Education.sort_order, Education.start_year)
        )
        return list(result.scalars().all())
