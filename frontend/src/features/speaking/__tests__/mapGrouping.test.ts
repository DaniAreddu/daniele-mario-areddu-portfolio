import {
  findGroupSlugsFor,
  groupFeaturesByCoordinate,
  uniqueSlugs,
} from "@/features/speaking/mapGrouping";
import type { GeoJsonFeature } from "@/types/api";

function feature(slug: string, coordinates: [number, number]): GeoJsonFeature {
  return {
    type: "Feature",
    geometry: { type: "Point", coordinates },
    properties: {
      slug,
      event_name: slug,
      session_title: null,
      city: null,
      country: null,
      continent: null,
      year: 2026,
      month: null,
      start_date: null,
      end_date: null,
      format: "conference",
      topics: [],
      status: "completed",
      is_featured: false,
      is_international_milestone: false,
      event_url: null,
    },
  };
}

describe("groupFeaturesByCoordinate", () => {
  it("groups features sharing the same coordinate (e.g. two Toronto events)", () => {
    const toronto = [-79.3832, 43.6532] as [number, number];
    const features = [
      feature("m365-toronto-2026", toronto),
      feature("sql-saturday-toronto-2026", toronto),
      feature("gdg-almaty-2026", [76.8897, 43.2389]),
    ];

    const groups = groupFeaturesByCoordinate(features);

    expect(groups).toHaveLength(2);
    const torontoGroup = groups.find((g) => g.length === 2);
    expect(torontoGroup?.map((f) => f.properties.slug).sort()).toEqual([
      "m365-toronto-2026",
      "sql-saturday-toronto-2026",
    ]);
  });

  it("keeps genuinely distinct coordinates separate", () => {
    const features = [feature("a", [10, 20]), feature("b", [10.5, 20.5])];
    expect(groupFeaturesByCoordinate(features)).toHaveLength(2);
  });
});

describe("findGroupSlugsFor", () => {
  it("returns every slug at the same location as the given slug", () => {
    const vicenza = [11.5354, 45.5455] as [number, number];
    const features = [
      feature("devfest-vicenza-2025", vicenza),
      feature("devfest-vicenza-2026", vicenza),
    ];
    expect(findGroupSlugsFor(features, "devfest-vicenza-2025").sort()).toEqual([
      "devfest-vicenza-2025",
      "devfest-vicenza-2026",
    ]);
  });

  it("returns just the slug itself when it has no location-mates", () => {
    const features = [feature("solo-event", [1, 1])];
    expect(findGroupSlugsFor(features, "solo-event")).toEqual(["solo-event"]);
  });
});

describe("uniqueSlugs", () => {
  it("deduplicates features queried multiple times at the same point", () => {
    const point = [0, 0] as [number, number];
    const features = [feature("a", point), feature("a", point), feature("b", point)];
    expect(uniqueSlugs(features)).toEqual(["a", "b"]);
  });
});
