from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.redirect import Redirect


class RedirectRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_enabled(self) -> list[Redirect]:
        result = await self.session.execute(
            select(Redirect).where(Redirect.enabled.is_(True)).order_by(Redirect.source_path)
        )
        return list(result.scalars().all())

    async def list_all(self) -> list[Redirect]:
        result = await self.session.execute(select(Redirect).order_by(Redirect.source_path))
        return list(result.scalars().all())

    async def get_by_id(self, redirect_id: int) -> Redirect | None:
        return await self.session.get(Redirect, redirect_id)

    async def get_by_source_path(self, source_path: str) -> Redirect | None:
        result = await self.session.execute(
            select(Redirect).where(Redirect.source_path == source_path)
        )
        return result.scalars().first()

    async def create(self, redirect: Redirect) -> Redirect:
        self.session.add(redirect)
        await self.session.flush()
        return redirect

    async def delete(self, redirect: Redirect) -> None:
        await self.session.delete(redirect)
