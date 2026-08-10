from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.skill import Skill, SkillCategory


class SkillRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_categories(self) -> list[SkillCategory]:
        """Public: only enabled categories. Disabled *skills* within an
        enabled category are filtered by the service layer when mapping to
        the output schema — never by mutating `category.skills` here, since
        that relationship cascades "all, delete-orphan": assigning it a
        filtered list would delete the "removed" (merely disabled) skills
        from the database on the next flush.
        """
        result = await self.session.execute(
            select(SkillCategory)
            .options(selectinload(SkillCategory.skills))
            .where(SkillCategory.enabled.is_(True))
            .order_by(SkillCategory.sort_order)
        )
        return list(result.scalars().all())

    # -- admin: everything, regardless of enabled -------------------------

    async def list_categories_admin(self) -> list[SkillCategory]:
        result = await self.session.execute(
            select(SkillCategory).options(selectinload(SkillCategory.skills)).order_by(
                SkillCategory.sort_order
            )
        )
        return list(result.scalars().all())

    async def get_category_by_id(self, category_id: int) -> SkillCategory | None:
        result = await self.session.execute(
            select(SkillCategory)
            .options(selectinload(SkillCategory.skills))
            .where(SkillCategory.id == category_id)
        )
        return result.scalars().first()

    async def get_category_by_slug_any(self, slug: str) -> SkillCategory | None:
        result = await self.session.execute(
            select(SkillCategory).where(SkillCategory.slug == slug)
        )
        return result.scalars().first()

    async def create_category(self, category: SkillCategory) -> SkillCategory:
        self.session.add(category)
        await self.session.flush()
        return category

    async def delete_category(self, category: SkillCategory) -> None:
        await self.session.delete(category)

    async def get_skill_by_id(self, skill_id: int) -> Skill | None:
        return await self.session.get(Skill, skill_id)

    async def create_skill(self, skill: Skill) -> Skill:
        self.session.add(skill)
        await self.session.flush()
        return skill

    async def delete_skill(self, skill: Skill) -> None:
        await self.session.delete(skill)
