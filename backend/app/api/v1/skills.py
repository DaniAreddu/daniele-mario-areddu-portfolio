from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_skill_service
from app.schemas.skill import SkillCategoryOut
from app.services.skill_service import SkillService

router = APIRouter()


@router.get("/skills", response_model=list[SkillCategoryOut])
async def list_skills(
    locale: Locale, service: Annotated[SkillService, Depends(get_skill_service)]
) -> list[SkillCategoryOut]:
    return await service.list_categories(locale)
