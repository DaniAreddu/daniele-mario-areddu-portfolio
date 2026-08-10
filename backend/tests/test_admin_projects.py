from __future__ import annotations

import uuid

import pytest
from sqlalchemy import delete, select

from app.core.security import hash_password
from app.models.admin_user import AdminUser
from app.models.audit_event import AuditEvent
from app.models.project import Project
from app.models.revision import Revision

SPA_HEADERS = {"X-Requested-With": "admin-spa"}
PASSWORD = "correct-horse-battery-staple"


@pytest.fixture(autouse=True)
async def _cleanup_test_projects(db_session):
    """Mirrors test_admin_events.py's cleanup fixture: this file's Project
    rows (slug prefix `test-project-`) must not outlive their test, or they
    pollute totals other tests assert on, and their Revision/AuditEvent rows
    must go too since SQLite recycles primary-key ids after a delete.
    """
    yield
    result = await db_session.execute(
        select(Project.id).where(Project.slug.like("test-project-%"))
    )
    project_ids = [row[0] for row in result]
    if project_ids:
        await db_session.execute(
            delete(Revision).where(
                Revision.entity_type == "project", Revision.entity_id.in_(project_ids)
            )
        )
        await db_session.execute(
            delete(AuditEvent).where(
                AuditEvent.entity_type == "project", AuditEvent.entity_id.in_(project_ids)
            )
        )
        await db_session.execute(delete(Project).where(Project.id.in_(project_ids)))
        await db_session.commit()


async def _create_and_login_admin(client, db_session) -> str:
    email = f"admin-{uuid.uuid4().hex[:12]}@example.com"
    db_session.add(AdminUser(email=email, password_hash=hash_password(PASSWORD)))
    await db_session.commit()
    response = await client.post(
        "/api/v1/admin/auth/login",
        json={"email": email, "password": PASSWORD},
        headers=SPA_HEADERS,
    )
    assert response.status_code == 200
    return email


def _minimal_project_payload(**overrides):
    slug = f"test-project-{uuid.uuid4().hex[:10]}"
    payload = {"slug": slug, "title_en": "Test Project", "tag_labels": []}
    payload.update(overrides)
    return payload


async def test_admin_projects_reject_unauthenticated_requests(client):
    response = await client.get("/api/v1/admin/projects")
    assert response.status_code == 401


