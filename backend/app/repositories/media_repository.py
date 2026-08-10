from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.media_asset import MediaAsset


class MediaRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_all(self) -> list[MediaAsset]:
        result = await self.session.execute(
            select(MediaAsset)
            .options(selectinload(MediaAsset.uploaded_by))
            .order_by(MediaAsset.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_by_id(self, media_id: int) -> MediaAsset | None:
        result = await self.session.execute(
            select(MediaAsset)
            .options(selectinload(MediaAsset.uploaded_by))
            .where(MediaAsset.id == media_id)
        )
        return result.scalars().first()

    async def get_by_storage_key(self, storage_key: str) -> MediaAsset | None:
        result = await self.session.execute(
            select(MediaAsset).where(MediaAsset.storage_key == storage_key)
        )
        return result.scalars().first()

    async def create(self, asset: MediaAsset) -> MediaAsset:
        self.session.add(asset)
        await self.session.flush()
        return asset

    async def delete(self, asset: MediaAsset) -> None:
        await self.session.delete(asset)
