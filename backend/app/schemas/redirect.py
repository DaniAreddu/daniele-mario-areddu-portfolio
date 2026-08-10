from __future__ import annotations

from app.schemas.common import ORMModel


class RedirectOut(ORMModel):
    source_path: str
    destination_path: str
    status_code: int
