from __future__ import annotations

from pydantic import BaseModel


class TagOut(BaseModel):
    slug: str
    label: str
