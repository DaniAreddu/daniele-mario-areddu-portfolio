"""Real, computed-on-demand dashboard metrics — never hardcoded or cached
stale, so the numbers can never drift from the actual database state.
"""

from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import PublishableMixin
from app.db.filters import visible_now
from app.models.community import CommunityActivity
from app.models.education import Education
from app.models.event import Event
from app.models.experience import Experience
from app.models.media_asset import MediaAsset
from app.models.project import Project
from app.models.recognition import Recognition
from app.repositories.audit_event_repository import AuditEventRepository
from app.schemas.dashboard_admin import ContentTypeCounts, DashboardStatsOut
from app.services.audit_admin_service import to_audit_event_out


async def _count_by_status(
    session: AsyncSession, model: type[PublishableMixin]
) -> ContentTypeCounts:
    result = await session.execute(
        select(model.publication_status, func.count())
        .where(model.deleted_at.is_(None))  # type: ignore[attr-defined]
        .group_by(model.publication_status)
    )
    by_status: dict[str, int] = dict(result.all())  # type: ignore[arg-type]
    trashed_result = await session.execute(
        select(func.count())
        .select_from(model)
        .where(model.deleted_at.is_not(None))  # type: ignore[attr-defined]
    )
    return ContentTypeCounts(
        published=by_status.get("PUBLISHED", 0),
        draft=by_status.get("DRAFT", 0),
        scheduled=by_status.get("SCHEDULED", 0),
        archived=by_status.get("ARCHIVED", 0),
        trashed=trashed_result.scalar_one(),
    )


class DashboardAdminService:
    def __init__(self, session: AsyncSession, audit_repository: AuditEventRepository) -> None:
        self.session = session
        self.audit_repository = audit_repository

    async def get_stats(self) -> DashboardStatsOut:
        media_count_result = await self.session.execute(
            select(func.count()).select_from(MediaAsset)
        )
        upcoming_result = await self.session.execute(
            select(func.count())
            .select_from(Event)
            .where(Event.status.in_(["upcoming", "incoming"]), visible_now(Event))
        )
        recent_events = await self.audit_repository.list_recent(limit=15)

        return DashboardStatsOut(
            events=await _count_by_status(self.session, Event),
            projects=await _count_by_status(self.session, Project),
            experience=await _count_by_status(self.session, Experience),
            education=await _count_by_status(self.session, Education),
            community_activities=await _count_by_status(self.session, CommunityActivity),
            recognition=await _count_by_status(self.session, Recognition),
            media_count=media_count_result.scalar_one(),
            upcoming_events_count=upcoming_result.scalar_one(),
            recent_activity=[to_audit_event_out(event) for event in recent_events],
        )
