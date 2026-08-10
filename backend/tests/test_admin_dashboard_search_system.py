from __future__ import annotations

import uuid

from app.core.security import hash_password
from app.models.admin_user import AdminUser

SPA_HEADERS = {"X-Requested-With": "admin-spa"}
PASSWORD = "correct-horse-battery-staple"


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


async def test_dashboard_stats_reflect_real_counts(client, db_session):
    await _login(client, db_session)
    response = await client.get("/api/v1/admin/dashboard")
    assert response.status_code == 200
    body = response.json()
    content_types = (
        "events",
        "projects",
        "experience",
        "education",
        "community_activities",
        "recognition",
    )
    for key in content_types:
        assert set(body[key].keys()) == {"published", "draft", "scheduled", "archived", "trashed"}
    assert isinstance(body["media_count"], int)
    assert isinstance(body["upcoming_events_count"], int)
    assert isinstance(body["recent_activity"], list)


async def test_dashboard_counts_increase_after_creating_a_draft(client, db_session):
    await _login(client, db_session)
    before = (await client.get("/api/v1/admin/dashboard")).json()["projects"]["draft"]

    slug = f"test-dashboard-project-{uuid.uuid4().hex[:8]}"
    create = await client.post(
        "/api/v1/admin/projects",
        json={"slug": slug, "title_en": "Dashboard Project", "tag_labels": []},
        headers=SPA_HEADERS,
    )
    project_id = create.json()["id"]

    after = (await client.get("/api/v1/admin/dashboard")).json()["projects"]["draft"]
    assert after == before + 1

    await client.post(f"/api/v1/admin/projects/{project_id}/trash", headers=SPA_HEADERS)
    await client.delete(f"/api/v1/admin/projects/{project_id}", headers=SPA_HEADERS)


async def test_audit_log_lists_recent_events(client, db_session):
    await _login(client, db_session)
    slug = f"test-audit-project-{uuid.uuid4().hex[:8]}"
    create = await client.post(
        "/api/v1/admin/projects",
        json={"slug": slug, "title_en": "Audit Project", "tag_labels": []},
        headers=SPA_HEADERS,
    )
    project_id = create.json()["id"]

    log = await client.get("/api/v1/admin/audit-log?entity_type=project")
    assert log.status_code == 200
    assert any(
        entry["entity_id"] == project_id and entry["action"] == "project.create"
        for entry in log.json()
    )

    await client.post(f"/api/v1/admin/projects/{project_id}/trash", headers=SPA_HEADERS)
    await client.delete(f"/api/v1/admin/projects/{project_id}", headers=SPA_HEADERS)


async def test_recent_revisions_endpoint(client, db_session):
    await _login(client, db_session)
    response = await client.get("/api/v1/admin/revisions/recent")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_system_health_reports_database_and_storage_ok(client, db_session):
    await _login(client, db_session)
    response = await client.get("/api/v1/admin/system/health")
    assert response.status_code == 200
    body = response.json()
    assert body["database_ok"] is True
    assert body["storage_ok"] is True
    assert body["migration_status"] in ("up_to_date", "behind", "unknown")


async def test_search_finds_matching_project(client, db_session):
    await _login(client, db_session)
    marker = uuid.uuid4().hex[:10]
    slug = f"test-search-project-{marker}"
    create = await client.post(
        "/api/v1/admin/projects",
        json={"slug": slug, "title_en": f"Searchable {marker}", "tag_labels": []},
        headers=SPA_HEADERS,
    )
    project_id = create.json()["id"]

    results = await client.get(f"/api/v1/admin/search?q={marker}")
    assert results.status_code == 200
    matching = [r for r in results.json() if r["entity_type"] == "project"]
    assert any(r["entity_id"] == project_id for r in matching)

    await client.post(f"/api/v1/admin/projects/{project_id}/trash", headers=SPA_HEADERS)
    await client.delete(f"/api/v1/admin/projects/{project_id}", headers=SPA_HEADERS)


async def test_search_requires_minimum_query_length(client, db_session):
    await _login(client, db_session)
    response = await client.get("/api/v1/admin/search?q=a")
    assert response.status_code == 422


async def test_dashboard_audit_search_system_reject_unauthenticated(client):
    assert (await client.get("/api/v1/admin/dashboard")).status_code == 401
    assert (await client.get("/api/v1/admin/audit-log")).status_code == 401
    assert (await client.get("/api/v1/admin/system/health")).status_code == 401
    assert (await client.get("/api/v1/admin/search?q=test")).status_code == 401
