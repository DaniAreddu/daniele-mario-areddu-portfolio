from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_education_service
from app.schemas.education import EducationOut
from app.services.education_service import EducationService

router = APIRouter()


@router.get("/education", response_model=list[EducationOut])
async def list_education(
    locale: Locale, service: Annotated[EducationService, Depends(get_education_service)]
) -> list[EducationOut]:
    return await service.list_all(locale)
