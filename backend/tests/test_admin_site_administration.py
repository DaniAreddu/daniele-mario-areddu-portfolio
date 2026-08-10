from __future__ import annotations

import uuid

import pytest
from sqlalchemy import delete, select

from app.core.security import hash_password
from app.models.admin_user import AdminUser
from app.models.audit_event import AuditEvent
from app.models.navigation_item import NavigationItem
from app.models.redirect import Redirect
from app.models.site_settings import HomepageFeature
from app.models.social_link import SocialLink

SPA_HEADERS = {"X-Requested-With": "admin-spa"}
PASSWORD = "correct-horse-battery-staple"
_MARKER = "zzz-site-admin-test-marker-zzz"


@pytest.fixture(autouse=True)
async def _cleanup(db_session):
    yield
    for model, entity_type, field in (
        (NavigationItem, "navigation_item", NavigationItem.label_en),
        (SocialLink, "social_link", SocialLink.label),
        (Redirect, "redirect", Redirect.source_path),
    ):
        result = await db_session.execute(select(model.id).where(field.like(f"%{_MARKER}%")))
        ids = [row[0] for row in result]
        if ids:
            await db_session.execute(
                delete(AuditEvent).where(
                    AuditEvent.entity_type == entity_type, AuditEvent.entity_id.in_(ids)
                )
            )
            await db_session.execute(delete(model).where(model.id.in_(ids)))
            await db_session.commit()

    await db_session.execute(delete(HomepageFeature))
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


# -- Site settings / SEO settings (singletons) -----------------------------


async def test_site_settings_singleton_get_and_update(client, db_session):
    await _login(client, db_session)
    current = await client.get("/api/v1/admin/site-settings")
    assert current.status_code == 200

    update = await client.put(
        "/api/v1/admin/site-settings",
        json={**current.json(), "show_projects": False},
        headers=SPA_HEADERS,
    )
    assert update.status_code == 200
    assert update.json()["show_projects"] is False

    public = await client.get("/api/v1/site-settings")
    assert public.status_code == 200
    assert public.json()["show_projects"] is False
    assert "analytics_id" not in public.json()


async def test_seo_settings_singleton_get_and_update(client, db_session):
    await _login(client, db_session)
    current = await client.get("/api/v1/admin/seo-settings")
    assert current.status_code == 200

    update = await client.put(
        "/api/v1/admin/seo-settings",
        json={**current.json(), "site_title": f"Title {_MARKER}"},
        headers=SPA_HEADERS,
    )
    assert update.status_code == 200

    public = await client.get("/api/v1/seo-settings")
    assert public.status_code == 200
    assert public.json()["site_title"] == f"Title {_MARKER}"


# -- Navigation --------------------------------------------------------------


