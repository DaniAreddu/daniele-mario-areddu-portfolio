from __future__ import annotations


async def test_events_list_and_count(client):
    response = await client.get("/api/v1/events")
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 32


async def test_events_filter_by_continent(client):
    response = await client.get("/api/v1/events", params={"continent": "Central Asia"})
    body = response.json()
    assert len(body) == 2
    assert {item["city"] for item in body} == {"Almaty", "Bishkek"}


async def test_events_filter_by_year(client):
    response = await client.get("/api/v1/events", params={"year": 2025})
    body = response.json()
    assert all(item["year"] == 2025 for item in body)
    assert len(body) == 17


async def test_events_filter_by_topic(client):
    response = await client.get("/api/v1/events", params={"topic": "Gemini"})
    body = response.json()
    assert len(body) >= 2
    assert all("Gemini" in item["topics"] for item in body)


async def test_events_filter_by_format(client):
    response = await client.get("/api/v1/events", params={"format": "devfest"})
    body = response.json()
    assert len(body) > 0
    assert all(item["format"] == "devfest" for item in body)


async def test_events_filter_by_status(client):
    response = await client.get("/api/v1/events", params={"status": "incoming"})
    body = response.json()
    assert {item["slug"] for item in body} == {
        "m365-toronto-2026",
        "sql-saturday-toronto-2026",
        "bsides-nova-2026",
    }


async def test_events_filter_by_milestones(client):
    response = await client.get("/api/v1/events", params={"milestones": True})
    body = response.json()
    assert len(body) == 8
    assert all(item["is_international_milestone"] for item in body)


async def test_events_search(client):
    response = await client.get("/api/v1/events", params={"q": "almaty"})
    body = response.json()
    assert len(body) == 1
    assert body[0]["slug"] == "gdg-almaty-2026"


async def test_toronto_has_two_distinct_events(client):
    response = await client.get("/api/v1/events", params={"q": "toronto"})
    body = response.json()
    assert {item["slug"] for item in body} == {"m365-toronto-2026", "sql-saturday-toronto-2026"}
    assert all(item["status"] == "incoming" for item in body)


async def test_madrid_has_exactly_one_deduplicated_event(client):
    """Nerdearla Madrid / Nerdearla España 2025 must be a single appearance,
    not two separate records — see docs/event-management.md."""
    response = await client.get("/api/v1/events", params={"q": "madrid"})
    body = response.json()
    assert len(body) == 1
    assert body[0]["event_name"] == "Nerdearla España 2025"


async def test_event_detail_with_talk_association(client):
    response = await client.get("/api/v1/events/gdg-almaty-2026")
    assert response.status_code == 200
    body = response.json()
    assert body["event_name"] == "Qazaq IT Community Conference"
    assert body["is_international_milestone"] is True
    assert body["talk_title"] == (
        "From Cloud to Edge: Building Autonomous AI Agents with Gemini, ADK and On-Device AI"
    )


async def test_event_detail_not_found(client):
    response = await client.get("/api/v1/events/no-such-event")
    assert response.status_code == 404


async def test_event_facets(client):
    response = await client.get("/api/v1/events/facets")
    assert response.status_code == 200
    body = response.json()
    assert 2023 in body["years"]
    assert 2026 in body["years"]
    assert "Italy" in body["countries"]
    assert "Central Asia" in body["continents"]
    assert "devfest" in body["formats"]


async def test_event_stats_are_computed_from_real_data(client):
    response = await client.get("/api/v1/events/stats")
    assert response.status_code == 200
    body = response.json()
    assert body["total_events"] == 32
    assert body["total_countries"] == 10
    assert body["total_continents"] == 3
    assert body["first_year"] == 2023
    assert body["last_year"] == 2026
    assert body["upcoming_count"] == 5
    assert body["international_count"] > 0
    assert body["gdg_devfest_count"] > 0


async def test_geojson_structure(client):
    response = await client.get("/api/v1/events/geojson")
    assert response.status_code == 200
    assert response.headers["cache-control"] == "public, max-age=300"
    body = response.json()
    assert body["type"] == "FeatureCollection"
    assert len(body["features"]) > 0

    events_response = await client.get("/api/v1/events")
    total_events = len(events_response.json())
    events_with_coords = len(
        [e for e in events_response.json() if e["latitude"] is not None]
    )
    assert len(body["features"]) == events_with_coords
    assert 0 < events_with_coords <= total_events

    for feature in body["features"]:
        assert feature["type"] == "Feature"
        assert feature["geometry"]["type"] == "Point"
        lon, lat = feature["geometry"]["coordinates"]
        assert -180 <= lon <= 180
        assert -90 <= lat <= 90
        assert "slug" in feature["properties"]
        assert "event_name" in feature["properties"]


async def test_geojson_toronto_events_share_coordinates(client):
    response = await client.get("/api/v1/events/geojson")
    body = response.json()
    toronto_features = [
        f for f in body["features"] if f["properties"]["city"] == "Toronto"
    ]
    assert len(toronto_features) == 2
    coords = {tuple(f["geometry"]["coordinates"]) for f in toronto_features}
    assert len(coords) == 1  # same city -> same coordinates, by design


async def test_geojson_handles_events_with_only_a_known_year_gracefully(client):
    """BSides NOVA has a confirmed year but no confirmed month or day —
    the API must represent that honestly rather than guessing a date."""
    response = await client.get("/api/v1/events/geojson")
    body = response.json()
    bsides = next(
        f for f in body["features"] if f["properties"]["slug"] == "bsides-nova-2026"
    )
    assert bsides["properties"]["start_date"] is None
    assert bsides["properties"]["month"] is None
    assert bsides["properties"]["year"] == 2026
