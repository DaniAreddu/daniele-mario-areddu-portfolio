from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.api.deps import CurrentAdminUser, DbSession
from app.schemas.search_admin import SearchResultOut
from app.services.search_admin_service import SearchAdminService

router = APIRouter(prefix="/admin")


def get_search_admin_service(session: DbSession) -> SearchAdminService:
    return SearchAdminService(session)


ServiceDep = Annotated[SearchAdminService, Depends(get_search_admin_service)]


@router.get("/search", response_model=list[SearchResultOut])
async def admin_search(
    user: CurrentAdminUser,
    service: ServiceDep,
    q: Annotated[str, Query(min_length=2, max_length=100)],
) -> list[SearchResultOut]:
    return await service.search(q)
