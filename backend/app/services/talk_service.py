from __future__ import annotations

from app.repositories.talk_repository import TalkRepository
from app.schemas.talk import TalkOut
from app.services.localization import pick


class TalkService:
    def __init__(self, repository: TalkRepository) -> None:
        self.repository = repository

    async def list_all(self, locale: str) -> list[TalkOut]:
        talks = await self.repository.list_all()
        return [
            TalkOut(
                slug=talk.slug,
                title=talk.title,
                language=talk.language,
                summary=pick(talk, "summary", locale) if talk.summary_en else None,
                topics=talk.topics,
                is_featured=talk.is_featured,
                event_slugs=[event.slug for event in talk.events],
            )
            for talk in talks
        ]
