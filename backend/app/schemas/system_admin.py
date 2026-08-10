from __future__ import annotations

from pydantic import BaseModel


class SystemHealthOut(BaseModel):
    database_ok: bool
    migration_status: str
    """One of: "up_to_date", "behind", "unknown"."""
    current_migration: str | None
    head_migration: str | None
    storage_ok: bool
    storage_backend: str
