import { usePrefersReducedMotion } from "@/hooks/usePrefersReducedMotion";

/** An abstract, cartographic decoration built from real speaking-destination
 * coordinates projected onto a simple equirectangular grid. Purely
 * decorative: hidden from assistive technology, and its subtle draw-in
 * animation is skipped under prefers-reduced-motion. */
export function RouteMotif({ className }: { className?: string }) {
  const prefersReducedMotion = usePrefersReducedMotion();

  // [lon, lat] for Velletri and a handful of 2025–2026 speaking destinations.
  const points: [number, number][] = [
    [12.7775, 41.6867], // Velletri
    [10.4017, 43.7228], // Pisa
    [19.8187, 41.3275], // Tirana
    [23.3219, 42.6977], // Sofia
    [-96.797, 32.7767], // Dallas
    [76.8897, 43.2389], // Almaty
  ];

  const project = ([lon, lat]: [number, number]) => {
    const x = ((lon + 180) / 360) * 400;
    const y = ((90 - lat) / 180) * 240;
    return [x, y] as const;
  };

  const path = points
    .map(project)
    .map(([x, y], index) => `${index === 0 ? "M" : "L"}${x.toFixed(1)},${y.toFixed(1)}`)
    .join(" ");

  return (
    <svg viewBox="0 0 400 240" className={className} aria-hidden="true" focusable="false">
      <rect x="0" y="0" width="400" height="240" fill="none" />
      {Array.from({ length: 9 }).map((_, i) => (
        <line
          key={`h-${i}`}
          x1={0}
          x2={400}
          y1={(i * 240) / 8}
          y2={(i * 240) / 8}
          stroke="currentColor"
          strokeOpacity={0.08}
        />
      ))}
      {Array.from({ length: 13 }).map((_, i) => (
        <line
          key={`v-${i}`}
          y1={0}
          y2={240}
          x1={(i * 400) / 12}
          x2={(i * 400) / 12}
          stroke="currentColor"
          strokeOpacity={0.08}
        />
      ))}
      <path
        d={path}
        fill="none"
        stroke="currentColor"
        strokeWidth={1.25}
        strokeDasharray={prefersReducedMotion ? undefined : "4 5"}
        className="text-cobalt"
      />
      {points.map(([lon, lat], index) => {
        const [x, y] = project([lon, lat]);
        return (
          <circle
            key={index}
            cx={x}
            cy={y}
            r={index === 0 ? 4 : 2.5}
            fill="currentColor"
            className={index === 0 ? "text-ink" : "text-cobalt"}
          />
        );
      })}
    </svg>
  );
}
