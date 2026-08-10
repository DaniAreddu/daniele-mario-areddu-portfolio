import maplibregl, { type GeoJSONSource, type MapGeoJSONFeature } from "maplibre-gl";
import "maplibre-gl/dist/maplibre-gl.css";
import { useEffect, useRef } from "react";

import { uniqueSlugs } from "@/features/speaking/mapGrouping";
import { usePrefersReducedMotion } from "@/hooks/usePrefersReducedMotion";
import type { GeoJsonFeature, GeoJsonFeatureCollection } from "@/types/api";

const MAP_STYLE_URL =
  import.meta.env.VITE_MAP_STYLE_URL ?? "https://tiles.openfreemap.org/styles/liberty";

const SOURCE_ID = "speaking-events";
const UNCLUSTERED_LAYER_ID = "speaking-events-point";
const CLUSTER_LAYER_ID = "speaking-events-clusters";
const CLUSTER_COUNT_LAYER_ID = "speaking-events-cluster-count";

// Half-width, in pixels, of the click hit-box queried around a pointer
// event. Events at the exact same coordinate (e.g. two DevFest Vicenza
// editions) render as perfectly overlapping markers once unclustered, so a
// single-pixel hit test would only ever find the topmost one.
const CLICK_HIT_RADIUS_PX = 6;

interface SpeakingMapProps {
  data: GeoJsonFeatureCollection;
  selectedSlug?: string;
  onSelectEvent: (slug: string) => void;
  /** Called instead of onSelectEvent when a click resolves to more than one
   * event sharing the same location. */
  onSelectGroup: (slugs: string[]) => void;
  onError: () => void;
}

