from __future__ import annotations

import io
import uuid

import pytest
from PIL import Image
from sqlalchemy import delete, select, update

from app.core.security import hash_password
from app.models.admin_user import AdminUser
from app.models.audit_event import AuditEvent
from app.models.media_asset import MediaAsset
from app.models.project import Project

SPA_HEADERS = {"X-Requested-With": "admin-spa"}
PASSWORD = "correct-horse-battery-staple"


@pytest.fixture(autouse=True)
async def _cleanup_test_media(db_session):
    yield
    result = await db_session.execute(select(MediaAsset.id))
    media_ids = [row[0] for row in result]
    if media_ids:
        await db_session.execute(
            delete(AuditEvent).where(
                AuditEvent.entity_type == "media_asset", AuditEvent.entity_id.in_(media_ids)
            )
        )
        await db_session.execute(delete(MediaAsset).where(MediaAsset.id.in_(media_ids)))
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


def _png_bytes(size: tuple[int, int] = (400, 300)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", size, color=(120, 20, 200)).save(buffer, format="PNG")
    return buffer.getvalue()


async def test_admin_media_rejects_unauthenticated_requests(client):
    response = await client.get("/api/v1/admin/media")
    assert response.status_code == 401


async def test_upload_valid_image_creates_asset_with_variants(client, db_session):
    await _create_and_login_admin(client, db_session)

    response = await client.post(
        "/api/v1/admin/media",
        headers=SPA_HEADERS,
        files={"file": ("photo.png", _png_bytes(), "image/png")},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["mime_type"] == "image/png"
    assert body["width"] == 400
    assert body["height"] == 300
    assert body["original_filename"] == "photo.png"
    assert "thumbnail" in body["variants"]
    assert body["url"].startswith("/api/v1/media/")

    # The stored file and its variants are fetchable from the public route.
    fetched = await client.get(body["url"])
    assert fetched.status_code == 200
    assert fetched.headers["content-type"] == "image/png"


async def test_upload_rejects_non_image_payload(client, db_session):
    await _create_and_login_admin(client, db_session)

    response = await client.post(
        "/api/v1/admin/media",
        headers=SPA_HEADERS,
        files={"file": ("notes.txt", b"this is not an image", "text/plain")},
    )
    assert response.status_code == 415
    assert response.json()["error"]["code"] == "unsupported_media_type"


async def test_upload_rejects_file_over_size_limit(client, db_session, monkeypatch):
    await _create_and_login_admin(client, db_session)
    from app.core.config import get_settings

    monkeypatch.setattr(get_settings(), "media_max_upload_bytes", 10)

    response = await client.post(
        "/api/v1/admin/media",
        headers=SPA_HEADERS,
        files={"file": ("photo.png", _png_bytes(), "image/png")},
    )
    assert response.status_code == 413
    assert response.json()["error"]["code"] == "media_too_large"


async def test_update_alt_text_and_caption(client, db_session):
    await _create_and_login_admin(client, db_session)
    upload = await client.post(
        "/api/v1/admin/media",
        headers=SPA_HEADERS,
        files={"file": ("photo.png", _png_bytes(), "image/png")},
    )
    media_id = upload.json()["id"]

    update = await client.patch(
        f"/api/v1/admin/media/{media_id}",
        json={"alt_text": "A colorful square", "caption": "Test caption"},
        headers=SPA_HEADERS,
    )
    assert update.status_code == 200
    assert update.json()["alt_text"] == "A colorful square"
    assert update.json()["caption"] == "Test caption"


async def test_delete_warns_when_media_is_referenced_and_force_overrides(client, db_session):
    await _create_and_login_admin(client, db_session)
    upload = await client.post(
        "/api/v1/admin/media",
        headers=SPA_HEADERS,
        files={"file": ("photo.png", _png_bytes(), "image/png")},
    )
    media_id = upload.json()["id"]
    media_url = upload.json()["url"]

    slug = f"test-media-project-{uuid.uuid4().hex[:8]}"
    create = await client.post(
        "/api/v1/admin/projects",
        json={"slug": slug, "title_en": "Media Project", "tag_labels": []},
        headers=SPA_HEADERS,
    )
    project_id = create.json()["id"]
    # `cover_image_url` is written directly (bypassing the admin
    # http(s)-only write validator) since a real upload's public URL is a
    # relative, same-origin path — the usage check operates on the raw
    # column value regardless of how it was set.
    await db_session.execute(
        update(Project).where(Project.id == project_id).values(cover_image_url=media_url)
    )
    await db_session.commit()

    usage = await client.get(f"/api/v1/admin/media/{media_id}/usage", headers=SPA_HEADERS)
    assert usage.json()["reference_count"] == 1

    blocked = await client.delete(f"/api/v1/admin/media/{media_id}", headers=SPA_HEADERS)
    assert blocked.status_code == 400
    assert blocked.json()["error"]["code"] == "media_in_use"

    forced = await client.delete(
        f"/api/v1/admin/media/{media_id}", headers=SPA_HEADERS, params={"force": "true"}
    )
    assert forced.status_code == 204

    await client.post(f"/api/v1/admin/projects/{project_id}/trash", headers=SPA_HEADERS)
    await client.delete(f"/api/v1/admin/projects/{project_id}", headers=SPA_HEADERS)


async def test_delete_unreferenced_media_succeeds(client, db_session):
    await _create_and_login_admin(client, db_session)
    upload = await client.post(
        "/api/v1/admin/media",
        headers=SPA_HEADERS,
        files={"file": ("photo.png", _png_bytes(), "image/png")},
    )
    media_id = upload.json()["id"]

    deleted = await client.delete(f"/api/v1/admin/media/{media_id}", headers=SPA_HEADERS)
    assert deleted.status_code == 204

    refetch = await client.get(f"/api/v1/admin/media/{media_id}", headers=SPA_HEADERS)
    assert refetch.status_code == 404


async def test_upload_and_delete_are_recorded_in_the_audit_log(client, db_session):
    await _create_and_login_admin(client, db_session)
    upload = await client.post(
        "/api/v1/admin/media",
        headers=SPA_HEADERS,
        files={"file": ("photo.png", _png_bytes(), "image/png")},
    )
    media_id = upload.json()["id"]
    await client.delete(f"/api/v1/admin/media/{media_id}", headers=SPA_HEADERS)

    result = await db_session.execute(
        select(AuditEvent).where(
            AuditEvent.entity_type == "media_asset", AuditEvent.entity_id == media_id
        )
    )
    actions = {row.action for row in result.scalars().all()}
    assert "media.upload" in actions
    assert "media.delete" in actions
