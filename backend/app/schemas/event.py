from __future__ import annotations

from datetime import date
from typing import Any, Literal

from pydantic import BaseModel

from app.schemas.common import ORMModel


class EventOut(ORMModel):
    slug: str
    event_name: str
    session_title: str | None
    short_description: str | None
    full_description: str | None
    start_date: date | None
    end_date: date | None
    year: int
    month: int | None
    city: str | None
    country: str | None
    continent: str | None
    latitude: float | None
    longitude: float | None
    venue: str | None
    format: str
    language: str
    topics: list[str]
    event_url: str | None
    slides_url: str | None
    recording_url: str | None
    image: str | None
    status: str
    sessions_count: int
    is_featured: bool
    is_international_milestone: bool
    talk_title: str | None


class EventFacetsOut(BaseModel):
    years: list[int]
    countries: list[str]
    continents: list[str]
    topics: list[str]
    event_names: list[str]
    formats: list[str]


class EventStatsOut(BaseModel):
    """Numbers computed live from the seeded event dataset — never hardcoded,
    so the displayed figures can never drift from what is actually seeded."""

    total_events: int
    total_countries: int
    total_cities: int
    total_continents: int
    first_year: int
    last_year: int
    international_count: int
    upcoming_count: int
    gdg_devfest_count: int


class GeoJsonGeometry(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]


class GeoJsonFeature(BaseModel):
    type: Literal["Feature"] = "Feature"
    geometry: GeoJsonGeometry
    properties: dict[str, Any]


class GeoJsonFeatureCollection(BaseModel):
    type: Literal["FeatureCollection"] = "FeatureCollection"
    features: list[GeoJsonFeature]
