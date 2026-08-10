"""Admin CRUD for Skills — plain create/update/delete/reorder, no
draft/publish/revision machinery. A skill list is a structured settings-like
list (see docs/admin-guide.md), not long-form content that benefits from
scheduling or point-in-time restore; a simple `enabled` switch is enough.
Audit logging still applies to every mutation.
"""

from __future__ import annotations

from app.core.errors import AppError, NotFoundError
from app.models.admin_user import AdminUser
from app.models.skill import Skill, SkillCategory
from app.repositories.skill_repository import SkillRepository
from app.schemas.skill_admin import (
    SkillAdminOut,
    SkillAdminWrite,
    SkillCategoryAdminOut,
    SkillCategoryAdminWrite,
)
from app.services._admin_common import record_audit_event


def _to_skill_out(skill: Skill) -> SkillAdminOut:
    return SkillAdminOut(
        id=skill.id,
        category_id=skill.category_id,
        name=skill.name,
        context_en=skill.context_en,
        context_it=skill.context_it,
        is_featured=skill.is_featured,
        enabled=skill.enabled,
        sort_order=skill.sort_order,
    )


def _to_category_out(category: SkillCategory) -> SkillCategoryAdminOut:
    return SkillCategoryAdminOut(
        id=category.id,
        slug=category.slug,
        name_en=category.name_en,
        name_it=category.name_it,
        description_en=category.description_en,
        description_it=category.description_it,
        sort_order=category.sort_order,
        enabled=category.enabled,
        skills=[
            _to_skill_out(skill) for skill in sorted(category.skills, key=lambda s: s.sort_order)
        ],
    )


class SkillAdminService:
    def __init__(self, repository: SkillRepository) -> None:
        self.repository = repository

    async def list_categories(self) -> list[SkillCategoryAdminOut]:
        categories = await self.repository.list_categories_admin()
        return [_to_category_out(category) for category in categories]

    async def _get_category_or_404(self, category_id: int) -> SkillCategory:
        category = await self.repository.get_category_by_id(category_id)
        if category is None:
            raise NotFoundError("Skill category not found.")
        return category

    async def create_category(
        self, payload: SkillCategoryAdminWrite, actor: AdminUser
    ) -> SkillCategoryAdminOut:
        if await self.repository.get_category_by_slug_any(payload.slug) is not None:
            raise AppError("A skill category with this slug already exists.", code="slug_conflict")
        category = SkillCategory(**payload.model_dump())
        await self.repository.create_category(category)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="skill_category.create",
            entity_type="skill_category",
            entity_id=category.id,
            summary=f"Created skill category '{category.name_en}'",
        )
        await self.repository.session.commit()
        # A brand-new category has no `skills` relationship loaded yet — an
        # unguarded access below would attempt an implicit (sync) lazy-load
        # and crash under the async driver.
        await self.repository.session.refresh(category, attribute_names=["skills"])
        return _to_category_out(category)

    async def update_category(
        self, category_id: int, payload: SkillCategoryAdminWrite, actor: AdminUser
    ) -> SkillCategoryAdminOut:
        category = await self._get_category_or_404(category_id)
        for field, value in payload.model_dump().items():
            setattr(category, field, value)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="skill_category.update",
            entity_type="skill_category",
            entity_id=category.id,
            summary=f"Updated skill category '{category.name_en}'",
        )
        await self.repository.session.commit()
        return _to_category_out(category)

    async def delete_category(self, category_id: int, actor: AdminUser) -> None:
        category = await self._get_category_or_404(category_id)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="skill_category.delete",
            entity_type="skill_category",
            entity_id=category.id,
            summary=f"Deleted skill category '{category.name_en}'",
        )
        await self.repository.delete_category(category)
        await self.repository.session.commit()

    async def create_skill(self, payload: SkillAdminWrite, actor: AdminUser) -> SkillAdminOut:
        await self._get_category_or_404(payload.category_id)
        skill = Skill(**payload.model_dump())
        await self.repository.create_skill(skill)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="skill.create",
            entity_type="skill",
            entity_id=skill.id,
            summary=f"Created skill '{skill.name}'",
        )
        await self.repository.session.commit()
        return _to_skill_out(skill)

    async def update_skill(
        self, skill_id: int, payload: SkillAdminWrite, actor: AdminUser
    ) -> SkillAdminOut:
        skill = await self.repository.get_skill_by_id(skill_id)
        if skill is None:
            raise NotFoundError("Skill not found.")
        for field, value in payload.model_dump().items():
            setattr(skill, field, value)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="skill.update",
            entity_type="skill",
            entity_id=skill.id,
            summary=f"Updated skill '{skill.name}'",
        )
        await self.repository.session.commit()
        return _to_skill_out(skill)

    async def delete_skill(self, skill_id: int, actor: AdminUser) -> None:
        skill = await self.repository.get_skill_by_id(skill_id)
        if skill is None:
            raise NotFoundError("Skill not found.")
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="skill.delete",
            entity_type="skill",
            entity_id=skill.id,
            summary=f"Deleted skill '{skill.name}'",
        )
        await self.repository.delete_skill(skill)
        await self.repository.session.commit()
