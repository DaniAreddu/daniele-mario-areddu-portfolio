from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.contact import ContactSubmission


class ContactRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, submission: ContactSubmission) -> ContactSubmission:
        self.session.add(submission)
        await self.session.commit()
        await self.session.refresh(submission)
        return submission

    async def count_recent_from_ip_hash(self, ip_hash: str, within: timedelta) -> int:
        since = datetime.now(UTC) - within
        result = await self.session.execute(
            select(func.count())
            .select_from(ContactSubmission)
            .where(
                ContactSubmission.source_ip_hash == ip_hash,
                ContactSubmission.created_at >= since,
            )
        )
        return int(result.scalar_one())
