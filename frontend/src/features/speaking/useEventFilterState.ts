import { useCallback, useMemo } from "react";
import { useSearchParams } from "react-router-dom";

export interface EventFilterState {
  year?: number;
  country?: string;
  continent?: string;
  topic?: string;
  format?: string;
  q?: string;
  event?: string;
}

/** Filter + selection state kept in the URL query string, so a specific
 * filtered view or a single event can be deep-linked and shared. */
export function useEventFilterState() {
  const [searchParams, setSearchParams] = useSearchParams();

  const state: EventFilterState = useMemo(
    () => ({
      year: searchParams.get("year") ? Number(searchParams.get("year")) : undefined,
      country: searchParams.get("country") ?? undefined,
      continent: searchParams.get("continent") ?? undefined,
      topic: searchParams.get("topic") ?? undefined,
      format: searchParams.get("format") ?? undefined,
      q: searchParams.get("q") ?? undefined,
      event: searchParams.get("event") ?? undefined,
    }),
    [searchParams],
  );

  const setFilter = useCallback(
    (key: keyof EventFilterState, value: string | number | undefined) => {
      setSearchParams(
        (previous) => {
          const next = new URLSearchParams(previous);
          if (value === undefined || value === "") next.delete(key);
          else next.set(key, String(value));
          return next;
        },
        { replace: true },
      );
    },
    [setSearchParams],
  );

  const selectEvent = useCallback(
    (slug: string | undefined) => setFilter("event", slug),
    [setFilter],
  );

  const clearFilters = useCallback(() => {
    setSearchParams(
      (previous) => {
        const next = new URLSearchParams(previous);
        for (const key of ["year", "country", "continent", "topic", "format", "q"])
          next.delete(key);
        return next;
      },
      { replace: true },
    );
  }, [setSearchParams]);

  const hasActiveFilters = Boolean(
    state.year || state.country || state.continent || state.topic || state.format || state.q,
  );

  return { state, setFilter, selectEvent, clearFilters, hasActiveFilters };
}
