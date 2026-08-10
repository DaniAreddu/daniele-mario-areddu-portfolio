from __future__ import annotations

from sqlalchemy import func, select

from app.db.session import get_session_factory
from app.models.event import Event
from app.models.profile import Profile
from app.seed.seed import seed_all


async def _counts() -> tuple[int, int]:
    factory = get_session_factory()
    async with factory() as session:
        events = (await session.execute(select(func.count()).select_from(Event))).scalar_one()
        profiles = (
            await session.execute(select(func.count()).select_from(Profile))
        ).scalar_one()
        return events, profiles


async def test_seed_all_is_idempotent():
    """The session-scoped fixture already ran seed_all() once; running it
    again must not create duplicate rows or fail on unique constraints."""
    events_before, profiles_before = await _counts()

    await seed_all()
    await seed_all()

    events_after, profiles_after = await _counts()

    assert events_after == events_before == 32
    assert profiles_after == profiles_before == 1
