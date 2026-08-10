"""System health checks for the admin "System" page — deliberately never
renders secret values (connection strings, keys), only booleans/status
labels, since this page's whole purpose is a quick operational glance.
"""

from __future__ import annotations

import uuid

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings
from app.core.logging import get_logger
from app.schemas.system_admin import SystemHealthOut
from app.services.storage import LocalFilesystemStorage

logger = get_logger(__name__)


async def _check_database(session: AsyncSession) -> bool:
    try:
        await session.execute(text("SELECT 1"))
        return True
    except Exception:  # noqa: BLE001 — a health check must never propagate
        logger.error("system_health_database_check_failed")
        return False


async def _check_migrations(session: AsyncSession) -> tuple[str, str | None, str | None]:
    try:
        result = await session.execute(text("SELECT version_num FROM alembic_version LIMIT 1"))
        current = result.scalar_one_or_none()
    except Exception:  # noqa: BLE001
        return "unknown", None, None

    try:
        from alembic.config import Config
        from alembic.script import ScriptDirectory

        config = Config("alembic.ini")
        script = ScriptDirectory.from_config(config)
        head = script.get_current_head()
    except Exception:  # noqa: BLE001 — best-effort; missing alembic.ini shouldn't 500
        return "unknown", current, None

    status = "up_to_date" if current == head else "behind"
    return status, current, head


async def _check_storage(storage: LocalFilesystemStorage) -> bool:
    probe_key = f"health-check-{uuid.uuid4().hex}.tmp"
    try:
        await storage.save(probe_key, b"ok")
        await storage.delete(probe_key)
        return True
    except OSError:
        logger.error("system_health_storage_check_failed")
        return False


class SystemAdminService:
    def __init__(
        self, session: AsyncSession, storage: LocalFilesystemStorage, settings: Settings
    ) -> None:
        self.session = session
        self.storage = storage
        self.settings = settings

    async def get_health(self) -> SystemHealthOut:
        database_ok = await _check_database(self.session)
        migration_status, current, head = await _check_migrations(self.session)
        storage_ok = await _check_storage(self.storage)

        return SystemHealthOut(
            database_ok=database_ok,
            migration_status=migration_status,
            current_migration=current,
            head_migration=head,
            storage_ok=storage_ok,
            storage_backend=self.settings.storage_backend,
        )
