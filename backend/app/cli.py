"""Administrative command-line utilities.

Run via ``python -m app.cli <command>`` inside the backend container/venv —
this is the only supported way to create or recover an administrator
account. The application never creates a default admin/admin account on
startup, and there is no public sign-up endpoint.
"""

from __future__ import annotations

import argparse
import asyncio
import getpass
import re
import sys

from app.core.security import hash_password
from app.db.session import dispose_engine, get_session_factory
from app.models.admin_user import AdminUser
from app.repositories.admin_auth_repository import AdminAuthRepository

_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_MIN_PASSWORD_LENGTH = 12


def _prompt_credentials() -> tuple[str, str]:
    email = input("Email: ").strip()
    if not _EMAIL_RE.match(email):
        print("That doesn't look like a valid email address.", file=sys.stderr)
        raise SystemExit(1)

    password = getpass.getpass("Password: ")
    if len(password) < _MIN_PASSWORD_LENGTH:
        print(f"Password must be at least {_MIN_PASSWORD_LENGTH} characters.", file=sys.stderr)
        raise SystemExit(1)

    if getpass.getpass("Confirm password: ") != password:
        print("Passwords do not match.", file=sys.stderr)
        raise SystemExit(1)

    return email, password


async def _create_admin(email: str, password: str) -> None:
    factory = get_session_factory()
    async with factory() as session:
        repository = AdminAuthRepository(session)
        if await repository.get_user_by_email(email) is not None:
            print(f"An admin user with email {email!r} already exists.", file=sys.stderr)
            raise SystemExit(1)

        user = AdminUser(email=email.lower(), password_hash=hash_password(password), role="OWNER")
        session.add(user)
        await session.commit()
        print(f"Created admin user {email!r} (role=OWNER).")
        print("Sign in at /admin — you can enable two-factor authentication afterward.")
    await dispose_engine()


async def _reset_password(email: str, password: str, *, disable_totp: bool) -> None:
    factory = get_session_factory()
    async with factory() as session:
        repository = AdminAuthRepository(session)
        user = await repository.get_user_by_email(email)
        if user is None:
            print(f"No admin user found with email {email!r}.", file=sys.stderr)
            raise SystemExit(1)

        user.password_hash = hash_password(password)
        await repository.revoke_all_sessions_for_user(user.id)
        if disable_totp:
            user.totp_enabled = False
            user.totp_secret_encrypted = None
            await repository.delete_recovery_codes(user.id)
        await session.commit()

        print(f"Password reset for {email!r}. All active sessions have been revoked.")
        if disable_totp:
            print("Two-factor authentication has been disabled for this account.")
    await dispose_engine()


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="python -m app.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("create-admin", help="Create the first/an additional administrator.")

    reset_parser = subparsers.add_parser(
        "reset-password",
        help="Reset an existing administrator's password and revoke all sessions.",
    )
    reset_parser.add_argument(
        "--disable-totp",
        action="store_true",
        help="Also disable two-factor authentication (use if the authenticator device is lost).",
    )

    args = parser.parse_args(argv)

    if args.command == "create-admin":
        email, password = _prompt_credentials()
        asyncio.run(_create_admin(email, password))
    elif args.command == "reset-password":
        email, password = _prompt_credentials()
        asyncio.run(_reset_password(email, password, disable_totp=args.disable_totp))


if __name__ == "__main__":
    main()
