from __future__ import annotations


async def test_education_list(client):
    response = await client.get("/api/v1/education")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    institutions = {item["institution"] for item in body}
    assert "University of Calabria" in institutions
    # The technical institute's start year is genuinely unknown; must be null, never guessed.
    vallauri = next(item for item in body if "Vallauri" in item["institution"])
    assert vallauri["start_year"] is None
    assert vallauri["end_year"] == 2025


async def test_experience_list(client):
    response = await client.get("/api/v1/experiences")
    assert response.status_code == 200
    body = response.json()
    assert body[0]["organization"] == "Global Technologies Italia"
    assert body[0]["is_current"] is True


async def test_skills_grouped_by_category(client):
    response = await client.get("/api/v1/skills")
    assert response.status_code == 200
    body = response.json()
    slugs = {category["slug"] for category in body}
    assert slugs == {
        "backend-engineering",
        "artificial-intelligence",
        "data-platforms",
        "engineering-practices",
    }
    backend = next(c for c in body if c["slug"] == "backend-engineering")
    assert any(skill["name"] == "FastAPI" for skill in backend["skills"])
    # No percentages or star ratings anywhere in the skill payload.
    for category in body:
        for skill in category["skills"]:
            assert set(skill.keys()) == {"name", "context"}
