from __future__ import annotations

from app.core.errors import NotFoundError
from app.models.event import Event
from app.repositories.event_repository import EventRepository
from app.schemas.event import (
    EventFacetsOut,
    EventOut,
    EventStatsOut,
    GeoJsonFeature,
    GeoJsonFeatureCollection,
    GeoJsonGeometry,
)
from app.services.localization import pick

# The publicly describable "home base"; anything else counts toward the
# international-appearances statistic.
_HOME_COUNTRY = "Italy"

# Statuses that represent an engagement which hasn't happened yet. Anything
# else ("completed") is past. Never inferred from a date comparison here —
# each event's status is set explicitly in the seed data based on what is
# actually known (see docs/event-management.md).
_UPCOMING_STATUSES = {"upcoming", "incoming"}


def _to_event_out(event: Event, locale: str) -> EventOut:
    return EventOut(
        slug=event.slug,
        event_name=event.event_name,
        session_title=event.session_title,
        short_description=(
            pick(event, "short_description", locale) if event.short_description_en else None
        ),
        full_description=(
            pick(event, "full_description", locale) if event.full_description_en else None
        ),
        start_date=event.start_date,
        end_date=event.end_date,
        year=event.year,
        month=event.month,
        city=event.city,
        country=event.country,
        continent=event.continent,
        latitude=event.latitude,
        longitude=event.longitude,
        venue=event.venue,
        format=event.format,
        language=event.language,
        topics=event.topics,
        event_url=event.event_url,
        slides_url=event.slides_url,
        recording_url=event.recording_url,
        image=event.image,
        status=event.status,
        sessions_count=event.sessions_count,
        is_featured=event.is_featured,
        is_international_milestone=event.is_international_milestone,
        talk_title=event.talk.title if event.talk else event.session_title,
    )


class EventService:
    def __init__(self, repository: EventRepository) -> None:
        self.repository = repository

    async def list_all(
        self,
        locale: str,
        *,
        year: int | None = None,
        country: str | None = None,
        continent: str | None = None,
        topic: str | None = None,
        format: str | None = None,
        status: str | None = None,
        q: str | None = None,
        featured_only: bool = False,
        milestones_only: bool = False,
    ) -> list[EventOut]:
        events = await self.repository.list_all()

        def matches(event: Event) -> bool:
            if year is not None and event.year != year:
                return False
            if country is not None and (event.country or "").lower() != country.lower():
                return False
            if continent is not None and (event.continent or "").lower() != continent.lower():
                return False
            if topic is not None and topic.lower() not in [t.lower() for t in event.topics]:
                return False
            if format is not None and event.format.lower() != format.lower():
                return False
            if status is not None and event.status.lower() != status.lower():
                return False
            if featured_only and not event.is_featured:
                return False
            if milestones_only and not event.is_international_milestone:
                return False
            if q:
                haystack = " ".join(
                    filter(
                        None,
                        [event.event_name, event.session_title, event.city, event.country],
                    )
                ).lower()
                if q.lower() not in haystack:
                    return False
            return True

        return [_to_event_out(event, locale) for event in events if matches(event)]

    async def get_facets(self) -> EventFacetsOut:
        events = await self.repository.list_all()
        return EventFacetsOut(
            years=sorted({event.year for event in events}),
            countries=sorted({event.country for event in events if event.country}),
            continents=sorted({event.continent for event in events if event.continent}),
            topics=sorted({topic for event in events for topic in event.topics}),
            event_names=sorted({event.event_name for event in events}),
            formats=sorted({event.format for event in events}),
        )

    async def get_stats(self) -> EventStatsOut:
        """Every number here is derived from the live dataset — nothing is a
        hardcoded marketing figure, so it can never drift out of sync with
        what is actually seeded (see docs/event-management.md)."""
        events = await self.repository.list_all()
        years = [event.year for event in events]
        gdg_devfest_count = sum(
            1
            for event in events
            if event.format == "devfest"
            or "gdg" in event.event_name.lower()
            or "devfest" in event.event_name.lower()
        )
        return EventStatsOut(
            total_events=len(events),
            total_countries=len({event.country for event in events if event.country}),
            total_cities=len({event.city for event in events if event.city}),
            total_continents=len({event.continent for event in events if event.continent}),
            first_year=min(years) if years else 0,
            last_year=max(years) if years else 0,
            international_count=sum(
                1 for event in events if event.country and event.country != _HOME_COUNTRY
            ),
            upcoming_count=sum(1 for event in events if event.status in _UPCOMING_STATUSES),
            gdg_devfest_count=gdg_devfest_count,
        )

    async def get_by_slug(self, slug: str, locale: str) -> EventOut:
        event = await self.repository.get_by_slug(slug)
        if event is None:
            raise NotFoundError(f"Event '{slug}' was not found.")
        return _to_event_out(event, locale)

    async def get_geojson(self) -> GeoJsonFeatureCollection:
        events = await self.repository.list_with_coordinates()
        features = [
            GeoJsonFeature(
                geometry=GeoJsonGeometry(coordinates=(event.longitude, event.latitude)),
                properties={
                    "slug": event.slug,
                    "event_name": event.event_name,
                    "session_title": event.session_title,
                    "city": event.city,
                    "country": event.country,
                    "continent": event.continent,
                    "year": event.year,
                    "month": event.month,
                    "start_date": event.start_date.isoformat() if event.start_date else None,
                    "end_date": event.end_date.isoformat() if event.end_date else None,
                    "format": event.format,
                    "topics": event.topics,
                    "status": event.status,
                    "is_featured": event.is_featured,
                    "is_international_milestone": event.is_international_milestone,
                    "event_url": event.event_url,
                },
            )
            for event in events
        ]
        return GeoJsonFeatureCollection(features=features)
