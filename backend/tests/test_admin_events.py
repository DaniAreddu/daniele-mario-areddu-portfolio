from __future__ import annotations

import uuid

import pytest
from sqlalchemy import delete, select

from app.core.security import hash_password
from app.models.admin_user import AdminUser
from app.models.audit_event import AuditEvent
from app.models.event import Event
from app.models.revision import Revision

SPA_HEADERS = {"X-Requested-With": "admin-spa"}
PASSWORD = "correct-horse-battery-staple"


@pytest.fixture(autouse=True)
async def _cleanup_test_events(db_session):
    """Every event this file creates uses the `test-event-*` slug prefix.

    The test database is shared (session-scoped) across every test module —
    unlike the admin-auth fixtures (random emails, harmless to leave behind),
    real Event rows change the totals other tests assert on
    (test_events_and_geojson.py, test_seed_idempotency.py), so they must not
    outlive the test that created them. Their Revision/AuditEvent rows must
    go too: SQLite reuses primary-key ids after a delete, so a leftover
    Revision pointing at a since-recycled `entity_id` would otherwise leak
    into an unrelated later test's revision history.
    """
    yield
    result = await db_session.execute(select(Event.id).where(Event.slug.like("test-event-%")))
    event_ids = [row[0] for row in result]
    if event_ids:
        await db_session.execute(
            delete(Revision).where(
                Revision.entity_type == "event", Revision.entity_id.in_(event_ids)
            )
        )
        await db_session.execute(
            delete(AuditEvent).where(
                AuditEvent.entity_type == "event", AuditEvent.entity_id.in_(event_ids)
            )
        )
        await db_session.execute(delete(Event).where(Event.id.in_(event_ids)))
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


def _minimal_event_payload(**overrides):
    slug = f"test-event-{uuid.uuid4().hex[:10]}"
    payload = {
        "slug": slug,
        "event_name": "Test Conference 2027",
        "year": 2027,
        "format": "conference",
        "language": "en",
        "tag_labels": [],
    }
    payload.update(overrides)
    return payload


# -- authorization ---------------------------------------------------------


async def test_admin_events_reject_unauthenticated_requests(client):
    response = await client.get("/api/v1/admin/events")
    assert response.status_code == 401
    assert response.json()["error"]["code"] == "unauthorized"


async def test_create_event_requires_spa_header(client, db_session):
    await _create_and_login_admin(client, db_session)
    response = await client.post("/api/v1/admin/events", json=_minimal_event_payload())
    assert response.status_code == 400


async def test_admin_events_list_defaults_to_event_date_descending(client, db_session):
    """Never id/created_at/insertion order — the admin list defaults to
    newest event date first, same contract as the public list."""
    await _create_and_login_admin(client, db_session)
    older = _minimal_event_payload(year=2025, month=3)
    newer = _minimal_event_payload(year=2027, month=1)
    # Create the older event LAST, so an id/created_at/insertion-order sort
    # would (wrongly) place it before the newer one.
    await client.post("/api/v1/admin/events", json=newer, headers=SPA_HEADERS)
    await client.post("/api/v1/admin/events", json=older, headers=SPA_HEADERS)

    response = await client.get("/api/v1/admin/events")
    slugs = [item["slug"] for item in response.json()]
    assert slugs.index(newer["slug"]) < slugs.index(older["slug"])


# -- create / draft / publish lifecycle -------------------------------------


