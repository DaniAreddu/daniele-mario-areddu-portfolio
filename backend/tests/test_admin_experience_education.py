from __future__ import annotations

import uuid

import pytest
from sqlalchemy import delete, select

from app.core.security import hash_password
from app.models.admin_user import AdminUser
from app.models.audit_event import AuditEvent
from app.models.education import Education
from app.models.experience import Experience
from app.models.revision import Revision

SPA_HEADERS = {"X-Requested-With": "admin-spa"}
PASSWORD = "correct-horse-battery-staple"
_MARKER = "zzz-admin-test-marker-zzz"


@pytest.fixture(autouse=True)
async def _cleanup(db_session):
    yield
    for model, entity_type in ((Experience, "experience"), (Education, "education")):
        result = await db_session.execute(
            select(model.id).where(
                model.organization.like(f"%{_MARKER}%")
                if model is Experience
                else model.institution.like(f"%{_MARKER}%")
            )
        )
        ids = [row[0] for row in result]
        if ids:
            await db_session.execute(
                delete(Revision).where(
                    Revision.entity_type == entity_type, Revision.entity_id.in_(ids)
                )
            )
            await db_session.execute(
                delete(AuditEvent).where(
                    AuditEvent.entity_type == entity_type, AuditEvent.entity_id.in_(ids)
                )
            )
            await db_session.execute(delete(model).where(model.id.in_(ids)))
            await db_session.commit()


async def _login(client, db_session) -> None:
    email = f"admin-{uuid.uuid4().hex[:12]}@example.com"
    db_session.add(AdminUser(email=email, password_hash=hash_password(PASSWORD)))
    await db_session.commit()
    response = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    assert response.status_code == 200


# -- Experience --------------------------------------------------------


async def test_experience_full_lifecycle_and_public_visibility(client, db_session):
    await _login(client, db_session)
    payload = {
        "organization": f"Test Org {_MARKER}",
        "role_en": "Backend Engineer",
        "start_date": "2020-01-01",
        "tag_labels": ["Python", "FastAPI"],
    }
    create = await client.post("/api/v1/admin/experience", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    assert create.json()["publication_status"] == "DRAFT"
    experience_id = create.json()["id"]

    public_before = await client.get("/api/v1/experiences")
    assert all(_MARKER not in item["organization"] for item in public_before.json())

    preview = await client.get(f"/api/v1/admin/experience/{experience_id}/preview")
    assert preview.status_code == 200
    assert preview.json()["organization"] == payload["organization"]

    publish = await client.post(
        f"/api/v1/admin/experience/{experience_id}/publish", headers=SPA_HEADERS
    )
    assert publish.status_code == 200
    assert publish.json()["publication_status"] == "PUBLISHED"

    public_after = await client.get("/api/v1/experiences")
    matching = [item for item in public_after.json() if _MARKER in item["organization"]]
    assert len(matching) == 1
    assert set(matching[0]["technologies"]) == {"Python", "FastAPI"}

    trash = await client.post(
        f"/api/v1/admin/experience/{experience_id}/trash", headers=SPA_HEADERS
    )
    assert trash.json()["deleted_at"] is not None
    public_after_trash = await client.get("/api/v1/experiences")
    assert all(_MARKER not in item["organization"] for item in public_after_trash.json())

    restore = await client.post(
        f"/api/v1/admin/experience/{experience_id}/restore", headers=SPA_HEADERS
    )
    assert restore.json()["deleted_at"] is None


async def test_experience_update_creates_revision(client, db_session):
    await _login(client, db_session)
    payload = {
        "organization": f"Rev Org {_MARKER}",
        "role_en": "Engineer",
        "start_date": "2021-01-01",
        "summary_en": "Original",
        "tag_labels": [],
    }
    create = await client.post("/api/v1/admin/experience", json=payload, headers=SPA_HEADERS)
    experience_id = create.json()["id"]

    updated = {**payload, "summary_en": "Updated"}
    await client.patch(
        f"/api/v1/admin/experience/{experience_id}", json=updated, headers=SPA_HEADERS
    )

    revisions = await client.get(f"/api/v1/admin/experience/{experience_id}/revisions")
    assert len(revisions.json()) == 1
    assert revisions.json()[0]["snapshot"]["summary_en"] == "Original"

    restore = await client.post(
        f"/api/v1/admin/experience/{experience_id}/revisions/{revisions.json()[0]['id']}/restore",
        headers=SPA_HEADERS,
    )
    assert restore.json()["summary_en"] == "Original"


# -- Education -----------------------------------------------------------


async def test_education_full_lifecycle_and_public_visibility(client, db_session):
    await _login(client, db_session)
    payload = {
        "institution": f"Test University {_MARKER}",
        "degree_en": "BSc Computer Science",
        "start_year": 2018,
    }
    create = await client.post("/api/v1/admin/education", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    education_id = create.json()["id"]

    public_before = await client.get("/api/v1/education")
    assert all(_MARKER not in item["institution"] for item in public_before.json())

    preview = await client.get(f"/api/v1/admin/education/{education_id}/preview")
    assert preview.status_code == 200
    assert preview.json()["institution"] == payload["institution"]

    await client.post(f"/api/v1/admin/education/{education_id}/publish", headers=SPA_HEADERS)
    public_after = await client.get("/api/v1/education")
    assert any(_MARKER in item["institution"] for item in public_after.json())

    await client.post(f"/api/v1/admin/education/{education_id}/trash", headers=SPA_HEADERS)
    public_after_trash = await client.get("/api/v1/education")
    assert all(_MARKER not in item["institution"] for item in public_after_trash.json())


async def test_admin_experience_and_education_reject_unauthenticated(client):
    assert (await client.get("/api/v1/admin/experience")).status_code == 401
    assert (await client.get("/api/v1/admin/education")).status_code == 401
