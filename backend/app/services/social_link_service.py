from __future__ import annotations

from app.repositories.social_link_repository import SocialLinkRepository
from app.schemas.social_link import SocialLinkOut


class SocialLinkService:
    def __init__(self, repository: SocialLinkRepository) -> None:
        self.repository = repository

    async def list_all(self) -> list[SocialLinkOut]:
        links = await self.repository.list_enabled()
        return [SocialLinkOut(label=link.label, url=link.url, icon=link.icon) for link in links]
