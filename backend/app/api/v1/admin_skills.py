from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession, require_admin_spa_header
from app.repositories.skill_repository import SkillRepository
from app.schemas.skill_admin import (
    SkillAdminOut,
    SkillAdminWrite,
    SkillCategoryAdminOut,
    SkillCategoryAdminWrite,
)
from app.services.skill_admin_service import SkillAdminService

router = APIRouter(prefix="/admin/skills")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_skill_admin_service(session: DbSession) -> SkillAdminService:
    return SkillAdminService(SkillRepository(session))


ServiceDep = Annotated[SkillAdminService, Depends(get_skill_admin_service)]


@router.get("/categories", response_model=list[SkillCategoryAdminOut])
async def list_categories(
    user: CurrentAdminUser, service: ServiceDep
) -> list[SkillCategoryAdminOut]:
    return await service.list_categories()


@router.post("/categories", response_model=SkillCategoryAdminOut, status_code=201)
async def create_category(
    payload: SkillCategoryAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> SkillCategoryAdminOut:
    return await service.create_category(payload, user)


@router.patch("/categories/{category_id}", response_model=SkillCategoryAdminOut)
async def update_category(
    category_id: int,
    payload: SkillCategoryAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> SkillCategoryAdminOut:
    return await service.update_category(category_id, payload, user)


@router.delete("/categories/{category_id}", status_code=204, response_model=None)
async def delete_category(
    category_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.delete_category(category_id, user)


@router.post("", response_model=SkillAdminOut, status_code=201)
async def create_skill(
    payload: SkillAdminWrite, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> SkillAdminOut:
    return await service.create_skill(payload, user)


@router.patch("/{skill_id}", response_model=SkillAdminOut)
async def update_skill(
    skill_id: int,
    payload: SkillAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> SkillAdminOut:
    return await service.update_skill(skill_id, payload, user)


@router.delete("/{skill_id}", status_code=204, response_model=None)
async def delete_skill(
    skill_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.delete_skill(skill_id, user)
