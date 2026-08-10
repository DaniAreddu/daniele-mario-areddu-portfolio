from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession
from app.repositories.redirect_repository import RedirectRepository
from app.schemas.redirect import RedirectOut
from app.services.redirect_service import RedirectService

router = APIRouter()


def get_redirect_service(session: DbSession) -> RedirectService:
    return RedirectService(RedirectRepository(session))


ServiceDep = Annotated[RedirectService, Depends(get_redirect_service)]


@router.get("/redirects", response_model=list[RedirectOut])
async def list_redirects(service: ServiceDep) -> list[RedirectOut]:
    return await service.list_all()
