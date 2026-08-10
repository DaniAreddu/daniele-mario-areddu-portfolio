from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, Locale
from app.repositories.recognition_repository import RecognitionRepository
from app.schemas.recognition import RecognitionOut
from app.services.recognition_service import RecognitionService

router = APIRouter()


def get_recognition_service(session: DbSession) -> RecognitionService:
    return RecognitionService(RecognitionRepository(session))


@router.get("/recognition", response_model=list[RecognitionOut])
async def list_recognition(
    locale: Locale, service: Annotated[RecognitionService, Depends(get_recognition_service)]
) -> list[RecognitionOut]:
    # Never shows an empty-but-present section: if there are no published
    # entries of a given kind, the list is simply absent from the response,
    # and the public UI shouldn't render that section at all.
    return await service.list_all(locale)
