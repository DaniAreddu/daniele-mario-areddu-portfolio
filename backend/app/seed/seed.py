"""Idempotent seed script.

Run with: `python -m app.seed.seed` (or `make seed`).
Safe to re-run: existing rows are matched by their natural key (slug, or
singleton for profile/biography/community_profile) and updated in place
rather than duplicated.
"""

from __future__ import annotations

import asyncio
import re
from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logging import configure_logging, get_logger
from app.db.session import dispose_engine, get_session_factory
from app.models.community import CommunityActivity, CommunityProfile
from app.models.education import Education
from app.models.event import Event
from app.models.experience import Experience
from app.models.navigation_item import NavigationItem
from app.models.passion import Passion
from app.models.profile import Biography, Profile
from app.models.project import Project, ProjectSkill
from app.models.site_settings import HomepageFeature, HomepageSettings
from app.models.skill import Skill, SkillCategory
from app.models.tag import Tag, event_tag, experience_tag, project_tag
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
        item = dict(item)
        item.setdefault("publication_status", "PUBLISHED")
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
        item = dict(item)
        item.setdefault("publication_status", "PUBLISHED")
        result = await session.execute(
            select(Experience).where(
                Experience.organization == item["organization"],
                Experience.role_en == item["role_en"],
            )
        )
        instance = result.scalars().first()
        if instance is None:
            instance = Experience(**item)
            session.add(instance)
            await session.flush()
        else:
            for key, value in item.items():
                setattr(instance, key, value)
            await session.flush()
        await _seed_tags_for(
            session, experience_tag, "experience_id", instance.id, item.get("technologies", [])
        )


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
        # Seed data represents already-known, already-public content, not an
        # admin's in-progress draft — see the matching comment in
        # _seed_events for why this must be set explicitly.
        item.setdefault("publication_status", "PUBLISHED")
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

        await _seed_tags_for(
            session, project_tag, "project_id", project.id, item.get("technologies", [])
        )


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
        # Seed data represents already-known, already-public content (see
        # docs/architecture.md) — not an admin's in-progress draft — so it
        # must be immediately visible, matching how the 0004 migration
        # backfills PUBLISHED for existing production rows. Without this,
        # every seeded event would fall back to the model's DRAFT default
        # and vanish from every public endpoint.
        item.setdefault("publication_status", "PUBLISHED")

        result = await session.execute(select(Event).where(Event.slug == item["slug"]))
        event = result.scalars().first()
        if event is None:
            event = Event(**item)
            session.add(event)
            await session.flush()
        else:
            for key, value in item.items():
                setattr(event, key, value)
            await session.flush()
        await _seed_tags_for(session, event_tag, "event_id", event.id, item.get("topics", []))


