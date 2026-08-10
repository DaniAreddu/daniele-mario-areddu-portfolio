from __future__ import annotations

from datetime import datetime
from typing import Any

from app.schemas.common import ORMModel


class AuditEventOut(ORMModel):
    id: int
    actor_email: str | None
    action: str
    entity_type: str | None
    entity_id: int | None
    summary: str
    context: dict[str, Any]
    created_at: datetime


class RevisionSummaryOut(ORMModel):
    id: int
    entity_type: str
    entity_id: int
    created_by_email: str | None
    created_at: datetime
