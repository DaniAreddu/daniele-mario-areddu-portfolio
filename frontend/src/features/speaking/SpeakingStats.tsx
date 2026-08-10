import { useTranslation } from "react-i18next";

import type { EventStats } from "@/types/api";

interface SpeakingStatsProps {
  stats: EventStats;
}

/** A restrained, data-driven stat strip. Every number comes straight from
 * `stats` (computed live by the backend from the seeded events — see
 * EventService.get_stats) — nothing here is a hardcoded marketing figure. */
export function SpeakingStats({ stats }: SpeakingStatsProps) {
  const { t } = useTranslation();

  const items: [string, string][] = [
    [String(stats.total_events), t("speaking.stats.talks")],
    [String(stats.total_cities), t("speaking.stats.cities")],
    [String(stats.total_countries), t("speaking.stats.countries")],
    [String(stats.total_continents), t("speaking.stats.continents")],
    [`${stats.first_year} → ${stats.last_year}`, ""],
  ];

  return (
    <dl className="grid grid-cols-2 gap-6 border-t border-ink/10 pt-6 sm:grid-cols-3 lg:grid-cols-5">
      {items.map(([value, label]) => (
        <div key={label || value}>
          <dt className="font-mono text-xs uppercase tracking-wide text-ink-faint">
            {label || "Years active"}
          </dt>
          <dd className="mt-1 font-serif text-2xl text-ink sm:text-3xl">{value}</dd>
        </div>
      ))}
    </dl>
  );
}
