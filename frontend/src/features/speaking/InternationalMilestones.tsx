import { useTranslation } from "react-i18next";

import type { EventItem } from "@/types/api";

interface InternationalMilestonesProps {
  events: EventItem[];
  onSelect: (slug: string) => void;
}

/** A visually stronger treatment for the handful of appearances that marked
 * a genuine step into a new country or region — distinct from the general
 * event catalogue, and from "featured talks" (which highlights session
 * content rather than geography). Hierarchy matters: not every event gets
 * this treatment, only `is_international_milestone` ones. */
export function InternationalMilestones({ events, onSelect }: InternationalMilestonesProps) {
  const { t } = useTranslation();

  if (events.length === 0) return null;

  const sorted = [...events].sort(
    (a, b) => a.year - b.year || (a.month ?? 99) - (b.month ?? 99),
  );

  return (
    <section className="mt-16 border-t border-ink/10 pt-10">
      <h2 className="eyebrow">{t("speaking.milestones.title")}</h2>
      <p className="mt-1 max-w-xl text-sm text-ink-faint">{t("speaking.milestones.intro")}</p>

      <ul className="mt-6 grid grid-cols-1 gap-x-10 gap-y-8 sm:grid-cols-2">
        {sorted.map((event) => (
          <li key={event.slug} className="border-l-2 border-cobalt pl-5">
            <button type="button" onClick={() => onSelect(event.slug)} className="text-left">
              <p className="font-serif text-2xl text-ink">{event.city}</p>
              <p className="mt-1 text-ink-soft">{event.event_name}</p>
              <p className="mt-1 font-mono text-xs text-ink-faint">{event.year}</p>
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