async def test_navigation_item_crud_and_public_visibility(client, db_session):
    await _login(client, db_session)
    payload = {
        "label_en": f"About {_MARKER}",
        "label_it": "Chi sono",
        "target": "/about",
        "placement": "header",
    }
    create = await client.post("/api/v1/admin/navigation", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    item_id = create.json()["id"]

    public = await client.get("/api/v1/navigation")
    assert any(item["label"] == payload["label_en"] for item in public.json()["header"])

    public_it = await client.get("/api/v1/navigation?lang=it")
    assert any(item["label"] == "Chi sono" for item in public_it.json()["header"])

    disable = await client.patch(
        f"/api/v1/admin/navigation/{item_id}",
        json={**payload, "enabled": False},
        headers=SPA_HEADERS,
    )
    assert disable.status_code == 200
    public_after_disable = await client.get("/api/v1/navigation")
    header_labels = [item["label"] for item in public_after_disable.json()["header"]]
    assert payload["label_en"] not in header_labels

    delete_response = await client.delete(
        f"/api/v1/admin/navigation/{item_id}", headers=SPA_HEADERS
    )
    assert delete_response.status_code == 204


async def test_navigation_item_rejects_bad_target(client, db_session):
    await _login(client, db_session)
    payload = {
        "label_en": f"Bad {_MARKER}",
        "target": "not-a-path",
        "placement": "header",
        "is_external": False,
    }
    response = await client.post("/api/v1/admin/navigation", json=payload, headers=SPA_HEADERS)
    assert response.status_code == 422


# -- Social links --------------------------------------------------------


async def test_social_link_crud_and_icon_allowlist(client, db_session):
    await _login(client, db_session)
    payload = {"label": f"GitHub {_MARKER}", "url": "https://github.com/example", "icon": "github"}
    create = await client.post("/api/v1/admin/social-links", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    link_id = create.json()["id"]

    public = await client.get("/api/v1/social-links")
    assert any(link["label"] == payload["label"] for link in public.json())

    bad_icon = await client.post(
        "/api/v1/admin/social-links",
        json={**payload, "label": f"Bad {_MARKER}", "icon": "not-a-real-icon"},
        headers=SPA_HEADERS,
    )
    assert bad_icon.status_code == 422

    await client.delete(f"/api/v1/admin/social-links/{link_id}", headers=SPA_HEADERS)


# -- Redirects -------------------------------------------------------------


async def test_redirect_crud_and_public_listing(client, db_session):
    await _login(client, db_session)
    source = f"/old-path-{_MARKER}"
    payload = {"source_path": source, "destination_path": "/about"}
    create = await client.post("/api/v1/admin/redirects", json=payload, headers=SPA_HEADERS)
    assert create.status_code == 201
    redirect_id = create.json()["id"]

    public = await client.get("/api/v1/redirects")
    assert any(r["source_path"] == source for r in public.json())

    await client.delete(f"/api/v1/admin/redirects/{redirect_id}", headers=SPA_HEADERS)


async def test_redirect_rejects_external_destination(client, db_session):
    await _login(client, db_session)
    payload = {"source_path": f"/x-{_MARKER}", "destination_path": "https://evil.example.com"}
    response = await client.post("/api/v1/admin/redirects", json=payload, headers=SPA_HEADERS)
    assert response.status_code == 422


async def test_redirect_rejects_self_reference(client, db_session):
    await _login(client, db_session)
    payload = {"source_path": f"/x-{_MARKER}", "destination_path": f"/x-{_MARKER}"}
    response = await client.post("/api/v1/admin/redirects", json=payload, headers=SPA_HEADERS)
    assert response.status_code == 422


async def test_redirect_rejects_two_hop_loop(client, db_session):
    await _login(client, db_session)
    a = f"/loop-a-{_MARKER}"
    b = f"/loop-b-{_MARKER}"
    first = await client.post(
        "/api/v1/admin/redirects",
        json={"source_path": a, "destination_path": b},
        headers=SPA_HEADERS,
    )
    assert first.status_code == 201

    second = await client.post(
        "/api/v1/admin/redirects",
        json={"source_path": b, "destination_path": a},
        headers=SPA_HEADERS,
    )
    assert second.status_code == 400
    assert second.json()["error"]["code"] == "redirect_loop"

    await client.delete(f"/api/v1/admin/redirects/{first.json()['id']}", headers=SPA_HEADERS)


async def test_redirect_rejects_duplicate_source_path(client, db_session):
    await _login(client, db_session)
    source = f"/dup-{_MARKER}"
    first = await client.post(
        "/api/v1/admin/redirects",
        json={"source_path": source, "destination_path": "/about"},
        headers=SPA_HEADERS,
    )
    assert first.status_code == 201

    second = await client.post(
        "/api/v1/admin/redirects",
        json={"source_path": source, "destination_path": "/contact"},
        headers=SPA_HEADERS,
    )
    assert second.status_code == 400
    assert second.json()["error"]["code"] == "source_path_conflict"

    await client.delete(f"/api/v1/admin/redirects/{first.json()['id']}", headers=SPA_HEADERS)


# -- Homepage settings + features --------------------------------------


async def test_homepage_settings_singleton_get_and_update(client, db_session):
    await _login(client, db_session)
    current = await client.get("/api/v1/admin/homepage/settings")
    assert current.status_code == 200

    update = await client.put(
        "/api/v1/admin/homepage/settings",
        json={**current.json(), "hero_headline_en": f"Headline {_MARKER}"},
        headers=SPA_HEADERS,
    )
    assert update.status_code == 200

    public = await client.get("/api/v1/homepage")
    assert public.status_code == 200
    assert public.json()["hero_headline"] == f"Headline {_MARKER}"


async def test_homepage_feature_resolves_published_project(client, db_session):
    await _login(client, db_session)
    slug = f"test-homepage-project-{uuid.uuid4().hex[:8]}"
    create_project = await client.post(
        "/api/v1/admin/projects",
        json={"slug": slug, "title_en": "Featured Project", "tag_labels": []},
        headers=SPA_HEADERS,
    )
    project_id = create_project.json()["id"]
    await client.post(f"/api/v1/admin/projects/{project_id}/publish", headers=SPA_HEADERS)

    feature = await client.post(
        "/api/v1/admin/homepage/features",
        json={"entity_type": "project", "entity_id": project_id},
        headers=SPA_HEADERS,
    )
    assert feature.status_code == 201
    feature_id = feature.json()["id"]

    public = await client.get("/api/v1/homepage")
    matching = [f for f in public.json()["features"] if f["url_path"] == f"/projects/{slug}"]
    assert len(matching) == 1

    await client.delete(f"/api/v1/admin/homepage/features/{feature_id}", headers=SPA_HEADERS)
    await client.post(f"/api/v1/admin/projects/{project_id}/trash", headers=SPA_HEADERS)
    await client.delete(f"/api/v1/admin/projects/{project_id}", headers=SPA_HEADERS)


async def test_homepage_feature_rejects_unknown_entity(client, db_session):
    await _login(client, db_session)
    response = await client.post(
        "/api/v1/admin/homepage/features",
        json={"entity_type": "project", "entity_id": 9_999_999},
        headers=SPA_HEADERS,
    )
    assert response.status_code == 400
    assert response.json()["error"]["code"] == "invalid_reference"


async def test_site_administration_rejects_unauthenticated(client):
    assert (await client.get("/api/v1/admin/navigation")).status_code == 401
    assert (await client.get("/api/v1/admin/social-links")).status_code == 401
    assert (await client.get("/api/v1/admin/redirects")).status_code == 401
    assert (await client.get("/api/v1/admin/site-settings")).status_code == 401
    assert (await client.get("/api/v1/admin/seo-settings")).status_code == 401
    assert (await client.get("/api/v1/admin/homepage/settings")).status_code == 401
