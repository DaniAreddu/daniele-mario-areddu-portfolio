from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.project import Project


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[Project]:
        result = await self.session.execute(
            select(Project)
            .options(selectinload(Project.skills))
            .order_by(Project.sort_order)
        )
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> Project | None:
        result = await self.session.execute(
            select(Project).options(selectinload(Project.skills)).where(Project.slug == slug)
        )
        return result.scalars().first()
