from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin


class SkillCategory(Base, TimestampMixin):
    __tablename__ = "skill_category"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True, nullable=False)
    name_en: Mapped[str] = mapped_column(String(120), nullable=False)
    name_it: Mapped[str] = mapped_column(String(120), nullable=False)
    description_en: Mapped[str | None] = mapped_column(Text, nullable=True)
    description_it: Mapped[str | None] = mapped_column(Text, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    # A simple on/off switch, not the full draft/publish state machine used
    # for long-form content — a skill list is a structured settings-like
    # list, not something that benefits from scheduling or revisions.
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)

    skills: Mapped[list[Skill]] = relationship(
        back_populates="category", order_by="Skill.sort_order", cascade="all, delete-orphan"
    )


class Skill(Base, TimestampMixin):
    __tablename__ = "skill"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("skill_category.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    context_en: Mapped[str | None] = mapped_column(
        Text, nullable=True, doc="How this skill has actually been applied."
    )
    context_it: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_featured: Mapped[bool] = mapped_column(Boolean, default=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    category: Mapped[SkillCategory] = relationship(back_populates="skills")
