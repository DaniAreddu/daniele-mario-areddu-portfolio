from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_experience_service
from app.schemas.experience import ExperienceOut
from app.services.experience_service import ExperienceService

router = APIRouter()


@router.get("/experiences", response_model=list[ExperienceOut])
async def list_experiences(
    locale: Locale, service: Annotated[ExperienceService, Depends(get_experience_service)]
) -> list[ExperienceOut]:
    return await service.list_all(locale)
