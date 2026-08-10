from __future__ import annotations

from app.schemas.common import ORMModel


class EducationOut(ORMModel):
    institution: str
    degree: str
    location: str
    start_year: int | None
    end_year: int | None
    is_ongoing: bool
    description: str | None
