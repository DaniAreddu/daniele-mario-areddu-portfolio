from __future__ import annotations

from app.models.education import Education
from app.repositories.education_repository import EducationRepository
from app.schemas.education import EducationOut
from app.services.localization import pick


def to_education_out(item: Education, locale: str) -> EducationOut:
    return EducationOut(
        institution=item.institution,
        degree=pick(item, "degree", locale),
        location=item.location,
        start_year=item.start_year,
        end_year=item.end_year,
        is_ongoing=item.is_ongoing,
        description=pick(item, "description", locale),
    )


class EducationService:
    def __init__(self, repository: EducationRepository) -> None:
        self.repository = repository

    async def list_all(self, locale: str) -> list[EducationOut]:
        items = await self.repository.list_all()
        return [to_education_out(item, locale) for item in items]
