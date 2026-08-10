from __future__ import annotations

from pydantic import BaseModel


class JourneyMilestoneOut(BaseModel):
    year: int | None
    title: str
    text: str
    kind: str
    event_slug: str | None = None
