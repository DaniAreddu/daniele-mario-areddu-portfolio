"""Public, unauthenticated media file serving.

`storage_key` values are server-generated (uuid4 hex, optionally suffixed
with a fixed variant name), never derived from client input — the strict
path parameter pattern below is a defense-in-depth belt on top of that,
not the primary access control. Unguessable keys are the access control
here, an accepted and documented tradeoff for a personal portfolio's
threat model (see docs/admin-guide.md).
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Path
from fastapi.responses import Response

from app.api.deps import SettingsDep
from app.core.errors import NotFoundError
from app.services.storage import get_storage_backend

router = APIRouter(prefix="/media")

_CONTENT_TYPES = {
    "jpg": "image/jpeg",
    "png": "image/png",
    "webp": "image/webp",
    "gif": "image/gif",
}

_KEY_PATTERN = r"^[a-f0-9]{32}(-[a-z]+)?\.(jpg|png|webp|gif)$"
KeyPath = Annotated[str, Path(pattern=_KEY_PATTERN)]


@router.get("/{key}")
async def get_media_file(key: KeyPath, settings: SettingsDep) -> Response:
    storage = get_storage_backend(settings)
    data = storage.read(key)
    if data is None:
        raise NotFoundError("Media file not found.")
    extension = key.rsplit(".", 1)[-1]
    return Response(
        content=data,
        media_type=_CONTENT_TYPES[extension],
        headers={"Cache-Control": "public, max-age=31536000, immutable"},
    )
