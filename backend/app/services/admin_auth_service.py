"""Admin authentication: password + optional TOTP two-factor, server-side
sessions. See docs/admin-guide.md for the operator-facing walkthrough.

Login is a two-step state machine:

    password verified -> "mfa_pending" session (rejected by
    get_current_admin_user) -> TOTP or recovery code verified -> "active"
    session

An account without TOTP enabled skips straight to "active" after the
password step. No session is ever upgraded in place — verifying the second
factor revokes the pending session and issues a brand new one, so a leaked
or replayed pending-session cookie can never itself grant access.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pyotp

from app.core.config import Settings
from app.core.errors import AppError, RateLimitedError, UnauthorizedError
from app.core.logging import get_logger
from app.core.security import (
    decrypt_secret,
    encrypt_secret,
    generate_recovery_code,
    generate_token,
    normalize_recovery_code,
    qr_data_uri,
    sha256_hex,
    verify_password,
    verify_password_constant_time,
)
from app.models.admin_recovery_code import AdminRecoveryCode
from app.models.admin_session import AdminSession
from app.models.admin_user import AdminUser
from app.repositories.admin_auth_repository import AdminAuthRepository
from app.schemas.admin_auth import AdminTotpEnrollOut
from app.services._admin_common import record_audit_event

logger = get_logger(__name__)

_PASSWORD_ATTEMPT_WINDOW = timedelta(hours=1)
_TOTP_ATTEMPT_WINDOW = timedelta(minutes=10)
_TOTP_ISSUER = "Areddu Portfolio Admin"
_RECOVERY_CODE_COUNT = 10


class InvalidCredentialsError(AppError):
    status_code = 401
    code = "invalid_credentials"


class InvalidTotpCodeError(AppError):
    status_code = 401
    code = "invalid_totp_code"


class SessionResult:
    """The outcome of a login step: either a still-pending MFA challenge or
    a fully authenticated session. ``token`` is the raw cookie value — it is
    never persisted anywhere, only its hash is.
    """

    def __init__(self, token: str, status: str, user: AdminUser) -> None:
        self.token = token
        self.status = status
        self.user = user


class AdminAuthService:
    def __init__(self, repository: AdminAuthRepository, settings: Settings) -> None:
        self.repository = repository
        self.settings = settings

    # -- login / logout ----------------------------------------------------

    async def login(
        self, email: str, password: str, ip_hash: str, user_agent: str | None
    ) -> SessionResult:
        attempts = await self.repository.count_recent_password_attempts(
            email, ip_hash, _PASSWORD_ATTEMPT_WINDOW
        )
        if attempts >= self.settings.admin_login_rate_limit_per_hour:
            raise RateLimitedError("Too many login attempts. Please try again later.")

        user = await self.repository.get_user_by_email(email)
        candidate_hash = user.password_hash if user and user.is_active else None
        password_ok = verify_password_constant_time(candidate_hash, password)

        await self.repository.record_password_attempt(
            email, ip_hash, succeeded=bool(password_ok and user)
        )

        if not user or not user.is_active or not password_ok:
            await self.repository.commit()
            logger.warning("admin_login_failed", email=email)
            raise InvalidCredentialsError("Invalid email or password.")

        next_status = "mfa_pending" if user.totp_enabled else "active"
        session, raw_token = await self._issue_session(user, next_status, ip_hash, user_agent)
        if next_status == "active":
            action, actor_id, summary = "admin.login", user.id, f"{user.email} signed in"
        else:
            action = "admin.login_password_verified"
            actor_id = None
            summary = f"{user.email} entered correct password, awaiting 2FA"
        await record_audit_event(
            self.repository.session, actor_id=actor_id, action=action, summary=summary
        )
        await self.repository.commit()
        logger.info("admin_login_password_verified", email=email, mfa_required=user.totp_enabled)
        return SessionResult(token=raw_token, status=session.status, user=user)

    async def verify_totp(
        self, pending_token: str, code: str, ip_hash: str, user_agent: str | None
    ) -> SessionResult:
        pending = await self._get_valid_session(pending_token, expected_status="mfa_pending")
        if pending is None:
            raise UnauthorizedError("Your sign-in attempt has expired. Please log in again.")
        user = await self.repository.get_user_by_id(pending.admin_user_id)
        if user is None or not user.is_active or not user.totp_enabled:
            raise UnauthorizedError("Your sign-in attempt has expired. Please log in again.")

        attempts = await self.repository.count_recent_totp_attempts(user.id, _TOTP_ATTEMPT_WINDOW)
        if attempts >= self.settings.admin_totp_rate_limit_per_10_minutes:
            raise RateLimitedError("Too many verification attempts. Please try again later.")

        ok = self._verify_totp_code(user, code)
        if not ok:
            ok = await self._consume_recovery_code(user.id, code)

        await self.repository.record_totp_attempt(user.id, ip_hash, succeeded=ok)
        if not ok:
            await self.repository.commit()
            raise InvalidTotpCodeError("Invalid authentication code.")

        pending.revoked_at = datetime.now(UTC)
        _new_session, raw_token = await self._issue_session(user, "active", ip_hash, user_agent)
        await record_audit_event(
            self.repository.session,
            actor_id=user.id,
            action="admin.login",
            summary=f"{user.email} completed two-factor sign-in",
        )
        await self.repository.commit()
        return SessionResult(token=raw_token, status="active", user=user)

    async def logout(self, token: str) -> None:
        session = await self.repository.get_session_by_token_hash(sha256_hex(token))
        if session is not None and session.revoked_at is None:
            session.revoked_at = datetime.now(UTC)
            await record_audit_event(
                self.repository.session,
                actor_id=session.admin_user_id,
                action="admin.logout",
                summary="Signed out",
            )
            await self.repository.commit()

    async def get_current_user(self, token: str) -> AdminUser | None:
        session = await self._get_valid_session(token, expected_status="active")
        if session is None:
            return None
        session.last_seen_at = datetime.now(UTC)
        await self.repository.commit()
        return await self.repository.get_user_by_id(session.admin_user_id)

    # -- TOTP enrollment -----------------------------------------------

    async def begin_totp_enrollment(self, user: AdminUser) -> AdminTotpEnrollOut:
        if user.totp_enabled:
            raise AppError(
                "Two-factor authentication is already enabled.", code="totp_already_enabled"
            )

        secret = pyotp.random_base32()
        user.totp_secret_encrypted = encrypt_secret(secret, self.settings.admin_totp_encryption_key)
        await self.repository.commit()

        otpauth_uri = pyotp.TOTP(secret, issuer=_TOTP_ISSUER).provisioning_uri(
            name=user.email, issuer_name=_TOTP_ISSUER
        )
        return AdminTotpEnrollOut(
            secret=secret, otpauth_uri=otpauth_uri, qr_data_uri=qr_data_uri(otpauth_uri)
        )

    async def confirm_totp_enrollment(self, user: AdminUser, code: str) -> list[str]:
        if not user.totp_secret_encrypted:
            raise AppError("No pending two-factor enrollment.", code="totp_not_pending")

        secret = decrypt_secret(user.totp_secret_encrypted, self.settings.admin_totp_encryption_key)
        if not pyotp.TOTP(secret).verify(code.strip(), valid_window=1):
            raise InvalidTotpCodeError("Invalid authentication code.")

        user.totp_enabled = True
        raw_codes = await self._issue_recovery_codes(user)
        await record_audit_event(
            self.repository.session,
            actor_id=user.id,
            action="admin.totp_enabled",
            summary="Two-factor authentication enabled",
        )
        await self.repository.commit()
        return raw_codes

    async def disable_totp(self, user: AdminUser, password: str) -> None:
        if not verify_password(user.password_hash, password):
            raise InvalidCredentialsError("Invalid password.")

        user.totp_enabled = False
        user.totp_secret_encrypted = None
        await self.repository.delete_recovery_codes(user.id)
        await record_audit_event(
            self.repository.session,
            actor_id=user.id,
            action="admin.totp_disabled",
            summary="Two-factor authentication disabled",
        )
        await self.repository.commit()

    async def regenerate_recovery_codes(self, user: AdminUser, password: str) -> list[str]:
        if not user.totp_enabled:
            raise AppError("Two-factor authentication is not enabled.", code="totp_not_enabled")
        if not verify_password(user.password_hash, password):
            raise InvalidCredentialsError("Invalid password.")

        raw_codes = await self._issue_recovery_codes(user)
        await record_audit_event(
            self.repository.session,
            actor_id=user.id,
            action="admin.totp_recovery_regenerated",
            summary="Recovery codes regenerated",
        )
        await self.repository.commit()
        return raw_codes

    # -- internal helpers ------------------------------------------------

    async def _issue_session(
        self, user: AdminUser, status: str, ip_hash: str, user_agent: str | None
    ) -> tuple[AdminSession, str]:
        raw_token = generate_token()
        ttl = (
            timedelta(minutes=self.settings.admin_mfa_pending_ttl_minutes)
            if status == "mfa_pending"
            else timedelta(hours=self.settings.admin_session_ttl_hours)
        )
        session = AdminSession(
            admin_user_id=user.id,
            token_hash=sha256_hex(raw_token),
            status=status,
            expires_at=datetime.now(UTC) + ttl,
            ip_hash=ip_hash,
            user_agent=(user_agent or "")[:255],
        )
        await self.repository.create_session(session)
        return session, raw_token

    async def _get_valid_session(self, token: str, expected_status: str) -> AdminSession | None:
        session = await self.repository.get_session_by_token_hash(sha256_hex(token))
        if session is None:
            return None
        if session.revoked_at is not None:
            return None
        if session.status != expected_status:
            return None
        expires_at = session.expires_at
        if expires_at.tzinfo is None:
            # SQLite (used in tests) does not round-trip timezone-aware
            # datetimes; every value this service writes is UTC, so a naive
            # value read back is always safe to treat as UTC. PostgreSQL
            # (dev/prod) preserves tzinfo and this is a no-op there.
            expires_at = expires_at.replace(tzinfo=UTC)
        if expires_at <= datetime.now(UTC):
            return None
        return session

    def _verify_totp_code(self, user: AdminUser, code: str) -> bool:
        normalized = code.strip().replace(" ", "")
        if not user.totp_secret_encrypted or not normalized.isdigit() or len(normalized) != 6:
            return False
        secret = decrypt_secret(user.totp_secret_encrypted, self.settings.admin_totp_encryption_key)
        return bool(pyotp.TOTP(secret).verify(normalized, valid_window=1))

    async def _consume_recovery_code(self, admin_user_id: int, code: str) -> bool:
        candidate_hash = sha256_hex(normalize_recovery_code(code))
        codes = await self.repository.get_recovery_codes(admin_user_id)
        for recovery_code in codes:
            if recovery_code.used_at is None and recovery_code.code_hash == candidate_hash:
                recovery_code.used_at = datetime.now(UTC)
                return True
        return False

    async def _issue_recovery_codes(self, user: AdminUser) -> list[str]:
        await self.repository.delete_recovery_codes(user.id)
        raw_codes = [generate_recovery_code() for _ in range(_RECOVERY_CODE_COUNT)]
        rows = [
            AdminRecoveryCode(
                admin_user_id=user.id, code_hash=sha256_hex(normalize_recovery_code(code))
            )
            for code in raw_codes
        ]
        await self.repository.add_recovery_codes(rows)
        return raw_codes
