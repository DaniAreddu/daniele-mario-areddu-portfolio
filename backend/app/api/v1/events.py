from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from fastapi.responses import JSONResponse

from app.api.deps import Locale, get_event_service
from app.schemas.event import EventFacetsOut, EventOut, EventStatsOut, GeoJsonFeatureCollection
from app.services.event_service import EventService

router = APIRouter()


@router.get("/events", response_model=list[EventOut])
async def list_events(
    locale: Locale,
    service: Annotated[EventService, Depends(get_event_service)],
    year: Annotated[int | None, Query()] = None,
    country: Annotated[str | None, Query()] = None,
    continent: Annotated[str | None, Query()] = None,
    topic: Annotated[str | None, Query()] = None,
    format: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query()] = None,
    q: Annotated[str | None, Query(max_length=120)] = None,
    featured: Annotated[bool, Query()] = False,
    milestones: Annotated[bool, Query()] = False,
) -> list[EventOut]:
    return await service.list_all(
        locale,
        year=year,
        country=country,
        continent=continent,
        topic=topic,
        format=format,
        status=status,
        q=q,
        featured_only=featured,
        milestones_only=milestones,
    )


@router.get("/events/facets", response_model=EventFacetsOut)
async def get_event_facets(
    service: Annotated[EventService, Depends(get_event_service)],
) -> EventFacetsOut:
    return await service.get_facets()


@router.get("/events/stats", response_model=EventStatsOut)
async def get_event_stats(
    service: Annotated[EventService, Depends(get_event_service)],
) -> JSONResponse:
    stats = await service.get_stats()
    response = JSONResponse(content=stats.model_dump(mode="json"))
    response.headers["Cache-Control"] = "public, max-age=300"
    return response


@router.get("/events/geojson", response_model=GeoJsonFeatureCollection)
async def get_events_geojson(
    service: Annotated[EventService, Depends(get_event_service)],
) -> JSONResponse:
    collection = await service.get_geojson()
    response = JSONResponse(content=collection.model_dump(mode="json"))
    response.headers["Cache-Control"] = "public, max-age=300"
    return response


@router.get("/events/{slug}", response_model=EventOut)
async def get_event(
    slug: str, locale: Locale, service: Annotated[EventService, Depends(get_event_service)]
) -> EventOut:
    return await service.get_by_slug(slug, locale)
