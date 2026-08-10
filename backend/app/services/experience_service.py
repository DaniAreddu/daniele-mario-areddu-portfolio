from __future__ import annotations

from app.repositories.experience_repository import ExperienceRepository
from app.schemas.experience import ExperienceOut
from app.services.localization import pick


class ExperienceService:
    def __init__(self, repository: ExperienceRepository) -> None:
        self.repository = repository

    async def list_all(self, locale: str) -> list[ExperienceOut]:
        items = await self.repository.list_all()
        return [
            ExperienceOut(
                organization=item.organization,
                role=pick(item, "role", locale),
                location=item.location,
                start_date=item.start_date,
                end_date=item.end_date,
                is_current=item.is_current,
                summary=pick(item, "summary", locale),
                highlights=pick(item, "highlights", locale),
                technologies=item.technologies,
            )
            for item in items
        ]
