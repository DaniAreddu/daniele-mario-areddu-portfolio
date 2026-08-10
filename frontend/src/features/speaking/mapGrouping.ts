import type { GeoJsonFeature } from "@/types/api";

/** Groups features that sit at (essentially) the same coordinate, so a click
 * on the map can reveal every event at that location — e.g. two DevFest
 * Vicenza editions, or both Toronto appearances — rather than only the one
 * MapLibre happens to render on top when markers are exactly coincident. */
export function groupFeaturesByCoordinate(features: GeoJsonFeature[]): GeoJsonFeature[][] {
  const groups = new Map<string, GeoJsonFeature[]>();
  for (const feature of features) {
    const [lon, lat] = feature.geometry.coordinates;
    const key = `${lon.toFixed(3)},${lat.toFixed(3)}`;
    const existing = groups.get(key);
    if (existing) existing.push(feature);
    else groups.set(key, [feature]);
  }
  return [...groups.values()];
}

/** Returns every event slug sharing a location with the given slug
 * (including the slug itself), or just `[slug]` if it's alone there. */
export function findGroupSlugsFor(features: GeoJsonFeature[], slug: string): string[] {
  const group = groupFeaturesByCoordinate(features).find((candidate) =>
    candidate.some((feature) => feature.properties.slug === slug),
  );
  return group ? group.map((feature) => feature.properties.slug) : [slug];
}

/** Deduplicates a set of clicked/queried features down to unique event
 * slugs, preserving first-seen order. */
export function uniqueSlugs(features: GeoJsonFeature[]): string[] {
  const seen = new Set<string>();
  const result: string[] = [];
  for (const feature of features) {
    const { slug } = feature.properties;
    if (!seen.has(slug)) {
      seen.add(slug);
      result.push(slug);
    }
  }
  return result;
}
