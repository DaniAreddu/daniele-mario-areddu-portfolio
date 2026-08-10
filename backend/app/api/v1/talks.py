from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_talk_service
from app.schemas.talk import TalkOut
from app.services.talk_service import TalkService

router = APIRouter()


@router.get("/talks", response_model=list[TalkOut])
async def list_talks(
    locale: Locale, service: Annotated[TalkService, Depends(get_talk_service)]
) -> list[TalkOut]:
    return await service.list_all(locale)
