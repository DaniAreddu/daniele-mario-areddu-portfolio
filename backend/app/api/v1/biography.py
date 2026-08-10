from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_profile_service
from app.schemas.profile import BiographyOut
from app.services.profile_service import ProfileService

router = APIRouter()


@router.get("/biography", response_model=BiographyOut)
async def get_biography(
    locale: Locale, service: Annotated[ProfileService, Depends(get_profile_service)]
) -> BiographyOut:
    return await service.get_biography(locale)
