from __future__ import annotations

from app.repositories.passion_repository import PassionRepository
from app.schemas.passion import PassionOut
from app.services.localization import pick


class PassionService:
    def __init__(self, repository: PassionRepository) -> None:
        self.repository = repository

    async def list_all(self, locale: str) -> list[PassionOut]:
        items = await self.repository.list_all()
        return [
            PassionOut(
                slug=item.slug,
                title=pick(item, "title", locale),
                text=pick(item, "text", locale),
                motif_label=item.motif_label,
            )
            for item in items
        ]
