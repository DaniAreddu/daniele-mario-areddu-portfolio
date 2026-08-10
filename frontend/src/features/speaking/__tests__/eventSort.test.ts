import {
  compareEventsDescending,
  sortEventsAscending,
  sortEventsDescending,
} from "@/features/speaking/eventSort";
import type { EventItem } from "@/types/api";

function event(slug: string, overrides: Partial<EventItem> = {}): EventItem {
  return {
    slug,
    event_name: slug,
    session_title: null,
    talk_title: null,
    short_description: null,
    full_description: null,
    start_date: null,
    end_date: null,
    year: 2026,
    month: null,
    city: null,
    country: null,
    continent: null,
    latitude: null,
    longitude: null,
    venue: null,
    format: "conference",
    language: "en",
    topics: [],
    event_url: null,
    slides_url: null,
    recording_url: null,
    image: null,
    status: "completed",
    sessions_count: 1,
    is_featured: false,
    is_international_milestone: false,
    ...overrides,
  };
}

describe("sortEventsDescending", () => {
  it("orders by year, newest first — never by id/created_at/insertion order", () => {
    const events = [
      event("older-2023", { year: 2023 }),
      event("newest-2026", { year: 2026 }),
      event("middle-2025", { year: 2025 }),
    ];

    expect(sortEventsDescending(events).map((e) => e.slug)).toEqual([
      "newest-2026",
      "middle-2025",
      "older-2023",
    ]);
  });

  it("orders same-year events by month, latest month first", () => {
    const events = [
      event("march", { year: 2026, month: 3 }),
      event("september", { year: 2026, month: 9 }),
      event("january", { year: 2026, month: 1 }),
    ];

    expect(sortEventsDescending(events).map((e) => e.slug)).toEqual([
      "september",
      "march",
      "january",
    ]);
  });

  it("orders same-year-and-month events by exact day, latest day first", () => {
    const events = [
      event("early", { year: 2026, month: 9, start_date: "2026-09-05" }),
      event("late", { year: 2026, month: 9, start_date: "2026-09-20" }),
    ];

    expect(sortEventsDescending(events).map((e) => e.slug)).toEqual(["late", "early"]);
  });

  it("preserves partial dates: a known-month-only event never gets an invented day, and sorts after known-day events in the same year+month", () => {
    const monthOnly = event("september-month-only", { year: 2026, month: 9, start_date: null });
    const withDay = event("september-with-day", {
      year: 2026,
      month: 9,
      start_date: "2026-09-01",
    });

    const sorted = sortEventsDescending([monthOnly, withDay]);
    expect(sorted.map((e) => e.slug)).toEqual(["september-with-day", "september-month-only"]);
    // The partial-date event's fields are untouched — no day was invented.
    expect(sorted[1].start_date).toBeNull();
  });

  it("sorts a year-known-only event after same-year events with a known month, in both directions", () => {
    const yearOnly = event("year-only", { year: 2026, month: null });
    const withMonth = event("with-month", { year: 2026, month: 1 });

    expect(sortEventsDescending([yearOnly, withMonth]).map((e) => e.slug)).toEqual([
      "with-month",
      "year-only",
    ]);
    expect(sortEventsAscending([yearOnly, withMonth]).map((e) => e.slug)).toEqual([
      "with-month",
      "year-only",
    ]);
  });
});

describe("sortEventsAscending", () => {
  it("orders by year, soonest first, for upcoming/next-stops showcases", () => {
    const events = [
      event("2026", { year: 2026 }),
      event("2024", { year: 2024 }),
      event("2025", { year: 2025 }),
    ];

    expect(sortEventsAscending(events).map((e) => e.slug)).toEqual(["2024", "2025", "2026"]);
  });
});

describe("compareEventsDescending", () => {
  it("is a stable, deterministic tiebreak (by slug) for fully identical dates", () => {
    const a = event("b-slug", { year: 2026, month: 9, start_date: "2026-09-01" });
    const b = event("a-slug", { year: 2026, month: 9, start_date: "2026-09-01" });
    expect(compareEventsDescending(a, b)).toBeGreaterThan(0);
    expect(compareEventsDescending(b, a)).toBeLessThan(0);
  });
});