def _slugify_tag(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


async def _seed_tags_for(
    session: AsyncSession, association_table: Any, id_column: str, entity_id: int, labels: list[str]
) -> None:
    """Populates the normalized Tag/<entity>_tag rows from a legacy
    JSON label list, so a freshly-seeded dev/test database has the same
    admin-manageable tag data that the matching migration backfills for real
    accumulated production data. Shared by events (topics) and projects
    (technologies) — the whole point of one Tag vocabulary is that a label
    used by both resolves to the same row. Idempotent: re-running never
    inserts a duplicate (entity_id, tag_id) pair.
    """
    if not labels:
        return

    existing_pairs = await session.execute(
        select(association_table.c.tag_id).where(
            getattr(association_table.c, id_column) == entity_id
        )
    )
    existing_tag_ids = {row[0] for row in existing_pairs}

    for raw_label in labels:
        label = raw_label.strip()
        if not label:
            continue
        slug = _slugify_tag(label)
        if not slug:
            continue

        result = await session.execute(select(Tag).where(Tag.slug == slug))
        tag = result.scalars().first()
        if tag is None:
            tag = Tag(slug=slug, label=label)
            session.add(tag)
            await session.flush()

        if tag.id not in existing_tag_ids:
            await session.execute(
                insert(association_table).values(**{id_column: entity_id, "tag_id": tag.id})
            )
            existing_tag_ids.add(tag.id)


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
        item = dict(item)
        item.setdefault("publication_status", "PUBLISHED")
        result = await session.execute(
            select(CommunityActivity).where(CommunityActivity.slug == item["slug"])
        )
        instance = result.scalars().first()
        if instance is None:
            session.add(CommunityActivity(**item))
        else:
            for key, value in item.items():
                setattr(instance, key, value)


_DEFAULT_NAV_ITEMS: list[dict[str, Any]] = [
    {"label_en": "Home", "label_it": "Home", "target": "/", "placement": "header", "sort_order": 0},
    {
        "label_en": "About",
        "label_it": "Chi sono",
        "target": "/about",
        "placement": "header",
        "sort_order": 1,
    },
    {
        "label_en": "Journey",
        "label_it": "Percorso",
        "target": "/journey",
        "placement": "header",
        "sort_order": 2,
    },
    {
        "label_en": "Projects",
        "label_it": "Progetti",
        "target": "/projects",
        "placement": "header",
        "sort_order": 3,
    },
    {
        "label_en": "Speaking",
        "label_it": "Speaking",
        "target": "/speaking",
        "placement": "header",
        "sort_order": 4,
    },
    {
        "label_en": "Community",
        "label_it": "Community",
        "target": "/community",
        "placement": "header",
        "sort_order": 5,
    },
    {
        "label_en": "Contact",
        "label_it": "Contatti",
        "target": "/contact",
        "placement": "header",
        "sort_order": 6,
    },
    {
        "label_en": "Privacy",
        "label_it": "Privacy",
        "target": "/privacy",
        "placement": "footer",
        "sort_order": 0,
    },
]

# Talk slug -> the specific event delivering it that best represents "featured
# speaking appearance" on the homepage, resolved at seed time (see
# _seed_homepage) since Talk itself has no public detail page to link to.
_FEATURED_EVENT_SLUGS = ["gdg-almaty-2026", "agentcamp-sofia-2026", "devfest-vicenza-2026"]
_FEATURED_PROJECT_SLUGS = [
    "municipal-data-reconciliation-platform",
    "production-ai-agent-architectures",
]


async def _seed_navigation(session: AsyncSession) -> None:
    """One-time bootstrap only: populates the CMS-managed navigation from the
    site's original hardcoded nav (`Nav.tsx`'s old static `NAV_ITEMS` plus the
    footer's Privacy link) so the public site's menu is unchanged the moment
    NavigationItem-driven rendering ships.

    Unlike `_seed_profile`/`_seed_community` above, this is deliberately NOT
    re-applied once any navigation item already exists — Navigation is meant
    to become fully admin-owned after this one-time migration (including
    admin deletions staying deleted), not perpetually reset by re-running the
    seed script.
    """
    existing = await session.execute(select(NavigationItem.id).limit(1))
    if existing.scalars().first() is not None:
        return
    for item in _DEFAULT_NAV_ITEMS:
        session.add(
            NavigationItem(**item, is_external=False, open_in_new_tab=False, enabled=True)
        )


async def _seed_homepage(session: AsyncSession) -> None:
    """One-time bootstrap only, same rationale as `_seed_navigation`: copies
    the site's original hardcoded hero copy/CTAs (previously living directly
    in `HomePage.tsx`, plus `Profile.positioning_statement_*` for the
    subheadline) into the CMS `HomepageSettings` singleton, and pins the
    projects/talks that were previously featured via ad-hoc `is_featured`
    flags as CMS-managed `HomepageFeature` rows. Only runs while the
    singleton is still in its untouched default state / the feature list is
    still empty — an admin's homepage edits are never overwritten by re-
    running the seed.
    """
    result = await session.execute(select(HomepageSettings).limit(1))
    settings = result.scalars().first()
    if settings is None:
        settings = HomepageSettings()
        session.add(settings)
        await session.flush()

    if not settings.hero_headline_en:
        settings.hero_eyebrow_en = PROFILE["brand_label"]
        settings.hero_eyebrow_it = PROFILE["brand_label"]
        settings.hero_headline_en = (
            "Building intelligent systems.\nSharing what I learn around the world."
        )
        settings.hero_headline_it = (
            "Costruisco sistemi intelligenti.\nCondivido ciò che imparo in giro per il mondo."
        )
        settings.hero_subheadline_en = PROFILE["positioning_statement_en"]
        settings.hero_subheadline_it = PROFILE["positioning_statement_it"]
        settings.primary_cta_label_en = "Explore my work"
        settings.primary_cta_label_it = "Esplora i miei lavori"
        settings.primary_cta_url = "/projects"
        settings.secondary_cta_label_en = "Invite me to speak"
        settings.secondary_cta_label_it = "Invitami a parlare"
        settings.secondary_cta_url = "/contact"
        settings.section_order = ["about", "journey", "speaking", "projects", "community"]
        settings.section_visibility = {
            "about": True,
            "journey": True,
            "speaking": True,
            "projects": True,
            "community": True,
        }

    existing_features = await session.execute(select(HomepageFeature.id).limit(1))
    if existing_features.scalars().first() is not None:
        return

    for slug in _FEATURED_PROJECT_SLUGS:
        project_result = await session.execute(select(Project.id).where(Project.slug == slug))
        project_id = project_result.scalars().first()
        if project_id is not None:
            session.add(HomepageFeature(entity_type="project", entity_id=project_id))

    for slug in _FEATURED_EVENT_SLUGS:
        event_result = await session.execute(select(Event.id).where(Event.slug == slug))
        event_id = event_result.scalars().first()
        if event_id is not None:
            session.add(HomepageFeature(entity_type="event", entity_id=event_id))


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
        await _seed_navigation(session)
        await _seed_homepage(session)
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
