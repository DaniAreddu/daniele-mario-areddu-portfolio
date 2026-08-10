"""Storage abstraction for uploaded media.

``LocalFilesystemStorage`` is the only implementation today, writing into a
Docker named volume (never PostgreSQL — large binary blobs don't belong in
the database). ``StorageBackend`` is the documented upgrade seam for a real
S3-compatible backend later: a new class implementing the same three
methods, selected via ``STORAGE_BACKEND``, with no changes needed anywhere
else — not a promise that one exists yet (no boto3/minio dependency has
been added, since nothing in this deployment uses it).
"""

from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Protocol

from app.core.config import Settings


class StorageBackend(Protocol):
    async def save(self, key: str, data: bytes) -> None: ...
    async def delete(self, key: str) -> None: ...
    def url_for(self, key: str) -> str: ...


class LocalFilesystemStorage:
    def __init__(self, base_path: str, public_base_url: str) -> None:
        self._base_path = Path(base_path)
        self._base_path.mkdir(parents=True, exist_ok=True)
        self._public_base_url = public_base_url.rstrip("/")

    async def save(self, key: str, data: bytes) -> None:
        target = self._base_path / key
        await asyncio.to_thread(target.write_bytes, data)

    async def delete(self, key: str) -> None:
        target = self._base_path / key
        await asyncio.to_thread(target.unlink, missing_ok=True)

    def url_for(self, key: str) -> str:
        return f"{self._public_base_url}/{key}"

    def read(self, key: str) -> bytes | None:
        target = self._base_path / key
        if not target.is_file():
            return None
        return target.read_bytes()


def get_storage_backend(settings: Settings) -> LocalFilesystemStorage:
    # A `match`/registry here is the seam for a future `STORAGE_BACKEND=s3`
    # branch — deliberately not built speculatively (see docs/admin-guide.md).
    return LocalFilesystemStorage(settings.media_storage_path, settings.media_public_base_url)
