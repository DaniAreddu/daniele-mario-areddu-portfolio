from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentAdminUser, DbSession
from app.repositories.audit_event_repository import AuditEventRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.audit_admin import AuditEventOut, RevisionSummaryOut
from app.services.audit_admin_service import AuditAdminService

router = APIRouter(prefix="/admin")


def get_audit_admin_service(session: DbSession) -> AuditAdminService:
    return AuditAdminService(AuditEventRepository(session), RevisionRepository(session))


ServiceDep = Annotated[AuditAdminService, Depends(get_audit_admin_service)]


@router.get("/audit-log", response_model=list[AuditEventOut])
async def list_audit_log(
    user: CurrentAdminUser,
    service: ServiceDep,
    entity_type: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> list[AuditEventOut]:
    return await service.list_audit_events(entity_type=entity_type, limit=limit, offset=offset)


@router.get("/revisions/recent", response_model=list[RevisionSummaryOut])
async def list_recent_revisions(
    user: CurrentAdminUser,
    service: ServiceDep,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
) -> list[RevisionSummaryOut]:
    return await service.list_recent_revisions(limit)
