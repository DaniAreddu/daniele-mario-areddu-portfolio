from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field, model_validator

from app.schemas.common import ORMModel


class NavigationItemAdminWrite(BaseModel):
    label_en: str = Field(min_length=1, max_length=80)
    label_it: str = ""
    target: str = Field(min_length=1, max_length=255)
    placement: Literal["header", "footer"] = "header"
    is_external: bool = False
    open_in_new_tab: bool = False
    enabled: bool = True
    sort_order: int = 0

    @model_validator(mode="after")
    def _validate_target(self) -> NavigationItemAdminWrite:
        if self.is_external:
            if not (self.target.startswith("http://") or self.target.startswith("https://")):
                raise ValueError("External targets must start with http:// or https://")
        elif not self.target.startswith("/"):
            raise ValueError("Internal targets must start with /")
        return self


class NavigationItemAdminOut(ORMModel):
    id: int
    label_en: str
    label_it: str
    target: str
    placement: str
    is_external: bool
    open_in_new_tab: bool
    enabled: bool
    sort_order: int
    created_at: datetime
    updated_at: datetime
