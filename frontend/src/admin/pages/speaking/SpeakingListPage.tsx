import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { useAdminEventList } from "@/admin/hooks/useAdminEvents";
import { Badge } from "@/admin/components/ui/Badge";
import { Input } from "@/admin/components/ui/Input";
import { LinkButton } from "@/admin/components/ui/LinkButton";
import type { EventListItem } from "@/admin/types/event";

const MONTH_LABELS = [
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
] as const;

function formatDate(item: EventListItem): string {
  if (item.month) return `${MONTH_LABELS[item.month - 1]} ${item.year}`;
  return String(item.year);
}

function publicationTone(status: EventListItem["publication_status"]) {
  switch (status) {
    case "PUBLISHED":
      return "success" as const;
    case "SCHEDULED":
      return "cobalt" as const;
    case "ARCHIVED":
      return "neutral" as const;
    default:
      return "warning" as const;
  }
}

export default function SpeakingListPage() {
  const [showTrashed, setShowTrashed] = useState(false);
  const [search, setSearch] = useState("");
  const { data: events, isLoading, isError } = useAdminEventList(showTrashed);

  const filtered = useMemo(() => {
    if (!events) return [];
    const query = search.trim().toLowerCase();
    if (!query) return events;
    return events.filter((event) =>
      [event.event_name, event.city, event.country].some((field) =>
        (field ?? "").toLowerCase().includes(query),
      ),
    );
  }, [events, search]);

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Speaking</p>
          <h1 className="mt-2 font-serif text-3xl text-ink">Appearances</h1>
        </div>
        <LinkButton to="/admin/speaking/new">New appearance</LinkButton>
      </div>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <Input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search by event, city, or country"
          className="max-w-xs"
          aria-label="Search appearances"
        />
        <label className="flex items-center gap-2 text-sm text-ink-soft">
          <input
            type="checkbox"
            checked={showTrashed}
            onChange={(event) => setShowTrashed(event.target.checked)}
            className="h-4 w-4 rounded border-ink/30"
          />
          Show trash
        </label>
      </div>

      {isLoading ? (
        <p className="mt-8 text-sm text-ink-faint">Loading…</p>
      ) : isError ? (
        <p className="mt-8 text-sm text-red-700">Could not load appearances.</p>
      ) : filtered.length === 0 ? (
        <div className="mt-8 rounded-2xl border border-dashed border-ink/15 p-10 text-center">
          <p className="text-ink-soft">
            {showTrashed ? "Trash is empty." : "No appearances yet."}
          </p>
          {!showTrashed ? (
            <Link to="/admin/speaking/new" className="mt-3 inline-block text-cobalt underline">
              Add your first appearance
            </Link>
          ) : null}
        </div>
      ) : (
        <div className="mt-6 overflow-x-auto rounded-2xl border border-ink/10">
          <table className="w-full min-w-[720px] border-collapse text-left text-sm">
            <thead>
              <tr className="border-b border-ink/10 bg-paper-warm text-xs uppercase tracking-wide text-ink-faint">
                <th className="px-4 py-3 font-medium">Event</th>
                <th className="px-4 py-3 font-medium">Location</th>
                <th className="px-4 py-3 font-medium">Date</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Visibility</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((event) => (
                <tr key={event.id} className="border-b border-ink/5 last:border-0">
                  <td className="px-4 py-3">
                    <Link
                      to={`/admin/speaking/${event.id}`}
                      className="font-medium text-ink hover:text-cobalt"
                    >
                      {event.event_name}
                    </Link>
                    {event.is_international_milestone ? (
                      <span
                        className="ml-2"
                        title="International milestone"
                        aria-label="International milestone"
                      >
                        ★
                      </span>
                    ) : null}
                  </td>
                  <td className="px-4 py-3 text-ink-soft">
                    {[event.city, event.country].filter(Boolean).join(", ") || "—"}
                  </td>
                  <td className="px-4 py-3 text-ink-soft">{formatDate(event)}</td>
                  <td className="px-4 py-3 text-ink-soft">{event.status}</td>
                  <td className="px-4 py-3">
                    <Badge tone={publicationTone(event.publication_status)}>
                      {event.publication_status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
