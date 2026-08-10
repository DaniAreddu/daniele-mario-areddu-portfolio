from __future__ import annotations

from datetime import date

from app.schemas.common import ORMModel


class RecognitionOut(ORMModel):
    kind: str
    title: str
    issuer: str | None
    description: str | None
    date_awarded: date | None
    url: str | None
