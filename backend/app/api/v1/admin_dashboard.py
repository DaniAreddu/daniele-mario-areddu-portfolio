from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession
from app.repositories.audit_event_repository import AuditEventRepository
from app.schemas.dashboard_admin import DashboardStatsOut
from app.services.dashboard_admin_service import DashboardAdminService

router = APIRouter(prefix="/admin")


def get_dashboard_admin_service(session: DbSession) -> DashboardAdminService:
    return DashboardAdminService(session, AuditEventRepository(session))


ServiceDep = Annotated[DashboardAdminService, Depends(get_dashboard_admin_service)]


@router.get("/dashboard", response_model=DashboardStatsOut)
async def get_dashboard_stats(user: CurrentAdminUser, service: ServiceDep) -> DashboardStatsOut:
    return await service.get_stats()
