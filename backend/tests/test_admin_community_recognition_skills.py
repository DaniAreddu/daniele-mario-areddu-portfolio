from __future__ import annotations

import uuid

import pytest
from sqlalchemy import delete, select

from app.core.security import hash_password
from app.models.admin_user import AdminUser
from app.models.audit_event import AuditEvent
from app.models.community import CommunityActivity
from app.models.recognition import Recognition
from app.models.revision import Revision
from app.models.skill import Skill, SkillCategory

SPA_HEADERS = {"X-Requested-With": "admin-spa"}
PASSWORD = "correct-horse-battery-staple"
_MARKER = "zzz-admin-test-marker-zzz"


@pytest.fixture(autouse=True)
async def _cleanup(db_session):
    yield
    for model, entity_type, field in (
        (CommunityActivity, "community_activity", CommunityActivity.slug),
        (Recognition, "recognition", Recognition.title_en),
    ):
        result = await db_session.execute(select(model.id).where(field.like(f"%{_MARKER}%")))
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

    result = await db_session.execute(
        select(SkillCategory.id).where(SkillCategory.slug.like(f"%{_MARKER}%"))
    )
    category_ids = [row[0] for row in result]
    if category_ids:
        await db_session.execute(delete(Skill).where(Skill.category_id.in_(category_ids)))
        await db_session.execute(delete(SkillCategory).where(SkillCategory.id.in_(category_ids)))
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


# -- Community -------------------------------------------------------------


async def test_community_profile_singleton_get_and_update(client, db_session):
    await _login(client, db_session)
    current = await client.get("/api/v1/admin/community/profile")
    assert current.status_code == 200
    payload = {**current.json(), "mission_en": f"Updated mission {_MARKER}"}
    for field in ("id", "created_at", "updated_at"):
        payload.pop(field, None)

    update = await client.put("/api/v1/admin/community/profile", json=payload, headers=SPA_HEADERS)
    assert update.status_code == 200
    assert update.json()["mission_en"] == f"Updated mission {_MARKER}"

    public = await client.get("/api/v1/community")
    assert public.json()["mission"] == f"Updated mission {_MARKER}"


async def test_community_activity_lifecycle(client, db_session):
    await _login(client, db_session)
    slug = f"test-activity-{_MARKER}-{uuid.uuid4().hex[:6]}"
    payload = {"slug": slug, "title_en": f"Activity {_MARKER}"}
    create = await client.post(
        "/api/v1/admin/community/activities", json=payload, headers=SPA_HEADERS
    )
    assert create.status_code == 201
    activity_id = create.json()["id"]

    public_before = await client.get("/api/v1/community")
    assert all(a["slug"] != slug for a in public_before.json()["activities"])

    preview = await client.get(f"/api/v1/admin/community/activities/{activity_id}/preview")
    assert preview.status_code == 200
    assert preview.json()["slug"] == slug

    await client.post(
        f"/api/v1/admin/community/activities/{activity_id}/publish", headers=SPA_HEADERS
    )
    public_after = await client.get("/api/v1/community")
    assert any(a["slug"] == slug for a in public_after.json()["activities"])

    await client.post(
        f"/api/v1/admin/community/activities/{activity_id}/trash", headers=SPA_HEADERS
    )
    public_trashed = await client.get("/api/v1/community")
    assert all(a["slug"] != slug for a in public_trashed.json()["activities"])


# -- Recognition -------------------------------------------------------


async def test_recognition_lifecycle_and_empty_section_stays_absent(client, db_session):
    await _login(client, db_session)
    payload = {"kind": "award", "title_en": f"Award {_MARKER}"}
    create = await client.post("/api/v1/admin/recognition", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    recognition_id = create.json()["id"]

    public_before = await client.get("/api/v1/recognition")
    assert all(_MARKER not in r["title"] for r in public_before.json())

    preview = await client.get(f"/api/v1/admin/recognition/{recognition_id}/preview")
    assert preview.status_code == 200
    assert preview.json()["title"] == payload["title_en"]

    await client.post(f"/api/v1/admin/recognition/{recognition_id}/publish", headers=SPA_HEADERS)
    public_after = await client.get("/api/v1/recognition")
    assert any(_MARKER in r["title"] for r in public_after.json())


async def test_recognition_rejects_unknown_kind(client, db_session):
    await _login(client, db_session)
    payload = {"kind": "not-a-real-kind", "title_en": "X"}
    response = await client.post("/api/v1/admin/recognition", json=payload, headers=SPA_HEADERS)
    assert response.status_code == 422


# -- Skills ---------------------------------------------------------------


async def test_skill_category_and_skill_crud(client, db_session):
    await _login(client, db_session)
    slug = f"test-cat-{_MARKER}-{uuid.uuid4().hex[:6]}"
    category_payload = {"slug": slug, "name_en": f"Category {_MARKER}"}
    create_category = await client.post(
        "/api/v1/admin/skills/categories", json=category_payload, headers=SPA_HEADERS
    )
    assert create_category.status_code == 201
    category_id = create_category.json()["id"]

    skill_payload = {"category_id": category_id, "name": "Rust"}
    create_skill = await client.post(
        "/api/v1/admin/skills", json=skill_payload, headers=SPA_HEADERS
    )
    assert create_skill.status_code == 201
    skill_id = create_skill.json()["id"]

    public_before = await client.get("/api/v1/skills")
    assert any(c["slug"] == slug for c in public_before.json())

    disable = await client.patch(
        f"/api/v1/admin/skills/{skill_id}",
        json={**skill_payload, "enabled": False},
        headers=SPA_HEADERS,
    )
    assert disable.status_code == 200
    public_after_disable = await client.get("/api/v1/skills")
    matching_category = next(c for c in public_after_disable.json() if c["slug"] == slug)
    assert all(s["name"] != "Rust" for s in matching_category["skills"])

    await client.delete(f"/api/v1/admin/skills/{skill_id}", headers=SPA_HEADERS)
    await client.delete(f"/api/v1/admin/skills/categories/{category_id}", headers=SPA_HEADERS)
    public_final = await client.get("/api/v1/skills")
    assert all(c["slug"] != slug for c in public_final.json())


async def test_admin_community_recognition_skills_reject_unauthenticated(client):
    assert (await client.get("/api/v1/admin/community/profile")).status_code == 401
    assert (await client.get("/api/v1/admin/recognition")).status_code == 401
    assert (await client.get("/api/v1/admin/skills/categories")).status_code == 401
