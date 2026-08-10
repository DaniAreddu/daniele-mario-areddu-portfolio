from __future__ import annotations

from pydantic import BaseModel


class SearchResultOut(BaseModel):
    entity_type: str
    entity_id: int
    title: str
    admin_path: str
