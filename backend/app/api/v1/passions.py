from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_passion_service
from app.schemas.passion import PassionOut
from app.services.passion_service import PassionService

router = APIRouter()


@router.get("/passions", response_model=list[PassionOut])
async def list_passions(
    locale: Locale, service: Annotated[PassionService, Depends(get_passion_service)]
) -> list[PassionOut]:
    return await service.list_all(locale)
