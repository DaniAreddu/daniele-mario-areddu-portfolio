import { ExternalLink, FileText, PlayCircle, X } from "lucide-react";
import { useEffect, useRef } from "react";
import { useTranslation } from "react-i18next";

import { formatEventDate } from "@/features/speaking/EventList";
import { StatusBadge } from "@/features/speaking/StatusBadge";
import type { EventItem } from "@/types/api";

interface EventDetailPanelProps {
  event: EventItem;
  onClose: () => void;
}

export function EventDetailPanel({ event, onClose }: EventDetailPanelProps) {
  const { t, i18n } = useTranslation();
  const headingRef = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    headingRef.current?.focus();
  }, [event.slug]);

  const place = [event.city, event.country].filter(Boolean).join(", ");
  const dateLabel = formatEventDate(event, i18n.language);

  return (
    <div
      role="dialog"
      aria-modal="false"
      aria-labelledby="event-detail-heading"
      className="rounded-2xl border border-ink/10 bg-paper p-6 shadow-sm"
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="eyebrow">{place || event.continent}</p>
          <h3
            id="event-detail-heading"
            ref={headingRef}
            tabIndex={-1}
            className="mt-1 font-serif text-2xl text-ink outline-none"
          >
            {event.event_name}
          </h3>
          <div className="mt-2 flex flex-wrap items-center gap-2">
            <span className="font-mono text-xs text-ink-faint">{dateLabel}</span>
            <StatusBadge status={event.status} />
            {event.is_international_milestone ? (
              <span className="rounded-full border border-cobalt/30 px-2 py-0.5 font-mono text-[0.65rem] uppercase tracking-wide text-cobalt">
                {t("speaking.eventDetail.milestoneNote")}
              </span>
            ) : null}
          </div>
        </div>
        <button
          type="button"
          onClick={onClose}
          aria-label={t("speaking.eventDetail.close")}
          className="rounded-full border border-ink/15 p-2 text-ink-faint hover:text-ink"
        >
          <X size={16} aria-hidden="true" />
        </button>
      </div>

      {event.session_title ? (
        <p className="mt-4 font-serif text-lg text-ink-soft">{event.session_title}</p>
      ) : null}

      {event.short_description ? (
        <p className="mt-3 text-ink-soft">{event.short_description}</p>
      ) : null}

      <dl className="mt-5 grid grid-cols-2 gap-3 text-sm">
        {event.venue ? (
          <div>
            <dt className="eyebrow">Venue</dt>
            <dd className="text-ink-soft">{event.venue}</dd>
          </div>
        ) : null}
        {event.sessions_count > 1 ? (
          <div>
            <dt className="eyebrow">Sessions</dt>
            <dd className="text-ink-soft">
              {t("speaking.eventDetail.sessions", { count: event.sessions_count })}
            </dd>
          </div>
        ) : null}
        {event.topics.length > 0 ? (
          <div className="col-span-2">
            <dt className="eyebrow">Topics</dt>
            <dd className="mt-1 flex flex-wrap gap-1.5">
              {event.topics.map((topic) => (
                <span
                  key={topic}
                  className="rounded-full border border-ink/15 px-2.5 py-0.5 text-xs text-ink-faint"
                >
                  {topic}
                </span>
              ))}
            </dd>
          </div>
        ) : null}
      </dl>

      <div className="mt-5 flex flex-wrap gap-3">
        {event.event_url ? (
          <a
            href={event.event_url}
            target="_blank"
            rel="noreferrer noopener"
            className="btn-secondary text-xs"
          >
            <ExternalLink size={13} aria-hidden="true" /> {t("speaking.eventDetail.eventSite")}
          </a>
        ) : null}
        {event.slides_url ? (
          <a
            href={event.slides_url}
            target="_blank"
            rel="noreferrer noopener"
            className="btn-secondary text-xs"
          >
            <FileText size={13} aria-hidden="true" /> {t("speaking.eventDetail.slides")}
          </a>
        ) : null}
        {event.recording_url ? (
          <a
            href={event.recording_url}
            target="_blank"
            rel="noreferrer noopener"
            className="btn-secondary text-xs"
          >
            <PlayCircle size={13} aria-hidden="true" /> {t("speaking.eventDetail.recording")}
          </a>
        ) : null}
      </div>
    </div>
  );
}
