from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession, require_admin_spa_header
from app.repositories.redirect_repository import RedirectRepository
from app.schemas.redirect_admin import RedirectAdminOut, RedirectAdminWrite
from app.services.redirect_admin_service import RedirectAdminService

router = APIRouter(prefix="/admin/redirects")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_redirect_admin_service(session: DbSession) -> RedirectAdminService:
    return RedirectAdminService(RedirectRepository(session))


ServiceDep = Annotated[RedirectAdminService, Depends(get_redirect_admin_service)]


@router.get("", response_model=list[RedirectAdminOut])
async def list_redirects(user: CurrentAdminUser, service: ServiceDep) -> list[RedirectAdminOut]:
    return await service.list_all()


@router.post("", response_model=RedirectAdminOut, status_code=201)
async def create_redirect(
    payload: RedirectAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> RedirectAdminOut:
    return await service.create(payload, user)


@router.patch("/{redirect_id}", response_model=RedirectAdminOut)
async def update_redirect(
    redirect_id: int,
    payload: RedirectAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> RedirectAdminOut:
    return await service.update(redirect_id, payload, user)


@router.delete("/{redirect_id}", status_code=204, response_model=None)
async def delete_redirect(
    redirect_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.delete(redirect_id, user)
