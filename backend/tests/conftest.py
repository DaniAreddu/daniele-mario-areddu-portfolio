"""Shared pytest fixtures.

Tests run against a dedicated, uniquely-named SQLite database file created
fresh for the session and removed afterward. This can never touch the
development or production PostgreSQL database, and the environment
variables below must be set before ``app.core.config`` is imported anywhere
(pydantic-settings reads them once, lazily, and the result is cached).
"""

from __future__ import annotations

import os
import tempfile
import uuid
from pathlib import Path

_TEST_DB_PATH = Path(tempfile.gettempdir()) / f"areddu_portfolio_test_{uuid.uuid4().hex}.db"
os.environ["DATABASE_URL"] = f"sqlite+aiosqlite:///{_TEST_DB_PATH.as_posix()}"
os.environ["CONTACT_RATE_LIMIT_PER_HOUR"] = "1000"
os.environ["SMTP_HOST"] = "127.0.0.1"
os.environ["SMTP_PORT"] = "1"  # nothing listens here: delivery fails fast and deterministically
os.environ["ENVIRONMENT"] = "test"

import pytest_asyncio  # noqa: E402
from httpx import ASGITransport, AsyncClient  # noqa: E402

from app.db.base import Base  # noqa: E402
from app.db.session import dispose_engine, get_engine, get_session_factory  # noqa: E402
from app.main import app  # noqa: E402
from app.seed.seed import seed_all  # noqa: E402


@pytest_asyncio.fixture(scope="session", autouse=True)
async def _prepared_database():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_all()
    yield
    await dispose_engine()
    if _TEST_DB_PATH.exists():
        _TEST_DB_PATH.unlink()


@pytest_asyncio.fixture()
async def db_session():
    factory = get_session_factory()
    async with factory() as session:
        yield session


@pytest_asyncio.fixture()
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
