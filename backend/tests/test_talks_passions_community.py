from __future__ import annotations


async def test_talks_list(client):
    response = await client.get("/api/v1/talks")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 3
    featured = next(t for t in body if t["slug"] == "cloud-to-edge-autonomous-agents")
    assert "gdg-almaty-2026" in featured["event_slugs"]


async def test_passions_list_has_no_generic_hobby_icons_field(client):
    response = await client.get("/api/v1/passions")
    assert response.status_code == 200
    body = response.json()
    assert len(body) >= 6
    for passion in body:
        assert set(passion.keys()) == {"slug", "title", "text", "motif_label"}


async def test_community_profile(client):
    response = await client.get("/api/v1/community")
    assert response.status_code == 200
    body = response.json()
    assert body["name"] == "Velletri.dev"
    assert body["role"] == "Founder & Community Lead"
    assert body["founded_year"] == 2023
    assert len(body["activities"]) >= 1


async def test_journey_localized(client):
    en = (await client.get("/api/v1/journey")).json()
    it = (await client.get("/api/v1/journey?lang=it")).json()
    assert len(en) == len(it)
    assert en[0]["title"] != it[0]["title"]
    speaking_milestones = [m for m in en if m["kind"] == "speaking"]
    assert all(m["event_slug"] for m in speaking_milestones)
