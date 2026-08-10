from __future__ import annotations

from app.schemas.common import ORMModel


class SocialLinkOut(ORMModel):
    label: str
    url: str
    icon: str | None
