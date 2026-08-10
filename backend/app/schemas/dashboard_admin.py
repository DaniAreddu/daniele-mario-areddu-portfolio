from __future__ import annotations

from pydantic import BaseModel

from app.schemas.audit_admin import AuditEventOut


class ContentTypeCounts(BaseModel):
    published: int
    draft: int
    scheduled: int
    archived: int
    trashed: int


class DashboardStatsOut(BaseModel):
    events: ContentTypeCounts
    projects: ContentTypeCounts
    experience: ContentTypeCounts
    education: ContentTypeCounts
    community_activities: ContentTypeCounts
    recognition: ContentTypeCounts
    media_count: int
    upcoming_events_count: int
    recent_activity: list[AuditEventOut]
