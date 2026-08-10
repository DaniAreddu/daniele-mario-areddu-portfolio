from __future__ import annotations

from app.repositories.education_repository import EducationRepository
from app.schemas.education import EducationOut
from app.services.localization import pick


class EducationService:
    def __init__(self, repository: EducationRepository) -> None:
        self.repository = repository

    async def list_all(self, locale: str) -> list[EducationOut]:
        items = await self.repository.list_all()
        return [
            EducationOut(
                institution=item.institution,
                degree=pick(item, "degree", locale),
                location=item.location,
                start_year=item.start_year,
                end_year=item.end_year,
                is_ongoing=item.is_ongoing,
                description=pick(item, "description", locale),
            )
            for item in items
        ]
