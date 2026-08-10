from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession
from app.repositories.social_link_repository import SocialLinkRepository
from app.schemas.social_link import SocialLinkOut
from app.services.social_link_service import SocialLinkService

router = APIRouter()


def get_social_link_service(session: DbSession) -> SocialLinkService:
    return SocialLinkService(SocialLinkRepository(session))


ServiceDep = Annotated[SocialLinkService, Depends(get_social_link_service)]


@router.get("/social-links", response_model=list[SocialLinkOut])
async def list_social_links(service: ServiceDep) -> list[SocialLinkOut]:
    return await service.list_all()
