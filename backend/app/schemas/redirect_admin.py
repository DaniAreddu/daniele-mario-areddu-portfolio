from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, field_validator, model_validator

from app.schemas.common import ORMModel


class RedirectAdminWrite(BaseModel):
    source_path: str = Field(min_length=1, max_length=300)
    destination_path: str = Field(min_length=1, max_length=300)
    status_code: int = 301
    enabled: bool = True

    @field_validator("source_path", "destination_path")
    @classmethod
    def _validate_internal_path(cls, value: str) -> str:
        # Destinations are restricted to internal paths by construction —
        # no external redirect targets are supported, which eliminates
        # open-redirect risk rather than relying on an allowlist of hosts.
        if not value.startswith("/"):
            raise ValueError("Path must start with /")
        return value

    @field_validator("status_code")
    @classmethod
    def _validate_status_code(cls, value: int) -> int:
        if value not in (301, 302, 307, 308):
            raise ValueError("status_code must be one of 301, 302, 307, 308")
        return value

    @model_validator(mode="after")
    def _validate_not_self_referential(self) -> RedirectAdminWrite:
        if self.source_path == self.destination_path:
            raise ValueError("A redirect cannot point to itself.")
        return self


class RedirectAdminOut(ORMModel):
    id: int
    source_path: str
    destination_path: str
    status_code: int
    enabled: bool
    created_at: datetime
    updated_at: datetime
