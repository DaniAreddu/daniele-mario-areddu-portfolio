from __future__ import annotations

from app.models.audit_event import AuditEvent
from app.models.revision import Revision
from app.repositories.audit_event_repository import AuditEventRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.audit_admin import AuditEventOut, RevisionSummaryOut


def to_audit_event_out(event: AuditEvent) -> AuditEventOut:
    return AuditEventOut(
        id=event.id,
        actor_email=event.actor.email if event.actor else None,
        action=event.action,
        entity_type=event.entity_type,
        entity_id=event.entity_id,
        summary=event.summary,
        context=event.context,
        created_at=event.created_at,
    )


def _to_revision_out(revision: Revision) -> RevisionSummaryOut:
    return RevisionSummaryOut(
        id=revision.id,
        entity_type=revision.entity_type,
        entity_id=revision.entity_id,
        created_by_email=revision.created_by.email if revision.created_by else None,
        created_at=revision.created_at,
    )


class AuditAdminService:
    def __init__(
        self, audit_repository: AuditEventRepository, revision_repository: RevisionRepository
    ) -> None:
        self.audit_repository = audit_repository
        self.revision_repository = revision_repository

    async def list_audit_events(
        self, *, entity_type: str | None = None, limit: int = 50, offset: int = 0
    ) -> list[AuditEventOut]:
        events = await self.audit_repository.list_all(
            entity_type=entity_type, limit=limit, offset=offset
        )
        return [to_audit_event_out(event) for event in events]

    async def list_recent_revisions(self, limit: int = 20) -> list[RevisionSummaryOut]:
        revisions = await self.revision_repository.list_recent(limit)
        return [_to_revision_out(revision) for revision in revisions]
