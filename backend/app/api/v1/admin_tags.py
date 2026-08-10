from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import CurrentAdminUser, DbSession
from app.repositories.tag_repository import TagRepository
from app.schemas.tag import TagOut

router = APIRouter(prefix="/admin/tags")


def get_tag_repository(session: DbSession) -> TagRepository:
    return TagRepository(session)


@router.get("", response_model=list[TagOut])
async def list_tags(
    user: CurrentAdminUser,
    repository: Annotated[TagRepository, Depends(get_tag_repository)],
) -> list[TagOut]:
    tags = await repository.list_all()
    return [TagOut(slug=tag.slug, label=tag.label) for tag in tags]
