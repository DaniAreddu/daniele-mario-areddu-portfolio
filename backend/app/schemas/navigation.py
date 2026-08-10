from __future__ import annotations

from app.schemas.common import ORMModel


class NavigationItemOut(ORMModel):
    label: str
    target: str
    is_external: bool
    open_in_new_tab: bool


class NavigationOut(ORMModel):
    header: list[NavigationItemOut]
    footer: list[NavigationItemOut]
