import { useTranslation } from "react-i18next";

import { formatEventDate } from "@/features/speaking/EventList";
import { sortEventsAscending } from "@/features/speaking/eventSort";
import { StatusBadge } from "@/features/speaking/StatusBadge";
import type { EventItem } from "@/types/api";

interface UpcomingEventsProps {
  events: EventItem[];
  onSelect: (slug: string) => void;
}

/** A dedicated "Next stops" showcase for engagements that haven't happened
 * yet. Deliberately never presented as completed talks — each card carries
 * its actual status (upcoming/incoming) as text, not just color. */
export function UpcomingEvents({ events, onSelect }: UpcomingEventsProps) {
  const { t, i18n } = useTranslation();

  if (events.length === 0) return null;

  const sorted = sortEventsAscending(events);

  return (
    <section className="mt-16 border-t border-ink/10 pt-10">
      <h2 className="eyebrow">{t("speaking.upcoming.title")}</h2>
      <p className="mt-1 max-w-xl text-sm text-ink-faint">{t("speaking.upcoming.intro")}</p>

      <ul className="mt-6 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {sorted.map((event) => (
          <li key={event.slug} className="border-t-2 border-cobalt/40 pt-4">
            <button
              type="button"
              onClick={() => onSelect(event.slug)}
              className="w-full text-left"
            >
              <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">
                {formatEventDate(event, i18n.language)}
              </p>
              <p className="mt-1 font-mono text-xs uppercase tracking-wide text-cobalt">
                {event.city ?? event.country}
              </p>
              <p className="mt-2 font-serif text-xl text-ink">{event.event_name}</p>
              <div className="mt-3">
                <StatusBadge status={event.status} />
              </div>
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
}
