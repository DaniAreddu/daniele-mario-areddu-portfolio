from __future__ import annotations

from app.models.recognition import Recognition
from app.repositories.recognition_repository import RecognitionRepository
from app.schemas.recognition import RecognitionOut
from app.services.localization import pick


def to_recognition_out(recognition: Recognition, locale: str) -> RecognitionOut:
    return RecognitionOut(
        kind=recognition.kind,
        title=pick(recognition, "title", locale),
        issuer=recognition.issuer,
        description=(
            pick(recognition, "description", locale) if recognition.description_en else None
        ),
        date_awarded=recognition.date_awarded,
        url=recognition.url,
    )


class RecognitionService:
    def __init__(self, repository: RecognitionRepository) -> None:
        self.repository = repository

    async def list_all(self, locale: str) -> list[RecognitionOut]:
        items = await self.repository.list_all()
        return [to_recognition_out(item, locale) for item in items]
