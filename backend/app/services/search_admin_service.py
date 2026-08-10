"""Global admin search — a small fan-out of ILIKE queries across the
title-like column of each content type. Good enough for a single-operator
portfolio's dataset (a few hundred rows at most); not built to scale to a
large multi-tenant corpus.
"""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.community import CommunityActivity
from app.models.education import Education
from app.models.event import Event
from app.models.experience import Experience
from app.models.media_asset import MediaAsset
from app.models.navigation_item import NavigationItem
from app.models.project import Project
from app.models.recognition import Recognition
from app.models.social_link import SocialLink
from app.schemas.search_admin import SearchResultOut

_LIMIT_PER_TYPE = 8


class SearchAdminService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def search(self, query: str) -> list[SearchResultOut]:
        pattern = f"%{query}%"
        results: list[SearchResultOut] = []

        event_rows = await self.session.execute(
            select(Event.id, Event.event_name)
            .where(Event.event_name.ilike(pattern), Event.deleted_at.is_(None))
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="event", entity_id=row.id, title=row.event_name,
                admin_path=f"/admin/speaking/{row.id}",
            )
            for row in event_rows
        ]

        project_rows = await self.session.execute(
            select(Project.id, Project.title_en)
            .where(Project.title_en.ilike(pattern), Project.deleted_at.is_(None))
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="project", entity_id=row.id, title=row.title_en,
                admin_path=f"/admin/projects/{row.id}",
            )
            for row in project_rows
        ]

        experience_rows = await self.session.execute(
            select(Experience.id, Experience.organization)
            .where(Experience.organization.ilike(pattern), Experience.deleted_at.is_(None))
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="experience", entity_id=row.id, title=row.organization,
                admin_path=f"/admin/experience/{row.id}",
            )
            for row in experience_rows
        ]

        education_rows = await self.session.execute(
            select(Education.id, Education.institution)
            .where(Education.institution.ilike(pattern), Education.deleted_at.is_(None))
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="education", entity_id=row.id, title=row.institution,
                admin_path=f"/admin/education/{row.id}",
            )
            for row in education_rows
        ]

        activity_rows = await self.session.execute(
            select(CommunityActivity.id, CommunityActivity.title_en)
            .where(
                CommunityActivity.title_en.ilike(pattern), CommunityActivity.deleted_at.is_(None)
            )
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="community_activity", entity_id=row.id, title=row.title_en,
                admin_path=f"/admin/community/{row.id}",
            )
            for row in activity_rows
        ]

        recognition_rows = await self.session.execute(
            select(Recognition.id, Recognition.title_en)
            .where(Recognition.title_en.ilike(pattern), Recognition.deleted_at.is_(None))
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="recognition", entity_id=row.id, title=row.title_en,
                admin_path=f"/admin/recognition/{row.id}",
            )
            for row in recognition_rows
        ]

        media_rows = await self.session.execute(
            select(MediaAsset.id, MediaAsset.original_filename)
            .where(MediaAsset.original_filename.ilike(pattern))
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="media_asset", entity_id=row.id, title=row.original_filename,
                admin_path="/admin/media",
            )
            for row in media_rows
        ]

        nav_rows = await self.session.execute(
            select(NavigationItem.id, NavigationItem.label_en)
            .where(NavigationItem.label_en.ilike(pattern))
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="navigation_item", entity_id=row.id, title=row.label_en,
                admin_path="/admin/navigation",
            )
            for row in nav_rows
        ]

        social_rows = await self.session.execute(
            select(SocialLink.id, SocialLink.label)
            .where(SocialLink.label.ilike(pattern))
            .limit(_LIMIT_PER_TYPE)
        )
        results += [
            SearchResultOut(
                entity_type="social_link", entity_id=row.id, title=row.label,
                admin_path="/admin/social-links",
            )
            for row in social_rows
        ]

        return results
