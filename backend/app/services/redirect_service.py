from __future__ import annotations

from app.repositories.redirect_repository import RedirectRepository
from app.schemas.redirect import RedirectOut


class RedirectService:
    def __init__(self, repository: RedirectRepository) -> None:
        self.repository = repository

    async def list_all(self) -> list[RedirectOut]:
        redirects = await self.repository.list_enabled()
        return [
            RedirectOut(
                source_path=redirect.source_path,
                destination_path=redirect.destination_path,
                status_code=redirect.status_code,
            )
            for redirect in redirects
        ]
