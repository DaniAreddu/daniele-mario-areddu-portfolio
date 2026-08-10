from __future__ import annotations

from fastapi import APIRouter
from sqlalchemy import text

from app.core.errors import AppError
from app.db.session import get_engine

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe: process is up. Does not touch external dependencies."""
    return {"status": "ok"}


@router.get("/ready")
async def ready() -> dict[str, str]:
    """Readiness probe: verifies the database connection is actually usable."""
    try:
        engine = get_engine()
        async with engine.connect() as connection:
            await connection.execute(text("SELECT 1"))
    except Exception as exc:  # noqa: BLE001
        raise AppError("Database is not reachable.", code="not_ready") from exc
    return {"status": "ready"}
