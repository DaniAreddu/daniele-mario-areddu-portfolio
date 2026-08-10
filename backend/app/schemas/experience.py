from __future__ import annotations

from datetime import date

from app.schemas.common import ORMModel


class ExperienceOut(ORMModel):
    organization: str
    role: str
    location: str
    start_date: date
    end_date: date | None
    is_current: bool
    summary: str
    highlights: list[str]
    technologies: list[str]
