"""Idempotent seed script.

Run with: `python -m app.seed.seed` (or `make seed`).
Safe to re-run: existing rows are matched by their natural key (slug, or
singleton for profile/biography/community_profile) and updated in place
rather than duplicated.
"""

from __future__ import annotations

import asyncio
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import configure_logging, get_logger
from app.db.session import dispose_engine, get_session_factory
from app.models.community import CommunityActivity, CommunityProfile
from app.models.education import Education
from app.models.event import Event
from app.models.experience import Experience
from app.models.passion import Passion
from app.models.profile import Biography, Profile
from app.models.project import Project, ProjectSkill
from app.models.skill import Skill, SkillCategory
from app.models.talk import Talk
from app.seed.data import (
    BIOGRAPHY,
    COMMUNITY_ACTIVITIES,
    COMMUNITY_PROFILE,
    EDUCATION,
    EVENTS,
    EXPERIENCE,
    PASSIONS,
    PROFILE,
    PROJECTS,
    SKILL_CATEGORIES,
    TALKS,
)

logger = get_logger(__name__)


async def _upsert_singleton(session: AsyncSession, model: type[Any], data: dict[str, Any]) -> None:
    result: Any = await session.execute(select(model).limit(1))
    instance = result.scalars().first()
    if instance is None:
        session.add(model(**data))
    else:
        for key, value in data.items():
            setattr(instance, key, value)


async def _seed_profile(session: AsyncSession) -> None:
    await _upsert_singleton(session, Profile, PROFILE)
    await _upsert_singleton(session, Biography, BIOGRAPHY)


async def _seed_education(session: AsyncSession) -> None:
    for item in EDUCATION:
        result = await session.execute(
            select(Education).where(
                Education.institution == item["institution"],
                Education.degree_en == item["degree_en"],
            )
        )
        instance = result.scalars().first()
        if instance is None:
            session.add(Education(**item))
        else:
            for key, value in item.items():
                setattr(instance, key, value)


async def _seed_experience(session: AsyncSession) -> None:
    for item in EXPERIENCE:
        result = await session.execute(
            select(Experience).where(
                Experience.organization == item["organization"],
                Experience.role_en == item["role_en"],
            )
        )
        instance = result.scalars().first()
        if instance is None:
            session.add(Experience(**item))
        else:
            for key, value in item.items():
                setattr(instance, key, value)


async def _seed_skills(session: AsyncSession) -> None:
    for category_data in SKILL_CATEGORIES:
        skills = category_data.pop("skills")
        result = await session.execute(
            select(SkillCategory).where(SkillCategory.slug == category_data["slug"])
        )
        category = result.scalars().first()
        if category is None:
            category = SkillCategory(**category_data)
            session.add(category)
            await session.flush()
        else:
            for key, value in category_data.items():
                setattr(category, key, value)

        existing_result = await session.execute(
            select(Skill).where(Skill.category_id == category.id)
        )
        existing_by_name = {skill.name: skill for skill in existing_result.scalars().all()}

        for order, (name, context_en, context_it) in enumerate(skills):
            skill = existing_by_name.get(name)
            if skill is None:
                session.add(
                    Skill(
                        category_id=category.id,
                        name=name,
                        context_en=context_en,
                        context_it=context_it,
                        sort_order=order,
                    )
                )
            else:
                skill.context_en = context_en
                skill.context_it = context_it
                skill.sort_order = order

        category_data["skills"] = skills  # restore for idempotent re-runs in-process


async def _seed_projects(session: AsyncSession) -> None:
    for item in PROJECTS:
        item = dict(item)
        related_skills = item.pop("related_skills")
        result = await session.execute(select(Project).where(Project.slug == item["slug"]))
        project = result.scalars().first()
        if project is None:
            project = Project(**item)
            session.add(project)
            await session.flush()
        else:
            for key, value in item.items():
                setattr(project, key, value)

        existing_result = await session.execute(
            select(ProjectSkill).where(ProjectSkill.project_id == project.id)
        )
        existing_names = {row.skill_name for row in existing_result.scalars().all()}
        for skill_name in related_skills:
            if skill_name not in existing_names:
                session.add(ProjectSkill(project_id=project.id, skill_name=skill_name))


async def _seed_talks(session: AsyncSession) -> dict[str, int]:
    slug_to_id: dict[str, int] = {}
    for item in TALKS:
        result = await session.execute(select(Talk).where(Talk.slug == item["slug"]))
        talk = result.scalars().first()
        if talk is None:
            talk = Talk(**item)
            session.add(talk)
            await session.flush()
        else:
            for key, value in item.items():
                setattr(talk, key, value)
        slug_to_id[item["slug"]] = talk.id
    return slug_to_id


async def _seed_events(session: AsyncSession, talk_slug_to_id: dict[str, int]) -> None:
    for item in EVENTS:
        item = dict(item)
        talk_slug = item.pop("talk_slug")
        item["talk_id"] = talk_slug_to_id.get(talk_slug) if talk_slug else None
        item.setdefault("short_description_en", None)
        item.setdefault("short_description_it", None)
        item.setdefault("full_description_en", None)
        item.setdefault("full_description_it", None)
        item.setdefault("session_title", None)
        item.setdefault("event_url", None)
        item.setdefault("slides_url", None)
        item.setdefault("recording_url", None)
        item.setdefault("image", None)

        result = await session.execute(select(Event).where(Event.slug == item["slug"]))
        event = result.scalars().first()
        if event is None:
            session.add(Event(**item))
        else:
            for key, value in item.items():
                setattr(event, key, value)


async def _seed_passions(session: AsyncSession) -> None:
    for item in PASSIONS:
        result = await session.execute(select(Passion).where(Passion.slug == item["slug"]))
        instance = result.scalars().first()
        if instance is None:
            session.add(Passion(**item))
        else:
            for key, value in item.items():
                setattr(instance, key, value)


async def _seed_community(session: AsyncSession) -> None:
    await _upsert_singleton(session, CommunityProfile, COMMUNITY_PROFILE)
    for item in COMMUNITY_ACTIVITIES:
        result = await session.execute(
            select(CommunityActivity).where(CommunityActivity.slug == item["slug"])
        )
        instance = result.scalars().first()
        if instance is None:
            session.add(CommunityActivity(**item))
        else:
            for key, value in item.items():
                setattr(instance, key, value)


async def seed_all() -> None:
    configure_logging()
    session_factory = get_session_factory()
    async with session_factory() as session:
        await _seed_profile(session)
        await _seed_education(session)
        await _seed_experience(session)
        await _seed_skills(session)
        talk_slug_to_id = await _seed_talks(session)
        await _seed_events(session, talk_slug_to_id)
        await _seed_projects(session)
        await _seed_passions(session)
        await _seed_community(session)
        await session.commit()
    logger.info("seed_completed")


def main() -> None:
    asyncio.run(_run())


async def _run() -> None:
    try:
        await seed_all()
    finally:
        await dispose_engine()


if __name__ == "__main__":
    main()
