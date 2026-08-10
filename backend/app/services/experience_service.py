from __future__ import annotations

from app.models.experience import Experience
from app.repositories.experience_repository import ExperienceRepository
from app.schemas.experience import ExperienceOut
from app.services.localization import pick


def _experience_technologies(experience: Experience) -> list[str]:
    if experience.tags:
        return sorted({tag.label for tag in experience.tags})
    return experience.technologies


def to_experience_out(experience: Experience, locale: str) -> ExperienceOut:
    return ExperienceOut(
        organization=experience.organization,
        role=pick(experience, "role", locale),
        location=experience.location,
        start_date=experience.start_date,
        end_date=experience.end_date,
        is_current=experience.is_current,
        summary=pick(experience, "summary", locale),
        highlights=pick(experience, "highlights", locale),
        technologies=_experience_technologies(experience),
    )


class ExperienceService:
    def __init__(self, repository: ExperienceRepository) -> None:
        self.repository = repository

    async def list_all(self, locale: str) -> list[ExperienceOut]:
        items = await self.repository.list_all()
        return [to_experience_out(item, locale) for item in items]
