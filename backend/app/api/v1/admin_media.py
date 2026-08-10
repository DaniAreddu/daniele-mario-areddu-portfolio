from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, File, Query, UploadFile

from app.api.deps import CurrentAdminUser, DbSession, SettingsDep, require_admin_spa_header
from app.repositories.media_repository import MediaRepository
from app.schemas.media_admin import MediaAssetOut, MediaAssetUpdate, MediaUsageOut
from app.services.media_admin_service import MediaAdminService
from app.services.storage import get_storage_backend

router = APIRouter(prefix="/admin/media")

RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def get_media_admin_service(session: DbSession, settings: SettingsDep) -> MediaAdminService:
    return MediaAdminService(MediaRepository(session), get_storage_backend(settings), settings)


ServiceDep = Annotated[MediaAdminService, Depends(get_media_admin_service)]


@router.get("", response_model=list[MediaAssetOut])
async def list_media(user: CurrentAdminUser, service: ServiceDep) -> list[MediaAssetOut]:
    return await service.list_all()


@router.get("/{media_id}", response_model=MediaAssetOut)
async def get_media(media_id: int, user: CurrentAdminUser, service: ServiceDep) -> MediaAssetOut:
    return await service.get(media_id)


@router.get("/{media_id}/usage", response_model=MediaUsageOut)
async def get_media_usage(
    media_id: int, user: CurrentAdminUser, service: ServiceDep
) -> MediaUsageOut:
    return await service.check_usage(media_id)


@router.post("", response_model=MediaAssetOut, status_code=201)
async def upload_media(
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
    file: Annotated[UploadFile, File()],
) -> MediaAssetOut:
    data = await file.read()
    return await service.upload(
        filename=file.filename or "upload",
        content_type=file.content_type or "application/octet-stream",
        data=data,
        actor=user,
    )


@router.patch("/{media_id}", response_model=MediaAssetOut)
async def update_media(
    media_id: int,
    payload: MediaAssetUpdate,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
) -> MediaAssetOut:
    return await service.update(media_id, payload, user)


@router.delete("/{media_id}", status_code=204, response_model=None)
async def delete_media(
    media_id: int,
    user: CurrentAdminUser,
    service: ServiceDep,
    _spa: RequireSpaHeader,
    force: Annotated[bool, Query()] = False,
) -> None:
    await service.delete(media_id, user, force=force)