export function SpeakingMap({
  data,
  selectedSlug,
  onSelectEvent,
  onSelectGroup,
  onError,
}: SpeakingMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<maplibregl.Map | null>(null);
  const onSelectEventRef = useRef(onSelectEvent);
  onSelectEventRef.current = onSelectEvent;
  const onSelectGroupRef = useRef(onSelectGroup);
  onSelectGroupRef.current = onSelectGroup;
  const prefersReducedMotion = usePrefersReducedMotion();

  useEffect(() => {
    if (!containerRef.current) return;

    const map = new maplibregl.Map({
      container: containerRef.current,
      style: MAP_STYLE_URL,
      center: [15, 35],
      zoom: 1.4,
      cooperativeGestures: true,
    });
    mapRef.current = map;

    map.addControl(new maplibregl.NavigationControl({ showCompass: false }), "top-right");

    map.on("error", onError);

    map.on("load", () => {
      map.addSource(SOURCE_ID, {
        type: "geojson",
        data: data as unknown as GeoJSON.FeatureCollection,
        cluster: true,
        clusterRadius: 40,
        clusterMaxZoom: 7,
      });

      map.addLayer({
        id: CLUSTER_LAYER_ID,
        type: "circle",
        source: SOURCE_ID,
        filter: ["has", "point_count"],
        paint: {
          "circle-color": "#1E3FE0",
          "circle-opacity": 0.85,
          "circle-radius": ["step", ["get", "point_count"], 16, 5, 20, 10, 26],
        },
      });

      map.addLayer({
        id: CLUSTER_COUNT_LAYER_ID,
        type: "symbol",
        source: SOURCE_ID,
        filter: ["has", "point_count"],
        layout: {
          "text-field": ["get", "point_count_abbreviated"],
          "text-size": 12,
          "text-font": ["Noto Sans Bold"],
        },
        paint: { "text-color": "#F7F3EC" },
      });

      map.addLayer({
        id: UNCLUSTERED_LAYER_ID,
        type: "circle",
        source: SOURCE_ID,
        filter: ["!", ["has", "point_count"]],
        paint: {
          "circle-radius": ["case", ["==", ["get", "slug"], selectedSlug ?? ""], 9, 6],
          "circle-color": [
            "case",
            ["==", ["get", "slug"], selectedSlug ?? ""],
            "#211F1C",
            "#1E3FE0",
          ],
          "circle-stroke-width": 2,
          "circle-stroke-color": "#F7F3EC",
        },
      });

      map.on("click", CLUSTER_LAYER_ID, (event) => {
        const [feature] = map.queryRenderedFeatures(event.point, {
          layers: [CLUSTER_LAYER_ID],
        });
        const clusterId = feature?.properties?.cluster_id;
        const source = map.getSource(SOURCE_ID) as GeoJSONSource;
        if (clusterId === undefined) return;
        void source.getClusterExpansionZoom(clusterId).then((zoom) => {
          const geometry = feature.geometry as GeoJSON.Point;
          map.easeTo({
            center: geometry.coordinates as [number, number],
            zoom,
            duration: prefersReducedMotion ? 0 : 500,
          });
        });
      });

      map.on("click", UNCLUSTERED_LAYER_ID, (event) => {
        // Query a small box around the click, not just the single point,
        // since events sharing a location (e.g. two Toronto appearances)
        // render as perfectly overlapping markers — a 1px hit test would
        // only ever surface the topmost one.
        const box: [maplibregl.PointLike, maplibregl.PointLike] = [
          [event.point.x - CLICK_HIT_RADIUS_PX, event.point.y - CLICK_HIT_RADIUS_PX],
          [event.point.x + CLICK_HIT_RADIUS_PX, event.point.y + CLICK_HIT_RADIUS_PX],
        ];
        const nearby = map.queryRenderedFeatures(box, {
          layers: [UNCLUSTERED_LAYER_ID],
        }) as unknown as GeoJsonFeature[];
        const fallback = (event.features as unknown as GeoJsonFeature[] | undefined) ?? [];
        const slugs = uniqueSlugs(nearby.length > 0 ? nearby : fallback);

        if (slugs.length > 1) onSelectGroupRef.current(slugs);
        else if (slugs.length === 1) onSelectEventRef.current(slugs[0]);
      });

      let hoverPopup: maplibregl.Popup | null = null;
      map.on("mouseenter", UNCLUSTERED_LAYER_ID, (event) => {
        map.getCanvas().style.cursor = "pointer";
        const feature = event.features?.[0] as MapGeoJSONFeature | undefined;
        if (!feature) return;
        const geometry = feature.geometry as GeoJSON.Point;
        hoverPopup = new maplibregl.Popup({
          closeButton: false,
          closeOnClick: false,
          offset: 12,
        })
          .setLngLat(geometry.coordinates as [number, number])
          .setHTML(
            `<strong>${String(feature.properties?.event_name ?? "")}</strong><br/>${String(
              feature.properties?.city ?? feature.properties?.country ?? "",
            )}`,
          )
          .addTo(map);
      });
      map.on("mouseleave", UNCLUSTERED_LAYER_ID, () => {
        map.getCanvas().style.cursor = "";
        hoverPopup?.remove();
        hoverPopup = null;
      });
    });

    return () => {
      map.remove();
      mapRef.current = null;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Keep the source data and highlight in sync with prop changes.
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    const applyUpdates = () => {
      const source = map.getSource(SOURCE_ID) as GeoJSONSource | undefined;
      source?.setData(data as unknown as GeoJSON.FeatureCollection);
      if (map.getLayer(UNCLUSTERED_LAYER_ID)) {
        map.setPaintProperty(UNCLUSTERED_LAYER_ID, "circle-radius", [
          "case",
          ["==", ["get", "slug"], selectedSlug ?? ""],
          9,
          6,
        ]);
        map.setPaintProperty(UNCLUSTERED_LAYER_ID, "circle-color", [
          "case",
          ["==", ["get", "slug"], selectedSlug ?? ""],
          "#211F1C",
          "#1E3FE0",
        ]);
      }
    };
    if (map.isStyleLoaded()) applyUpdates();
    else map.once("load", applyUpdates);
  }, [data, selectedSlug]);

  // Fly to the selected event when it changes (e.g. selected from the list).
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !selectedSlug) return;
    const feature = data.features.find((item) => item.properties.slug === selectedSlug);
    if (!feature) return;
    map.easeTo({
      center: feature.geometry.coordinates,
      zoom: Math.max(map.getZoom(), 4),
      duration: prefersReducedMotion ? 0 : 700,
    });
  }, [selectedSlug, data, prefersReducedMotion]);

  return (
    <div
      ref={containerRef}
      role="application"
      aria-label="Interactive map of speaking engagements"
      className="h-[32rem] w-full rounded-2xl border border-ink/10"
    />
  );
}
