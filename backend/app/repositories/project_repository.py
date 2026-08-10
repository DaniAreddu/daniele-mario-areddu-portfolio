from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.filters import visible_now
from app.models.project import Project

_EAGER = (selectinload(Project.skills), selectinload(Project.tags))


class ProjectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    # -- public (published, non-deleted content only) ---------------------

    async def list_all(self) -> list[Project]:
        result = await self.session.execute(
            select(Project).options(*_EAGER).where(visible_now(Project)).order_by(Project.sort_order)
        )
        return list(result.scalars().all())

    async def get_by_slug(self, slug: str) -> Project | None:
        result = await self.session.execute(
            select(Project).options(*_EAGER).where(Project.slug == slug, visible_now(Project))
        )
        return result.scalars().first()

    # -- admin (everything, including drafts/trashed) ---------------------

    async def list_all_admin(self, *, include_trashed: bool = False) -> list[Project]:
        stmt = select(Project).options(*_EAGER)
        if not include_trashed:
            stmt = stmt.where(Project.deleted_at.is_(None))
        stmt = stmt.order_by(Project.sort_order)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def get_by_id(self, project_id: int) -> Project | None:
        result = await self.session.execute(
            select(Project).options(*_EAGER).where(Project.id == project_id)
        )
        return result.scalars().first()

    async def get_by_slug_any(self, slug: str) -> Project | None:
        result = await self.session.execute(select(Project).where(Project.slug == slug))
        return result.scalars().first()

    async def create(self, project: Project) -> Project:
        self.session.add(project)
        await self.session.flush()
        return project

    async def delete(self, project: Project) -> None:
        await self.session.delete(project)
