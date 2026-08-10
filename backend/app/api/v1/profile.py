from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_profile_service
from app.schemas.profile import ProfileOut
from app.services.profile_service import ProfileService

router = APIRouter()


@router.get("/profile", response_model=ProfileOut)
async def get_profile(
    locale: Locale, service: Annotated[ProfileService, Depends(get_profile_service)]
) -> ProfileOut:
    return await service.get_profile(locale)
