from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import DbSession, Locale
from app.repositories.event_repository import EventRepository
from app.repositories.homepage_repository import HomepageFeatureRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.homepage import HomepageOut
from app.services.homepage_service import HomepageService

router = APIRouter()


def get_homepage_service(session: DbSession) -> HomepageService:
    return HomepageService(
        session,
        HomepageFeatureRepository(session),
        ProjectRepository(session),
        EventRepository(session),
    )


ServiceDep = Annotated[HomepageService, Depends(get_homepage_service)]


@router.get("/homepage", response_model=HomepageOut)
async def get_homepage(locale: Locale, service: ServiceDep) -> HomepageOut:
    return await service.get(locale)
