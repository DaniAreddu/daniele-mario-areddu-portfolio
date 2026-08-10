from __future__ import annotations

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel


class SkillAdminWrite(BaseModel):
    category_id: int
    name: str = Field(min_length=1, max_length=120)
    context_en: str | None = None
    context_it: str | None = None
    is_featured: bool = False
    enabled: bool = True
    sort_order: int = 0


class SkillAdminOut(ORMModel):
    id: int
    category_id: int
    name: str
    context_en: str | None
    context_it: str | None
    is_featured: bool
    enabled: bool
    sort_order: int


class SkillCategoryAdminWrite(BaseModel):
    slug: str = Field(min_length=1, max_length=80, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
    name_en: str = Field(min_length=1, max_length=120)
    name_it: str = ""
    description_en: str | None = None
    description_it: str | None = None
    sort_order: int = 0
    enabled: bool = True


class SkillCategoryAdminOut(ORMModel):
    id: int
    slug: str
    name_en: str
    name_it: str
    description_en: str | None
    description_it: str | None
    sort_order: int
    enabled: bool
    skills: list[SkillAdminOut]
