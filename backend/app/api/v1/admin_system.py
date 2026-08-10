from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession, SettingsDep
from app.schemas.system_admin import SystemHealthOut
from app.services.storage import get_storage_backend
from app.services.system_admin_service import SystemAdminService

router = APIRouter(prefix="/admin")


def get_system_admin_service(session: DbSession, settings: SettingsDep) -> SystemAdminService:
    return SystemAdminService(session, get_storage_backend(settings), settings)


ServiceDep = Annotated[SystemAdminService, Depends(get_system_admin_service)]


@router.get("/system/health", response_model=SystemHealthOut)
async def get_system_health(user: CurrentAdminUser, service: ServiceDep) -> SystemHealthOut:
    return await service.get_health()
