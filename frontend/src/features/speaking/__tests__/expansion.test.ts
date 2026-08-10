import { computeExpansionByYear } from "@/features/speaking/expansion";
import type { EventItem } from "@/types/api";

function event(overrides: Partial<EventItem> & { slug: string }): EventItem {
  return {
    event_name: overrides.slug,
    session_title: null,
    short_description: null,
    full_description: null,
    start_date: null,
    end_date: null,
    year: 2025,
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
    talk_title: null,
    ...overrides,
  };
}

describe("computeExpansionByYear", () => {
  it("shows every city for a year with no international appearances yet", () => {
    const events = [
      event({ slug: "a", year: 2023, month: 12, city: "Bari", country: "Italy" }),
    ];
    const result = computeExpansionByYear(events);
    expect(result).toEqual([{ year: 2023, cities: ["Bari"], international: false }]);
  });

  it("narrows to international cities once the speaker goes abroad", () => {
    const events = [
      event({ slug: "italy-1", year: 2025, month: 4, city: "Pisa", country: "Italy" }),
      event({ slug: "abroad-1", year: 2025, month: 7, city: "Tirana", country: "Albania" }),
      event({
        slug: "abroad-2",
        year: 2025,
        month: 11,
        city: "Dallas",
        country: "United States",
      }),
    ];
    const result = computeExpansionByYear(events);
    expect(result).toEqual([{ year: 2025, cities: ["Tirana", "Dallas"], international: true }]);
  });

  it("orders cities chronologically by month within a year", () => {
    const events = [
      event({ slug: "later", year: 2026, month: 9, city: "Toronto", country: "Canada" }),
      event({
        slug: "earlier",
        year: 2026,
        month: 6,
        city: "New York",
        country: "United States",
      }),
    ];
    const result = computeExpansionByYear(events);
    expect(result[0].cities).toEqual(["New York", "Toronto"]);
  });

  it("deduplicates repeat visits to the same city within a year", () => {
    const events = [
      event({ slug: "sofia-1", year: 2026, month: 5, city: "Sofia", country: "Bulgaria" }),
      event({ slug: "sofia-2", year: 2026, month: 10, city: "Sofia", country: "Bulgaria" }),
    ];
    const result = computeExpansionByYear(events);
    expect(result[0].cities).toEqual(["Sofia"]);
  });

  it("returns years in ascending order", () => {
    const events = [
      event({ slug: "a", year: 2026, city: "Sofia", country: "Bulgaria" }),
      event({ slug: "b", year: 2023, city: "Bari", country: "Italy" }),
      event({ slug: "c", year: 2024, city: "Gela", country: "Italy" }),
    ];
    const result = computeExpansionByYear(events);
    expect(result.map((r) => r.year)).toEqual([2023, 2024, 2026]);
  });

  it("skips events without a known city", () => {
    const events = [event({ slug: "unknown-city", year: 2025, city: null })];
    expect(computeExpansionByYear(events)).toEqual([]);
  });
});
