from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession, require_admin_spa_header
from app.repositories.navigation_repository import NavigationRepository
from app.schemas.navigation_admin import NavigationItemAdminOut, NavigationItemAdminWrite
from app.services.navigation_admin_service import NavigationAdminService

router = APIRouter(prefix="/admin/navigation")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_navigation_admin_service(session: DbSession) -> NavigationAdminService:
    return NavigationAdminService(NavigationRepository(session))


ServiceDep = Annotated[NavigationAdminService, Depends(get_navigation_admin_service)]


@router.get("", response_model=list[NavigationItemAdminOut])
async def list_navigation_items(
    user: CurrentAdminUser, service: ServiceDep
) -> list[NavigationItemAdminOut]:
    return await service.list_all()


@router.post("", response_model=NavigationItemAdminOut, status_code=201)
async def create_navigation_item(
    payload: NavigationItemAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> NavigationItemAdminOut:
    return await service.create(payload, user)


@router.patch("/{item_id}", response_model=NavigationItemAdminOut)
async def update_navigation_item(
    item_id: int,
    payload: NavigationItemAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> NavigationItemAdminOut:
    return await service.update(item_id, payload, user)


@router.delete("/{item_id}", status_code=204, response_model=None)
async def delete_navigation_item(
    item_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.delete(item_id, user)
