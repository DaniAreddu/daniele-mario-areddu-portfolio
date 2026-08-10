import { List, Map as MapIcon } from "lucide-react";
import { lazy, Suspense, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { ErrorState, LoadingState } from "@/components/AsyncState";
import { EventDetailPanel } from "@/features/speaking/EventDetailPanel";
import { EventFilters } from "@/features/speaking/EventFilters";
import { EventList } from "@/features/speaking/EventList";
import { ExpansionTimeline } from "@/features/speaking/ExpansionTimeline";
import { InternationalMilestones } from "@/features/speaking/InternationalMilestones";
import { MapBoundary } from "@/features/speaking/MapBoundary";
import { SpeakingStats } from "@/features/speaking/SpeakingStats";
import { UpcomingEvents } from "@/features/speaking/UpcomingEvents";
import { useEventFilterState } from "@/features/speaking/useEventFilterState";
import {
  useEventFacets,
  useEvents,
  useEventsGeoJson,
  useEventStats,
  useTalks,
} from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

const SpeakingMap = lazy(() =>
  import("@/features/speaking/SpeakingMap").then((mod) => ({ default: mod.SpeakingMap })),
);

type ViewMode = "map" | "list";

const UPCOMING_STATUSES = new Set(["upcoming", "incoming"]);

export default function SpeakingPage() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const { state, setFilter, selectEvent, clearFilters, hasActiveFilters } =
    useEventFilterState();
  const [viewMode, setViewMode] = useState<ViewMode>("map");
  const [mapFailed, setMapFailed] = useState(false);
  const [locationGroup, setLocationGroup] = useState<string[] | null>(null);

  const facets = useEventFacets();
  const stats = useEventStats();
  const geojson = useEventsGeoJson();
  const talks = useTalks();
  // Unfiltered: drives stats, upcoming, the milestones showcase and the
  // expansion timeline, which should always reflect the whole speaking
  // record regardless of the catalogue's active filters.
  const allEvents = useEvents();
  const events = useEvents({
    year: state.year,
    country: state.country,
    continent: state.continent,
    topic: state.topic,
    format: state.format,
    q: state.q,
  });

  useSeo({
    title: "Speaking — Daniele Mario Areddu",
    description:
      "An international speaking journey from 2023 to 2026 across Europe, North America and Central Asia. Explore the interactive speaking map, upcoming appearances and full event catalogue.",
    path: "/speaking",
    ready: events.isSuccess || events.isError,
  });

  const selectedEvent = useMemo(
    () => events.data?.find((event) => event.slug === state.event),
    [events.data, state.event],
  );

  const groupedEvents = useMemo(
    () =>
      locationGroup
        ? (events.data ?? []).filter((event) => locationGroup.includes(event.slug))
        : [],
    [events.data, locationGroup],
  );

  const handleSelectEvent = (slug: string | undefined) => {
    setLocationGroup(null);
    selectEvent(slug);
  };

  const filteredGeoJson = useMemo(() => {
    if (!geojson.data) return undefined;
    const visibleSlugs = new Set((events.data ?? []).map((event) => event.slug));
    return {
      ...geojson.data,
      features: geojson.data.features.filter((feature) =>
        visibleSlugs.has(feature.properties.slug),
      ),
    };
  }, [geojson.data, events.data]);

  const featuredTalks = talks.data?.filter((talk) => talk.is_featured) ?? [];
  const upcomingEvents =
    allEvents.data?.filter((event) => UPCOMING_STATUSES.has(event.status)) ?? [];
  const milestoneEvents =
    allEvents.data?.filter((event) => event.is_international_milestone) ?? [];

  return (
    <div className="container-editorial py-16 sm:py-24">
      <h1 className="eyebrow">{t("speaking.title")}</h1>
      <p className="mt-4 max-w-2xl font-serif text-2xl text-ink sm:text-3xl">
        {t("speaking.intro")}
      </p>

      {stats.data ? (
        <div className="mt-8">
          <SpeakingStats stats={stats.data} />
        </div>
      ) : null}

      <UpcomingEvents events={upcomingEvents} onSelect={handleSelectEvent} />

      {allEvents.data ? <ExpansionTimeline events={allEvents.data} /> : null}

      {featuredTalks.length > 0 ? (
        <section className="mt-16 border-t border-ink/10 pt-10">
          <h2 className="eyebrow">{t("speaking.featuredTalksTitle")}</h2>
          <ul className="mt-5 grid grid-cols-1 gap-6 sm:grid-cols-3">
            {featuredTalks.map((talk) => (
              <li key={talk.slug} className="border-t border-ink/15 pt-4">
                <p className="font-serif text-lg leading-snug text-ink">{talk.title}</p>
                {talk.summary ? (
                  <p className="mt-2 text-sm text-ink-faint">{talk.summary}</p>
                ) : null}
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <InternationalMilestones events={milestoneEvents} onSelect={handleSelectEvent} />

      <section className="mt-16 border-t border-ink/10 pt-10">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h2 className="eyebrow">{t("speaking.mapTitle")}</h2>
            <p className="mt-1 max-w-xl text-sm text-ink-faint">{t("speaking.mapIntro")}</p>
          </div>
          <div className="inline-flex rounded-full border border-ink/15 p-1">
            <button
              type="button"
              onClick={() => setViewMode("map")}
              aria-pressed={viewMode === "map"}
              className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-sm ${
                viewMode === "map" ? "bg-ink text-paper" : "text-ink-faint"
              }`}
            >
              <MapIcon size={14} aria-hidden="true" /> {t("speaking.mapViewToggle")}
            </button>
            <button
              type="button"
              onClick={() => setViewMode("list")}
              aria-pressed={viewMode === "list"}
              className={`inline-flex items-center gap-1.5 rounded-full px-3 py-1.5 text-sm ${
                viewMode === "list" ? "bg-ink text-paper" : "text-ink-faint"
              }`}
            >
              <List size={14} aria-hidden="true" /> {t("speaking.listViewToggle")}
            </button>
          </div>
        </div>

        <div className="mt-6">
          <EventFilters
            facets={facets.data}
            state={state}
            onChange={setFilter}
            onClear={clearFilters}
            hasActiveFilters={hasActiveFilters}
            resultCount={events.data?.length ?? 0}
          />
        </div>

        {events.isLoading ? (
          <LoadingState />
        ) : events.isError ? (
          <ErrorState onRetry={() => events.refetch()} />
        ) : (
          <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-[2fr_1fr]">
            <div>
              {viewMode === "map" && !mapFailed && filteredGeoJson ? (
                <MapBoundary
                  fallback={
                    <div className="rounded-2xl border border-ink/10 bg-paper-warm p-8 text-center">
                      <p className="font-serif text-lg text-ink">
                        {t("speaking.mapFallbackTitle")}
                      </p>
                      <p className="mt-2 text-sm text-ink-faint">
                        {t("speaking.mapFallbackBody")}
                      </p>
                    </div>
                  }
                >
                  <Suspense
                    fallback={<LoadingState label={t("speaking.mapLoading") ?? undefined} />}
                  >
                    <SpeakingMap
                      data={filteredGeoJson}
                      selectedSlug={state.event}
                      onSelectEvent={handleSelectEvent}
                      onSelectGroup={setLocationGroup}
                      onError={() => setMapFailed(true)}
                    />
                  </Suspense>
                </MapBoundary>
              ) : (
                <EventList
                  events={events.data ?? []}
                  selectedSlug={state.event}
                  onSelect={handleSelectEvent}
                />
              )}
            </div>

            <div>
              {locationGroup && groupedEvents.length > 1 ? (
                <div className="rounded-2xl border border-ink/10 bg-paper p-6 shadow-sm">
                  <p className="eyebrow">{t("speaking.sameLocation.title")}</p>
                  <p className="mt-2 text-sm text-ink-faint">
                    {t("speaking.sameLocation.body")}
                  </p>
                  <ul className="mt-4 divide-y divide-ink/10 border-t border-ink/10">
                    {groupedEvents.map((event) => (
                      <li key={event.slug}>
                        <button
                          type="button"
                          onClick={() => handleSelectEvent(event.slug)}
                          className="w-full py-3 text-left hover:text-cobalt"
                        >
                          <span className="block font-serif text-lg">{event.event_name}</span>
                          <span className="text-xs text-ink-faint">{event.year}</span>
                        </button>
                      </li>
                    ))}
                  </ul>
                </div>
              ) : selectedEvent ? (
                <EventDetailPanel
                  event={selectedEvent}
                  onClose={() => handleSelectEvent(undefined)}
                />
              ) : (
                <p className="rounded-2xl border border-dashed border-ink/15 p-6 text-sm text-ink-faint">
                  {t("speaking.eventCatalogueTitle")}
                </p>
              )}
            </div>
          </div>
        )}
      </section>

      <section className="mt-16 border-t border-ink/10 pt-10">
        <h2 className="eyebrow">{t("speaking.eventCatalogueTitle")}</h2>
        {events.data ? (
          <EventList
            events={events.data}
            selectedSlug={state.event}
            onSelect={handleSelectEvent}
          />
        ) : null}
      </section>

      <div className="mt-16 text-center">
        <Link to={localizedPath("/contact")} className="btn-primary">
          {t("common.inviteToSpeak")}
        </Link>
      </div>
    </div>
  );
}
