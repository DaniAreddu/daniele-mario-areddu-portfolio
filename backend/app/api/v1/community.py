from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_community_service
from app.schemas.community import CommunityProfileOut
from app.services.community_service import CommunityService

router = APIRouter()


@router.get("/community", response_model=CommunityProfileOut)
async def get_community(
    locale: Locale, service: Annotated[CommunityService, Depends(get_community_service)]
) -> CommunityProfileOut:
    return await service.get_profile(locale)
