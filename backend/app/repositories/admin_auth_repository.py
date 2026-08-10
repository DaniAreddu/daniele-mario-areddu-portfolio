from __future__ import annotations

from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_recovery_code import AdminRecoveryCode
from app.models.admin_session import AdminLoginAttempt, AdminSession
from app.models.admin_user import AdminUser


class AdminAuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    # -- users -----------------------------------------------------------

    async def get_user_by_email(self, email: str) -> AdminUser | None:
        result = await self.session.execute(
            select(AdminUser).where(AdminUser.email == email.lower())
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: int) -> AdminUser | None:
        return await self.session.get(AdminUser, user_id)

    # -- sessions ----------------------------------------------------------

    async def create_session(self, admin_session: AdminSession) -> AdminSession:
        self.session.add(admin_session)
        await self.session.flush()
        return admin_session

    async def get_session_by_token_hash(self, token_hash: str) -> AdminSession | None:
        result = await self.session.execute(
            select(AdminSession).where(AdminSession.token_hash == token_hash)
        )
        return result.scalar_one_or_none()

    async def revoke_all_sessions_for_user(
        self, admin_user_id: int, *, except_id: int | None = None
    ) -> None:
        result = await self.session.execute(
            select(AdminSession).where(
                AdminSession.admin_user_id == admin_user_id,
                AdminSession.revoked_at.is_(None),
            )
        )
        for row in result.scalars():
            if except_id is not None and row.id == except_id:
                continue
            row.revoked_at = datetime.now(UTC)

    # -- login/TOTP attempt throttling ------------------------------------

    async def count_recent_password_attempts(
        self, email: str, ip_hash: str, within: timedelta
    ) -> int:
        cutoff = datetime.now(UTC) - within
        result = await self.session.execute(
            select(func.count())
            .select_from(AdminLoginAttempt)
            .where(
                AdminLoginAttempt.kind == "password",
                AdminLoginAttempt.email == email.lower(),
                AdminLoginAttempt.ip_hash == ip_hash,
                AdminLoginAttempt.succeeded.is_(False),
                AdminLoginAttempt.created_at >= cutoff,
            )
        )
        return int(result.scalar_one())

    async def record_password_attempt(self, email: str, ip_hash: str, succeeded: bool) -> None:
        self.session.add(
            AdminLoginAttempt(
                kind="password", email=email.lower(), ip_hash=ip_hash, succeeded=succeeded
            )
        )

    async def count_recent_totp_attempts(self, admin_user_id: int, within: timedelta) -> int:
        cutoff = datetime.now(UTC) - within
        result = await self.session.execute(
            select(func.count())
            .select_from(AdminLoginAttempt)
            .where(
                AdminLoginAttempt.kind == "totp",
                AdminLoginAttempt.admin_user_id == admin_user_id,
                AdminLoginAttempt.succeeded.is_(False),
                AdminLoginAttempt.created_at >= cutoff,
            )
        )
        return int(result.scalar_one())

    async def record_totp_attempt(self, admin_user_id: int, ip_hash: str, succeeded: bool) -> None:
        self.session.add(
            AdminLoginAttempt(
                kind="totp", admin_user_id=admin_user_id, ip_hash=ip_hash, succeeded=succeeded
            )
        )

    # -- recovery codes ------------------------------------------------

    async def get_recovery_codes(self, admin_user_id: int) -> list[AdminRecoveryCode]:
        result = await self.session.execute(
            select(AdminRecoveryCode).where(AdminRecoveryCode.admin_user_id == admin_user_id)
        )
        return list(result.scalars())

    async def add_recovery_codes(self, codes: list[AdminRecoveryCode]) -> None:
        self.session.add_all(codes)

    async def delete_recovery_codes(self, admin_user_id: int) -> None:
        result = await self.session.execute(
            select(AdminRecoveryCode).where(AdminRecoveryCode.admin_user_id == admin_user_id)
        )
        for row in result.scalars():
            await self.session.delete(row)
