from __future__ import annotations

import uuid

import pyotp
from httpx import ASGITransport, AsyncClient

from app.core.config import get_settings
from app.core.security import hash_password
from app.main import app
from app.models.admin_user import AdminUser

SPA_HEADERS = {"X-Requested-With": "admin-spa"}
PASSWORD = "correct-horse-battery-staple"


async def _create_admin_user(db_session, *, totp_enabled: bool = False) -> tuple[AdminUser, str]:
    email = f"admin-{uuid.uuid4().hex[:12]}@example.com"
    user = AdminUser(
        email=email, password_hash=hash_password(PASSWORD), totp_enabled=totp_enabled
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user, email


# -- basic login / session lifecycle -------------------------------------


async def test_login_without_totp_authenticates_immediately(client, db_session):
    _, email = await _create_admin_user(db_session)

    response = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    assert response.status_code == 200
    assert response.json() == {"status": "authenticated"}
    assert "admin_session" in response.cookies

    me = await client.get("/api/v1/admin/auth/me")
    assert me.status_code == 200
    assert me.json()["email"] == email
    assert me.json()["role"] == "OWNER"


async def test_login_rejects_wrong_password_with_generic_error(client, db_session):
    _, email = await _create_admin_user(db_session)

    response = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": "wrong-password"},
        headers=SPA_HEADERS,
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"


async def test_login_rejects_unknown_email_with_same_generic_error(client):
    response = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": "nobody@example.com", "password": "whatever"},
        headers=SPA_HEADERS,
    )
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "invalid_credentials"


async def test_login_requires_spa_header(client, db_session):
    _, email = await _create_admin_user(db_session)

    response = await client.post(
        "/api/v1/admin/auth/login", json={"email": email, "password": PASSWORD}
    )
    assert response.status_code == 400


async def test_me_without_session_is_unauthorized(client):
    response = await client.get("/api/v1/admin/auth/me")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_logout_revokes_the_session(client, db_session):
    _, email = await _create_admin_user(db_session)
    await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    assert (await client.get("/api/v1/admin/auth/me")).status_code == 200

    logout = await client.post("/api/v1/admin/auth/logout", headers=SPA_HEADERS)
    assert logout.status_code == 204

    assert (await client.get("/api/v1/admin/auth/me")).status_code == 401


async def test_login_rate_limiting_locks_out_after_repeated_failures(db_session):
    _, email = await _create_admin_user(db_session)
    limited_settings = get_settings().model_copy(update={"admin_login_rate_limit_per_hour": 2})
    app.dependency_overrides[get_settings] = lambda: limited_settings
    try:
        transport = ASGITransport(app=app, client=("203.0.113.9", 12345))
        async with AsyncClient(transport=transport, base_url="http://test") as isolated:
            for _ in range(2):
                resp = await isolated.post(
                    "/api/v1/admin/auth/login",
                    json={"email": email, "password": "wrong"},
                    headers=SPA_HEADERS,
                )
                assert resp.status_code == 401
            locked = await isolated.post(
                "/api/v1/admin/auth/login",
                json={"email": email, "password": PASSWORD},
                headers=SPA_HEADERS,
            )
            assert locked.status_code == 429
            assert locked.json()["error"]["code"] == "rate_limited"
    finally:
        app.dependency_overrides.pop(get_settings, None)


# -- two-factor enrollment and login --------------------------------------


async def test_totp_enrollment_and_login_flow(client, db_session):
    _, email = await _create_admin_user(db_session)
    await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )

    enroll = await client.post("/api/v1/admin/auth/totp/enroll", headers=SPA_HEADERS)
    assert enroll.status_code == 200
    secret = enroll.json()["secret"]
    assert enroll.json()["qr_data_uri"].startswith("data:image/png;base64,")

    valid_code = pyotp.TOTP(secret).now()
    confirm = await client.post(
        "/api/v1/admin/auth/totp/confirm", json={"code": valid_code}, headers=SPA_HEADERS
    )
    assert confirm.status_code == 200
    recovery_codes = confirm.json()["codes"]
    assert len(recovery_codes) == 10

    # Logging out and back in must now demand the second factor.
    await client.post("/api/v1/admin/auth/logout", headers=SPA_HEADERS)
    login = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    assert login.json() == {"status": "mfa_required"}

    # The pending (mfa_pending) session must not grant access on its own.
    assert (await client.get("/api/v1/admin/auth/me")).status_code == 401

    verify = await client.post(
        "/api/v1/admin/auth/totp/verify",
        json={"code": pyotp.TOTP(secret).now()},
        headers=SPA_HEADERS,
    )
    assert verify.status_code == 200
    assert verify.json() == {"status": "authenticated"}
    assert (await client.get("/api/v1/admin/auth/me")).status_code == 200


async def test_totp_recovery_code_is_single_use(client, db_session):
    _, email = await _create_admin_user(db_session)
    await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    enroll = await client.post("/api/v1/admin/auth/totp/enroll", headers=SPA_HEADERS)
    secret = enroll.json()["secret"]
    confirm = await client.post(
        "/api/v1/admin/auth/totp/confirm",
        json={"code": pyotp.TOTP(secret).now()},
        headers=SPA_HEADERS,
    )
    recovery_code = confirm.json()["codes"][0]

    await client.post("/api/v1/admin/auth/logout", headers=SPA_HEADERS)
    await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )

    first_use = await client.post(
        "/api/v1/admin/auth/totp/verify", json={"code": recovery_code}, headers=SPA_HEADERS
    )
    assert first_use.status_code == 200

    await client.post("/api/v1/admin/auth/logout", headers=SPA_HEADERS)
    await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    second_use = await client.post(
        "/api/v1/admin/auth/totp/verify", json={"code": recovery_code}, headers=SPA_HEADERS
    )
    assert second_use.status_code == 401
    assert second_use.json()["error"]["code"] == "invalid_totp_code"


async def test_disable_totp_requires_correct_password(client, db_session):
    _, email = await _create_admin_user(db_session)
    await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    enroll = await client.post("/api/v1/admin/auth/totp/enroll", headers=SPA_HEADERS)
    secret = enroll.json()["secret"]
    await client.post(
        "/api/v1/admin/auth/totp/confirm",
        json={"code": pyotp.TOTP(secret).now()},
        headers=SPA_HEADERS,
    )

    wrong = await client.post(
        "/api/v1/admin/auth/totp/disable", json={"password": "wrong"}, headers=SPA_HEADERS
    )
    assert wrong.status_code == 401

    correct = await client.post(
        "/api/v1/admin/auth/totp/disable", json={"password": PASSWORD}, headers=SPA_HEADERS
    )
    assert correct.status_code == 204

    await client.post("/api/v1/admin/auth/logout", headers=SPA_HEADERS)
    login = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    assert login.json() == {"status": "authenticated"}
