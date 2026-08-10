from __future__ import annotations

from app.schemas.common import ORMModel


class SkillOut(ORMModel):
    name: str
    context: str | None


class SkillCategoryOut(ORMModel):
    slug: str
    name: str
    description: str | None
    skills: list[SkillOut]
