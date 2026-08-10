from __future__ import annotations


async def test_unknown_route_returns_json_envelope(client):
    response = await client.get("/api/v1/this-route-does-not-exist")
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "not_found"


async def test_validation_error_envelope_shape(client):
    response = await client.post("/api/v1/contact", json={"name": "A"})
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert isinstance(body["error"]["details"], list)


async def test_openapi_schema_is_served(client):
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    body = response.json()
    assert body["info"]["title"]
    assert "/api/v1/events/geojson" in body["paths"]
