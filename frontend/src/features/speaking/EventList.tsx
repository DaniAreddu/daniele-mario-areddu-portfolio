import { useTranslation } from "react-i18next";

import { StatusBadge } from "@/features/speaking/StatusBadge";
import type { EventItem } from "@/types/api";

const MONTH_LABELS_EN = [
  "Jan",
  "Feb",
  "Mar",
  "Apr",
  "May",
  "Jun",
  "Jul",
  "Aug",
  "Sep",
  "Oct",
  "Nov",
  "Dec",
];
const MONTH_LABELS_IT = [
  "Gen",
  "Feb",
  "Mar",
  "Apr",
  "Mag",
  "Giu",
  "Lug",
  "Ago",
  "Set",
  "Ott",
  "Nov",
  "Dic",
];

export function formatEventDate(event: EventItem, locale: string): string {
  const intl = locale === "it" ? "it-IT" : "en-US";
  if (event.start_date) {
    const start = new Date(event.start_date);
    const startLabel = start.toLocaleDateString(intl, {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
    if (!event.end_date || event.end_date === event.start_date) return startLabel;
    const end = new Date(event.end_date);
    const endLabel = end.toLocaleDateString(intl, {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
    return `${startLabel} – ${endLabel}`;
  }
  if (event.month) {
    const labels = locale === "it" ? MONTH_LABELS_IT : MONTH_LABELS_EN;
    return `${labels[event.month - 1]} ${event.year}`;
  }
  return String(event.year);
}

interface EventListProps {
  events: EventItem[];
  selectedSlug?: string;
  onSelect: (slug: string) => void;
}

export function EventList({ events, selectedSlug, onSelect }: EventListProps) {
  const { t, i18n } = useTranslation();

  return (
    <ul
      className="divide-y divide-ink/10 border-t border-ink/10"
      aria-label={t("speaking.eventCatalogueTitle")}
    >
      {events.map((event) => {
        const dateLabel = formatEventDate(event, i18n.language);
        const place = [event.city, event.country].filter(Boolean).join(", ");
        const isSelected = event.slug === selectedSlug;
        return (
          <li key={event.slug}>
            <button
              type="button"
              onClick={() => onSelect(event.slug)}
              aria-current={isSelected ? "true" : undefined}
              className={`grid w-full grid-cols-1 gap-2 py-5 text-left transition-colors sm:grid-cols-[9rem_1fr_auto] sm:items-center ${
                isSelected ? "bg-cobalt/5" : "hover:bg-ink/[0.03]"
              }`}
            >
              <span className="font-mono text-xs text-ink-faint">{dateLabel}</span>
              <span>
                <span className="flex flex-wrap items-center gap-2">
                  <span className="font-serif text-lg text-ink">{event.event_name}</span>
                  <StatusBadge status={event.status} />
                  {event.is_international_milestone ? (
                    <span
                      className="font-mono text-[0.65rem] uppercase tracking-wide text-cobalt"
                      title={t("speaking.eventDetail.milestoneNote") ?? undefined}
                    >
                      ★
                    </span>
                  ) : null}
                </span>
                {event.session_title ? (
                  <span className="mt-0.5 block text-sm text-ink-soft">
                    {event.session_title}
                  </span>
                ) : null}
              </span>
              <span className="text-sm text-ink-faint">{place || event.continent}</span>
            </button>
          </li>
        );
      })}
      {events.length === 0 ? (
        <li className="py-10 text-center text-ink-faint">
          {t("speaking.filters.resultsCount", { count: 0 })}
        </li>
      ) : null}
    </ul>
  );
}
