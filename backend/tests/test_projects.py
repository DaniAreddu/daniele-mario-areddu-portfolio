from __future__ import annotations


async def test_project_list(client):
    response = await client.get("/api/v1/projects")
    assert response.status_code == 200
    body = response.json()
    slugs = {item["slug"] for item in body}
    assert "municipal-data-reconciliation-platform" in slugs
    # No invented external links.
    for item in body:
        if item["external_url"] is not None:
            assert item["external_url"].startswith("http")


async def test_project_detail(client):
    response = await client.get("/api/v1/projects/municipal-data-reconciliation-platform")
    assert response.status_code == 200
    body = response.json()
    assert body["title"] == "Municipal Data Reconciliation Platform"
    assert "PostGIS" in body["technologies"]
    assert body["related_skills"]
    assert "70%" in body["outcome"]


async def test_project_detail_not_found(client):
    response = await client.get("/api/v1/projects/does-not-exist")
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "not_found"
    assert "error" in body and "message" in body["error"]
