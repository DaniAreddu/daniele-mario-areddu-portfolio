from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import Locale, get_project_service
from app.schemas.project import ProjectDetailOut, ProjectListItemOut
from app.services.project_service import ProjectService

router = APIRouter()


@router.get("/projects", response_model=list[ProjectListItemOut])
async def list_projects(
    locale: Locale, service: Annotated[ProjectService, Depends(get_project_service)]
) -> list[ProjectListItemOut]:
    return await service.list_all(locale)


@router.get("/projects/{slug}", response_model=ProjectDetailOut)
async def get_project(
    slug: str, locale: Locale, service: Annotated[ProjectService, Depends(get_project_service)]
) -> ProjectDetailOut:
    return await service.get_by_slug(slug, locale)
