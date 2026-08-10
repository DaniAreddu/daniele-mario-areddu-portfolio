from __future__ import annotations

from app.schemas.common import ORMModel


class PassionOut(ORMModel):
    slug: str
    title: str
    text: str
    motif_label: str | None
