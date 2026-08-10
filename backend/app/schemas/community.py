from __future__ import annotations

from datetime import date

from app.schemas.common import ORMModel


class CommunityActivityOut(ORMModel):
    slug: str
    title: str
    description: str
    activity_date: date | None
    activity_type: str
    url: str | None


class CommunityProfileOut(ORMModel):
    name: str
    role: str
    mission: str
    description: str
    vision: str
    collaboration: str
    founded_year: int
    website_url: str | None
    activities: list[CommunityActivityOut]
