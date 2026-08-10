from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, Locale
from app.repositories.navigation_repository import NavigationRepository
from app.schemas.navigation import NavigationOut
from app.services.navigation_service import NavigationService

router = APIRouter()


def get_navigation_service(session: DbSession) -> NavigationService:
    return NavigationService(NavigationRepository(session))


ServiceDep = Annotated[NavigationService, Depends(get_navigation_service)]


@router.get("/navigation", response_model=NavigationOut)
async def get_navigation(locale: Locale, service: ServiceDep) -> NavigationOut:
    return await service.get(locale)
