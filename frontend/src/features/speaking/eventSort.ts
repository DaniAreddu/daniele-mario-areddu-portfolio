import type { EventItem } from "@/types/api";

/** Compares two events by real event date only — year, then month, then
 * exact day — never by database id, created_at/updated_at, or insertion
 * order. Events known only to a year, or a year+month, are never assigned an
 * invented day: they simply sort after same-year/same-month events that do
 * have that precision, in both directions. `direction` is `1` for ascending
 * (soonest first) and `-1` for descending (newest first). */
function compareByEventDate(a: EventItem, b: EventItem, direction: 1 | -1): number {
  if (a.year !== b.year) return direction * (a.year - b.year);

  const aHasMonth = a.month != null;
  const bHasMonth = b.month != null;
  if (aHasMonth !== bHasMonth) return aHasMonth ? -1 : 1;
  if (aHasMonth && bHasMonth && a.month !== b.month) {
    return direction * ((a.month as number) - (b.month as number));
  }

  const aHasDate = a.start_date != null;
  const bHasDate = b.start_date != null;
  if (aHasDate !== bHasDate) return aHasDate ? -1 : 1;
  if (aHasDate && bHasDate && a.start_date !== b.start_date) {
    return direction * ((a.start_date as string) < (b.start_date as string) ? -1 : 1);
  }

  return a.slug.localeCompare(b.slug);
}

/** Newest event date first. Use for the main catalogue, admin lists, and
 * same-location map popups. */
export function compareEventsDescending(a: EventItem, b: EventItem): number {
  return compareByEventDate(a, b, -1);
}

/** Soonest upcoming event date first. Use for "Next stops"/upcoming
 * showcases. */
export function compareEventsAscending(a: EventItem, b: EventItem): number {
  return compareByEventDate(a, b, 1);
}

export function sortEventsDescending<T extends EventItem>(events: T[]): T[] {
  return [...events].sort(compareEventsDescending);
}

export function sortEventsAscending<T extends EventItem>(events: T[]): T[] {
  return [...events].sort(compareEventsAscending);
}
