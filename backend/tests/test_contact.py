from __future__ import annotations

from httpx import ASGITransport, AsyncClient

from app.core.config import get_settings
from app.main import app

VALID_PAYLOAD = {
    "name": "Jane Organizer",
    "email": "jane@example.com",
    "organization": "Example Conf",
    "request_type": "speaking_invitation",
    "event_or_project": "Example Conf 2027",
    "indicative_date": "Spring 2027",
    "message": "We would love to invite Daniele to speak about production AI agents.",
    "consent_given": True,
}


async def test_contact_submission_without_smtp_reports_delivery_failure(client):
    response = await client.post("/api/v1/contact", json=VALID_PAYLOAD)
    assert response.status_code == 201
    body = response.json()
    assert body["received"] is True
    # No SMTP relay is reachable in tests: never claim a false success.
    assert body["email_delivered"] is False


async def test_contact_requires_consent(client):
    payload = {**VALID_PAYLOAD, "consent_given": False}
    response = await client.post("/api/v1/contact", json=payload)
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"


async def test_contact_rejects_invalid_request_type(client):
    payload = {**VALID_PAYLOAD, "request_type": "not_a_real_type"}
    response = await client.post("/api/v1/contact", json=payload)
    assert response.status_code == 422


async def test_contact_rejects_short_message(client):
    payload = {**VALID_PAYLOAD, "message": "too short"}
    response = await client.post("/api/v1/contact", json=payload)
    assert response.status_code == 422


async def test_contact_honeypot_is_silently_accepted(client):
    payload = {**VALID_PAYLOAD, "website": "https://spam.example.com"}
    response = await client.post("/api/v1/contact", json=payload)
    # Bots must never be able to tell their submission was rejected.
    assert response.status_code == 201
    body = response.json()
    assert body["received"] is True
    assert body["email_delivered"] is False


async def test_contact_rate_limiting():
    # Uses its own client with a dedicated fake source IP so this test's
    # request count can never be polluted by other tests sharing the module
    # -level `client` fixture (and its default "unknown" client host).
    limited_settings = get_settings().model_copy(update={"contact_rate_limit_per_hour": 2})
    app.dependency_overrides[get_settings] = lambda: limited_settings
    transport = ASGITransport(app=app, client=("203.0.113.55", 12345))
    try:
        async with AsyncClient(transport=transport, base_url="http://test") as isolated_client:
            first = await isolated_client.post("/api/v1/contact", json=VALID_PAYLOAD)
            second = await isolated_client.post("/api/v1/contact", json=VALID_PAYLOAD)
            third = await isolated_client.post("/api/v1/contact", json=VALID_PAYLOAD)
        assert first.status_code == 201
        assert second.status_code == 201
        assert third.status_code == 429
        assert third.json()["error"]["code"] == "rate_limited"
    finally:
        app.dependency_overrides.pop(get_settings, None)
