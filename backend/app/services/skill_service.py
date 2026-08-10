from __future__ import annotations

from app.repositories.skill_repository import SkillRepository
from app.schemas.skill import SkillCategoryOut, SkillOut
from app.services.localization import pick


class SkillService:
    def __init__(self, repository: SkillRepository) -> None:
        self.repository = repository

    async def list_categories(self, locale: str) -> list[SkillCategoryOut]:
        categories = await self.repository.list_categories()
        return [
            SkillCategoryOut(
                slug=category.slug,
                name=pick(category, "name", locale),
                description=pick(category, "description", locale),
                skills=[
                    SkillOut(name=skill.name, context=pick(skill, "context", locale))
                    for skill in category.skills
                ],
            )
            for category in categories
        ]
