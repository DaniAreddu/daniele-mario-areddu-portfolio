from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MediaAssetOut(BaseModel):
    id: int
    storage_key: str
    url: str
    original_filename: str
    mime_type: str
    size_bytes: int
    width: int | None
    height: int | None
    alt_text: str | None
    caption: str | None
    variants: dict[str, str]
    uploaded_by_email: str | None
    created_at: datetime


class MediaAssetUpdate(BaseModel):
    alt_text: str | None = None
    caption: str | None = None


class MediaUsageOut(BaseModel):
    reference_count: int
    referenced_in: list[str]