async def test_new_draft_event_is_never_publicly_visible(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload()

    create = await client.post(
        "/api/v1/admin/events", json=payload, headers=SPA_HEADERS
    )
    assert create.status_code == 201
    body = create.json()
    assert body["publication_status"] == "DRAFT"
    event_id = body["id"]

    public_list = await client.get("/api/v1/events")
    assert all(event["slug"] != payload["slug"] for event in public_list.json())

    public_detail = await client.get(f"/api/v1/events/{payload['slug']}")
    assert public_detail.status_code == 404

    # But an authenticated admin can preview it in the exact public shape.
    preview = await client.get(f"/api/v1/admin/events/{event_id}/preview")
    assert preview.status_code == 200
    assert preview.json()["slug"] == payload["slug"]


async def test_publishing_a_draft_makes_it_publicly_visible(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload()
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    event_id = create.json()["id"]

    stats_before = (await client.get("/api/v1/events/stats")).json()["total_events"]

    publish = await client.post(
        f"/api/v1/admin/events/{event_id}/publish", headers=SPA_HEADERS
    )
    assert publish.status_code == 200
    assert publish.json()["publication_status"] == "PUBLISHED"
    assert publish.json()["published_at"] is not None

    public_detail = await client.get(f"/api/v1/events/{payload['slug']}")
    assert public_detail.status_code == 200

    stats_after = (await client.get("/api/v1/events/stats")).json()["total_events"]
    assert stats_after == stats_before + 1


async def test_scheduled_event_with_future_publish_at_is_not_yet_visible(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload()
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    event_id = create.json()["id"]

    schedule = await client.post(
        f"/api/v1/admin/events/{event_id}/schedule",
        json={"publish_at": "2099-01-01T00:00:00Z"},
        headers=SPA_HEADERS,
    )
    assert schedule.status_code == 200
    assert schedule.json()["publication_status"] == "SCHEDULED"

    public_detail = await client.get(f"/api/v1/events/{payload['slug']}")
    assert public_detail.status_code == 404


async def test_unpublish_and_archive_remove_from_public_view(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload()
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    event_id = create.json()["id"]
    await client.post(f"/api/v1/admin/events/{event_id}/publish", headers=SPA_HEADERS)
    assert (await client.get(f"/api/v1/events/{payload['slug']}")).status_code == 200

    unpublish = await client.post(
        f"/api/v1/admin/events/{event_id}/unpublish", headers=SPA_HEADERS
    )
    assert unpublish.json()["publication_status"] == "DRAFT"
    assert (await client.get(f"/api/v1/events/{payload['slug']}")).status_code == 404

    await client.post(f"/api/v1/admin/events/{event_id}/publish", headers=SPA_HEADERS)
    archive = await client.post(f"/api/v1/admin/events/{event_id}/archive", headers=SPA_HEADERS)
    assert archive.json()["publication_status"] == "ARCHIVED"
    assert (await client.get(f"/api/v1/events/{payload['slug']}")).status_code == 404


# -- trash / soft delete -----------------------------------------------------


async def test_trash_and_restore_roundtrip(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload()
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    event_id = create.json()["id"]
    await client.post(f"/api/v1/admin/events/{event_id}/publish", headers=SPA_HEADERS)

    trash = await client.post(f"/api/v1/admin/events/{event_id}/trash", headers=SPA_HEADERS)
    assert trash.status_code == 200
    assert trash.json()["deleted_at"] is not None
    assert (await client.get(f"/api/v1/events/{payload['slug']}")).status_code == 404

    default_list = await client.get("/api/v1/admin/events")
    assert all(item["id"] != event_id for item in default_list.json())
    trashed_list = await client.get("/api/v1/admin/events?trashed=true")
    assert any(item["id"] == event_id for item in trashed_list.json())

    restore = await client.post(f"/api/v1/admin/events/{event_id}/restore", headers=SPA_HEADERS)
    assert restore.json()["deleted_at"] is None
    assert (await client.get(f"/api/v1/events/{payload['slug']}")).status_code == 200


async def test_permanent_delete_requires_trash_first(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload()
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    event_id = create.json()["id"]

    refused = await client.delete(f"/api/v1/admin/events/{event_id}", headers=SPA_HEADERS)
    assert refused.status_code == 400
    assert refused.json()["error"]["code"] == "not_trashed"

    await client.post(f"/api/v1/admin/events/{event_id}/trash", headers=SPA_HEADERS)
    deleted = await client.delete(f"/api/v1/admin/events/{event_id}", headers=SPA_HEADERS)
    assert deleted.status_code == 204

    gone = await client.get(f"/api/v1/admin/events/{event_id}")
    assert gone.status_code == 404


# -- mass-assignment guard ---------------------------------------------------


async def test_update_payload_cannot_change_publication_status(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload()
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    event_id = create.json()["id"]
    assert create.json()["publication_status"] == "DRAFT"

    sneaky_update = {**payload, "publication_status": "PUBLISHED", "event_name": "Renamed"}
    update = await client.patch(
        f"/api/v1/admin/events/{event_id}", json=sneaky_update, headers=SPA_HEADERS
    )
    assert update.status_code == 200
    assert update.json()["event_name"] == "Renamed"
    # The lifecycle field was silently ignored by the schema, not applied —
    # publication only ever happens through the dedicated /publish endpoint.
    assert update.json()["publication_status"] == "DRAFT"


# -- tags ---------------------------------------------------------------


async def test_creating_an_event_with_tags_normalizes_and_reuses_them(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload(tag_labels=["AI", "  Backend  "])
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    assert create.json()["tags"] == ["AI", "Backend"]

    tags = await client.get("/api/v1/admin/tags")
    slugs = {tag["slug"] for tag in tags.json()}
    assert {"ai", "backend"}.issubset(slugs)

    # A second event reusing the same (differently-cased) label must not
    # create a duplicate Tag row.
    payload2 = _minimal_event_payload(tag_labels=["ai"])
    await client.post("/api/v1/admin/events", json=payload2, headers=SPA_HEADERS)
    tags_after = await client.get("/api/v1/admin/tags")
    ai_tags = [tag for tag in tags_after.json() if tag["slug"] == "ai"]
    assert len(ai_tags) == 1


# -- duplicate detection ------------------------------------------------


async def test_check_duplicates_flags_similar_existing_event(client, db_session):
    await _create_and_login_admin(client, db_session)
    # Uses real seeded data: an existing Madrid/2025 event should surface as
    # a candidate when creating something similarly named.
    response = await client.get(
        "/api/v1/admin/events/check-duplicates",
        params={"event_name": "Nerdearla Madrid", "year": 2025, "city": "Madrid"},
    )
    assert response.status_code == 200
    candidates = response.json()
    assert any("nerdearla" in c["event_name"].lower() for c in candidates)


# -- revisions ------------------------------------------------------------


async def test_update_creates_a_restorable_revision(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload(city="Rome")
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    event_id = create.json()["id"]

    updated_payload = {**payload, "city": "Milan"}
    update = await client.patch(
        f"/api/v1/admin/events/{event_id}", json=updated_payload, headers=SPA_HEADERS
    )
    assert update.json()["city"] == "Milan"

    revisions = await client.get(f"/api/v1/admin/events/{event_id}/revisions")
    assert revisions.status_code == 200
    revision_list = revisions.json()
    assert len(revision_list) == 1
    assert revision_list[0]["snapshot"]["city"] == "Rome"

    restore = await client.post(
        f"/api/v1/admin/events/{event_id}/revisions/{revision_list[0]['id']}/restore",
        headers=SPA_HEADERS,
    )
    assert restore.status_code == 200
    assert restore.json()["city"] == "Rome"

    # Restoring itself created a new revision (of the pre-restore state).
    revisions_after = await client.get(f"/api/v1/admin/events/{event_id}/revisions")
    assert len(revisions_after.json()) == 2


async def test_revision_restore_from_a_different_event_is_rejected(client, db_session):
    await _create_and_login_admin(client, db_session)
    first = await client.post(
        "/api/v1/admin/events", json=_minimal_event_payload(), headers=SPA_HEADERS
    )
    second = await client.post(
        "/api/v1/admin/events", json=_minimal_event_payload(), headers=SPA_HEADERS
    )
    first_id, second_id = first.json()["id"], second.json()["id"]

    await client.patch(
        f"/api/v1/admin/events/{first_id}",
        json={**_minimal_event_payload(), "city": "Turin"},
        headers=SPA_HEADERS,
    )
    revisions = (await client.get(f"/api/v1/admin/events/{first_id}/revisions")).json()

    cross_restore = await client.post(
        f"/api/v1/admin/events/{second_id}/revisions/{revisions[0]['id']}/restore",
        headers=SPA_HEADERS,
    )
    assert cross_restore.status_code == 404


# -- audit log --------------------------------------------------------------


async def test_lifecycle_actions_are_recorded_in_the_audit_log(client, db_session):
    await _create_and_login_admin(client, db_session)
    payload = _minimal_event_payload()
    create = await client.post("/api/v1/admin/events", json=payload, headers=SPA_HEADERS)
    event_id = create.json()["id"]
    await client.post(f"/api/v1/admin/events/{event_id}/publish", headers=SPA_HEADERS)

    result = await db_session.execute(
        select(AuditEvent).where(
            AuditEvent.entity_type == "event", AuditEvent.entity_id == event_id
        )
    )
    actions = {row.action for row in result.scalars().all()}
    assert "event.create" in actions
    assert "event.publish" in actions
