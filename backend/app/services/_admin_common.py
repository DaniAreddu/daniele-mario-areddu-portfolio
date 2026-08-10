"""Shared helpers used by every admin service: audit logging (auth today;
content services from the Speaking vertical onward reuse it too) and the
generic revision-snapshot/restore mechanism.
"""

from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_event import AuditEvent
from app.models.revision import Revision


async def record_audit_event(
    session: AsyncSession,
    *,
    actor_id: int | None,
    action: str,
    entity_type: str | None = None,
    entity_id: int | None = None,
    summary: str = "",
    context: dict[str, Any] | None = None,
) -> None:
    """Append an audit log entry. Caller is responsible for committing —
    this only adds to the session, so it can be grouped atomically with the
    mutation it's describing.
    """
    session.add(
        AuditEvent(
            actor_id=actor_id,
            action=action,
            entity_type=entity_type,
            entity_id=entity_id,
            summary=summary,
            context=context or {},
        )
    )


def _json_safe(value: Any) -> Any:
    if isinstance(value, datetime | date):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    return value


def snapshot_entity(entity: Any) -> dict[str, Any]:
    """Serialize an ORM entity's scalar column values only — relationships
    (e.g. Event.tags) are never included, since a Revision snapshot exists to
    let content fields be restored, not to model full referential state.
    """
    mapper = sa.inspect(entity).mapper
    return {col.key: _json_safe(getattr(entity, col.key)) for col in mapper.column_attrs}


async def create_revision(
    session: AsyncSession,
    *,
    entity: Any,
    entity_type: str,
    entity_id: int,
    actor_id: int | None,
    schema_version: int = 1,
) -> None:
    """Snapshot `entity`'s CURRENT (pre-mutation) scalar column state.

    Must be called BEFORE any new values are assigned to `entity` — taking
    the snapshot after mutation would make every future "restore" a no-op,
    since it would just be a copy of the already-new state.
    """
    session.add(
        Revision(
            entity_type=entity_type,
            entity_id=entity_id,
            schema_version=schema_version,
            snapshot=snapshot_entity(entity),
            created_by_id=actor_id,
        )
    )


def merge_revision_snapshot(
    snapshot: dict[str, Any], allowed_fields: set[str]
) -> tuple[dict[str, Any], list[str]]:
    """Split an old Revision snapshot into (fields still valid to apply,
    fields that no longer exist on the current write schema).

    Restoring must never blindly replay a raw old snapshot — a field removed
    or renamed since the revision was taken would otherwise crash the
    restore or silently write to a stale column name. The caller is expected
    to overlay `applied` on top of the entity's *current* values (not the
    bare snapshot) so fields absent from an older snapshot aren't reset.
    """
    applied = {key: value for key, value in snapshot.items() if key in allowed_fields}
    ignored = [key for key in snapshot if key not in allowed_fields]
    return applied, ignored