async def test_new_draft_project_is_never_publicly_visible(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload()

    create = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    assert create.json()["publication_status"] == "DRAFT"
    project_id = create.json()["id"]

    public_list = await client.get("/api/v1/projects")
    assert all(project["slug"] != payload["slug"] for project in public_list.json())
    assert (await client.get(f"/api/v1/projects/{payload['slug']}")).status_code == 404

    preview = await client.get(f"/api/v1/admin/projects/{project_id}/preview")
    assert preview.status_code == 200
    assert preview.json()["slug"] == payload["slug"]


async def test_publishing_a_draft_makes_it_publicly_visible(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload(tag_labels=["Python", "FastAPI"])
    create = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    project_id = create.json()["id"]

    publish = await client.post(
        f"/api/v1/admin/projects/{project_id}/publish", headers=SPA_HEADERS
    )
    assert publish.status_code == 200
    assert publish.json()["publication_status"] == "PUBLISHED"

    public_detail = await client.get(f"/api/v1/projects/{payload['slug']}")
    assert public_detail.status_code == 200
    assert set(public_detail.json()["technologies"]) == {"Python", "FastAPI"}


async def test_cover_image_url_round_trips_to_public_api(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload(cover_image_url="https://example.com/cover.png")
    create = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    assert create.json()["cover_image_url"] == "https://example.com/cover.png"
    project_id = create.json()["id"]

    await client.post(f"/api/v1/admin/projects/{project_id}/publish", headers=SPA_HEADERS)

    public_list = await client.get("/api/v1/projects")
    published = next(p for p in public_list.json() if p["slug"] == payload["slug"])
    assert published["cover_image_url"] == "https://example.com/cover.png"

    public_detail = await client.get(f"/api/v1/projects/{payload['slug']}")
    assert public_detail.json()["cover_image_url"] == "https://example.com/cover.png"


async def test_cover_image_url_rejects_non_http_values(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload(cover_image_url="javascript:alert(1)")
    response = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    assert response.status_code == 422


async def test_trash_and_restore_roundtrip(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload()
    create = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    project_id = create.json()["id"]
    await client.post(f"/api/v1/admin/projects/{project_id}/publish", headers=SPA_HEADERS)

    trash = await client.post(f"/api/v1/admin/projects/{project_id}/trash", headers=SPA_HEADERS)
    assert trash.json()["deleted_at"] is not None
    assert (await client.get(f"/api/v1/projects/{payload['slug']}")).status_code == 404

    restore = await client.post(
        f"/api/v1/admin/projects/{project_id}/restore", headers=SPA_HEADERS
    )
    assert restore.json()["deleted_at"] is None
    assert (await client.get(f"/api/v1/projects/{payload['slug']}")).status_code == 200


async def test_permanent_delete_requires_trash_first(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload()
    create = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    project_id = create.json()["id"]

    refused = await client.delete(f"/api/v1/admin/projects/{project_id}", headers=SPA_HEADERS)
    assert refused.status_code == 400
    assert refused.json()["error"]["code"] == "not_trashed"

    await client.post(f"/api/v1/admin/projects/{project_id}/trash", headers=SPA_HEADERS)
    deleted = await client.delete(f"/api/v1/admin/projects/{project_id}", headers=SPA_HEADERS)
    assert deleted.status_code == 204


async def test_update_payload_cannot_change_publication_status(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload()
    create = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    project_id = create.json()["id"]

    sneaky_update = {**payload, "publication_status": "PUBLISHED", "title_en": "Renamed"}
    update = await client.patch(
        f"/api/v1/admin/projects/{project_id}", json=sneaky_update, headers=SPA_HEADERS
    )
    assert update.status_code == 200
    assert update.json()["title_en"] == "Renamed"
    assert update.json()["publication_status"] == "DRAFT"


async def test_tags_are_shared_with_events(client, db_session):
    """The whole point of one Tag vocabulary: a label used on a project and
    on an event must resolve to the exact same row, not two near-duplicates.
    """
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload(tag_labels=["Rust"])
    await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)

    tags = await client.get("/api/v1/admin/tags")
    rust_tags = [tag for tag in tags.json() if tag["slug"] == "rust"]
    assert len(rust_tags) == 1


async def test_update_creates_a_restorable_revision(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload(summary_en="Original summary")
    create = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    project_id = create.json()["id"]

    updated = {**payload, "summary_en": "Updated summary"}
    await client.patch(f"/api/v1/admin/projects/{project_id}", json=updated, headers=SPA_HEADERS)

    revisions = await client.get(f"/api/v1/admin/projects/{project_id}/revisions")
    assert len(revisions.json()) == 1
    assert revisions.json()[0]["snapshot"]["summary_en"] == "Original summary"

    restore = await client.post(
        f"/api/v1/admin/projects/{project_id}/revisions/{revisions.json()[0]['id']}/restore",
        headers=SPA_HEADERS,
    )
    assert restore.status_code == 200
    assert restore.json()["summary_en"] == "Original summary"


async def test_lifecycle_actions_are_recorded_in_the_audit_log(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_project_payload()
    create = await client.post("/api/v1/admin/projects", json=payload, headers=SPA_HEADERS)
    project_id = create.json()["id"]
    await client.post(f"/api/v1/admin/projects/{project_id}/publish", headers=SPA_HEADERS)

    result = await db_session.execute(
        select(AuditEvent).where(
            AuditEvent.entity_type == "project", AuditEvent.entity_id == project_id
        )
    )
    actions = {row.action for row in result.scalars().all()}
    assert "project.create" in actions
    assert "project.publish" in actions
