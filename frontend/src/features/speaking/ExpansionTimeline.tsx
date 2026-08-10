import { useTranslation } from "react-i18next";

import { computeExpansionByYear } from "@/features/speaking/expansion";
import type { EventItem } from "@/types/api";

interface ExpansionTimelineProps {
  events: EventItem[];
}

/** Reads the same event data as a pure geographic story: one row per year,
 * showing the cities that mattered most that year (international ones,
 * once the speaking career goes abroad). No decorative airplane animation —
 * just typography, spacing and a restrained connecting line. */
export function ExpansionTimeline({ events }: ExpansionTimelineProps) {
  const { t } = useTranslation();
  const groups = computeExpansionByYear(events);

  if (groups.length === 0) return null;

  return (
    <section className="mt-16 border-t border-ink/10 pt-10">
      <h2 className="eyebrow">{t("speaking.expansion.title")}</h2>
      <p className="mt-1 max-w-xl text-sm text-ink-faint">{t("speaking.expansion.intro")}</p>

      <ol className="relative mt-8 space-y-6 border-l border-ink/15 pl-8">
        {groups.map((group, index) => (
          <li key={group.year} className="relative">
            <span
              aria-hidden="true"
              className="absolute -left-[2.05rem] top-1 h-3 w-3 rounded-full border-2 border-paper bg-cobalt"
            />
            <div className="flex flex-wrap items-baseline gap-3">
              <p className="font-serif text-2xl text-ink">{group.year}</p>
              {index > 0 ? (
                <span aria-hidden="true" className="font-mono text-ink-faint">
                  →
                </span>
              ) : null}
            </div>
            <p className="mt-1 max-w-2xl text-ink-soft">{group.cities.join(" · ")}</p>
          </li>
        ))}
      </ol>
    </section>
  );
}
