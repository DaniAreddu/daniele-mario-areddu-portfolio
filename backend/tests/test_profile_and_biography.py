from __future__ import annotations


async def test_profile_default_locale(client):
    response = await client.get("/api/v1/profile")
    assert response.status_code == 200
    body = response.json()
    assert body["full_name"] == "Daniele Mario Areddu"
    assert "Backend & AI Developer" in body["roles"]
    assert body["public_email"] == "danielemario@areddu.it"
    assert body["tagline"] == "Building intelligent systems. Sharing what I learn around the world."
    # Unverified social links must never be guessed.
    assert body["github_url"] is None
    assert body["linkedin_url"] is None


async def test_profile_italian_locale(client):
    response = await client.get("/api/v1/profile?lang=it")
    assert response.status_code == 200
    body = response.json()
    assert "Costruisco sistemi intelligenti" in body["tagline"]


async def test_biography_locales_differ(client):
    en = (await client.get("/api/v1/biography")).json()
    it = (await client.get("/api/v1/biography?lang=it")).json()
    assert en["micro"] != it["micro"]
    assert "Global Technologies Italia" in en["short"]


async def test_biography_accept_language_header(client):
    it_by_param = (await client.get("/api/v1/biography?lang=it")).json()
    it_by_header = (
        await client.get("/api/v1/biography", headers={"Accept-Language": "it-IT,it;q=0.9"})
    ).json()
    assert it_by_header["micro"] == it_by_param["micro"]
