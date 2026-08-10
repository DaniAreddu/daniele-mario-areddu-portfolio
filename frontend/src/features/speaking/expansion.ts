import { sortEventsAscending } from "@/features/speaking/eventSort";
import type { EventItem } from "@/types/api";

const HOME_COUNTRY = "Italy";

export interface ExpansionYearGroup {
  year: number;
  cities: string[];
  /** Whether `cities` represents international expansion for this year, or
   * (for years before any international appearance) simply every city
   * spoken in that year. */
  international: boolean;
}

/** Computes, for each year present in the dataset, the sequence of cities
 * that best tells the geographic-expansion story — international cities
 * once the speaking career goes international, or every city beforehand.
 * Entirely derived from real event data: nothing here is a hardcoded list
 * of years or places. */
export function computeExpansionByYear(events: EventItem[]): ExpansionYearGroup[] {
  const sorted = sortEventsAscending(events);

  const byYear = new Map<number, { all: string[]; international: string[] }>();
  for (const event of sorted) {
    if (!event.city) continue;
    const bucket = byYear.get(event.year) ?? { all: [], international: [] };
    if (!bucket.all.includes(event.city)) bucket.all.push(event.city);
    if (
      event.country &&
      event.country !== HOME_COUNTRY &&
      !bucket.international.includes(event.city)
    ) {
      bucket.international.push(event.city);
    }
    byYear.set(event.year, bucket);
  }

  return [...byYear.entries()]
    .sort(([a], [b]) => a - b)
    .map(([year, bucket]) => ({
      year,
      cities: bucket.international.length > 0 ? bucket.international : bucket.all,
      international: bucket.international.length > 0,
    }));
}
