from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession, require_admin_spa_header
from app.repositories.social_link_repository import SocialLinkRepository
from app.schemas.social_link_admin import SocialLinkAdminOut, SocialLinkAdminWrite
from app.services.social_link_admin_service import SocialLinkAdminService

router = APIRouter(prefix="/admin/social-links")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_social_link_admin_service(session: DbSession) -> SocialLinkAdminService:
    return SocialLinkAdminService(SocialLinkRepository(session))


ServiceDep = Annotated[SocialLinkAdminService, Depends(get_social_link_admin_service)]


@router.get("", response_model=list[SocialLinkAdminOut])
async def list_social_links(
    user: CurrentAdminUser, service: ServiceDep
) -> list[SocialLinkAdminOut]:
    return await service.list_all()


@router.post("", response_model=SocialLinkAdminOut, status_code=201)
async def create_social_link(
    payload: SocialLinkAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> SocialLinkAdminOut:
    return await service.create(payload, user)


@router.patch("/{link_id}", response_model=SocialLinkAdminOut)
async def update_social_link(
    link_id: int,
    payload: SocialLinkAdminWrite,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> SocialLinkAdminOut:
    return await service.update(link_id, payload, user)


@router.delete("/{link_id}", status_code=204, response_model=None)
async def delete_social_link(
    link_id: int, user: CurrentAdminUser, service: ServiceDep, _spa: RequireSpaHeader
) -> None:
    await service.delete(link_id, user)
