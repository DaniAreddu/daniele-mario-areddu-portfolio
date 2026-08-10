"""Shared cryptographic helpers for admin authentication.

Two different hashing strategies are used deliberately:

- Passwords use Argon2id (slow, memory-hard) because they are relatively
  low-entropy secrets a database leak would otherwise let an attacker
  brute-force offline.
- Session tokens and recovery codes use SHA-256 because they are already
  high-entropy random values (256-bit / long random strings) — a fast hash
  is enough defense-in-depth against a DB-read exposing live credentials,
  and matches the existing ``ContactService`` IP-hashing precedent.

TOTP secrets are the one long-lived, *reversible* secret in the schema (a
password hash can't be reversed; a session token can just be revoked) — they
are encrypted at rest with Fernet rather than merely hashed.
"""

from __future__ import annotations

import base64
import hashlib
import secrets
from io import BytesIO

import qrcode
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from cryptography.fernet import Fernet, InvalidToken

_password_hasher = PasswordHasher()

# Verifying against this fixed, never-valid hash keeps login timing constant
# when the supplied email matches no admin user, so response latency can't
# reveal which emails are valid administrators.
_DUMMY_HASH = _password_hasher.hash("not-a-real-password-never-matches-anything")


def hash_password(password: str) -> str:
    return _password_hasher.hash(password)


def verify_password(password_hash: str, password: str) -> bool:
    try:
        _password_hasher.verify(password_hash, password)
    except VerifyMismatchError:
        return False
    return True


def verify_password_constant_time(password_hash: str | None, password: str) -> bool:
    """Verify a password, taking the same time whether or not a user exists.

    Pass ``None`` when no matching user was found so a real Argon2
    verification still runs (against the fixed dummy hash) instead of
    short-circuiting.
    """
    if password_hash is None:
        verify_password(_DUMMY_HASH, password)
        return False
    return verify_password(password_hash, password)


def sha256_hex(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def generate_token(n_bytes: int = 32) -> str:
    return secrets.token_urlsafe(n_bytes)


def normalize_recovery_code(code: str) -> str:
    """Strip formatting so a code can be hashed/compared consistently."""
    return code.strip().upper().replace("-", "").replace(" ", "")


def generate_recovery_code() -> str:
    raw = normalize_recovery_code(secrets.token_hex(6))
    return f"{raw[0:4]}-{raw[4:8]}-{raw[8:12]}"


def encrypt_secret(value: str, key: str) -> str:
    return Fernet(key.encode("utf-8")).encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_secret(token: str, key: str) -> str:
    try:
        return Fernet(key.encode("utf-8")).decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise ValueError("Could not decrypt secret: invalid key or corrupted value.") from exc


def qr_data_uri(data: str) -> str:
    buffer = BytesIO()
    qrcode.make(data).save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"
