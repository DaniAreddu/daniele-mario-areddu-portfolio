from __future__ import annotations

from app.repositories.navigation_repository import NavigationRepository
from app.schemas.navigation import NavigationItemOut, NavigationOut
from app.services.localization import pick


class NavigationService:
    def __init__(self, repository: NavigationRepository) -> None:
        self.repository = repository

    async def get(self, locale: str) -> NavigationOut:
        items = await self.repository.list_enabled()
        header = [
            NavigationItemOut(
                label=pick(item, "label", locale),
                target=item.target,
                is_external=item.is_external,
                open_in_new_tab=item.open_in_new_tab,
            )
            for item in items
            if item.placement == "header"
        ]
        footer = [
            NavigationItemOut(
                label=pick(item, "label", locale),
                target=item.target,
                is_external=item.is_external,
                open_in_new_tab=item.open_in_new_tab,
            )
            for item in items
            if item.placement == "footer"
        ]
        return NavigationOut(header=header, footer=footer)
