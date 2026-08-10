from __future__ import annotations

from app.schemas.common import ORMModel


class TalkOut(ORMModel):
    slug: str
    title: str
    language: str
    summary: str | None
    topics: list[str]
    is_featured: bool
    event_slugs: list[str]
