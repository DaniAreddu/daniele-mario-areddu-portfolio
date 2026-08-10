import { Link } from "react-router-dom";

import { useAdminAuth } from "@/admin/auth/AdminAuthContext";
import { Badge } from "@/admin/components/ui/Badge";
import { Card } from "@/admin/components/ui/Card";
import { useAdminDashboardStats } from "@/admin/hooks/useAdminDashboard";
import type { ContentTypeCounts } from "@/admin/types/dashboard";

const CONTENT_TYPES: Array<{ key: keyof CountsByType; label: string; path: string }> = [
  { key: "events", label: "Speaking", path: "/admin/speaking" },
  { key: "projects", label: "Projects", path: "/admin/projects" },
  { key: "experience", label: "Experience", path: "/admin/experience" },
  { key: "education", label: "Education", path: "/admin/education" },
  { key: "community_activities", label: "Community", path: "/admin/community" },
  { key: "recognition", label: "Recognition", path: "/admin/recognition" },
];

type CountsByType = Record<
  "events" | "projects" | "experience" | "education" | "community_activities" | "recognition",
  ContentTypeCounts
>;

function ContentCard({
  label,
  path,
  counts,
}: {
  label: string;
  path: string;
  counts: ContentTypeCounts;
}) {
  return (
    <Link to={path}>
      <Card className="h-full space-y-3 transition-shadow hover:shadow-md">
        <h3 className="font-serif text-lg text-ink">{label}</h3>
        <div className="flex flex-wrap gap-2">
          <Badge tone="success">{counts.published} published</Badge>
          {counts.draft > 0 ? <Badge tone="warning">{counts.draft} draft</Badge> : null}
          {counts.scheduled > 0 ? (
            <Badge tone="cobalt">{counts.scheduled} scheduled</Badge>
          ) : null}
          {counts.archived > 0 ? (
            <Badge tone="neutral">{counts.archived} archived</Badge>
          ) : null}
          {counts.trashed > 0 ? <Badge tone="danger">{counts.trashed} trashed</Badge> : null}
        </div>
      </Card>
    </Link>
  );
}

function timeAgo(isoDate: string): string {
  const seconds = Math.round((Date.now() - new Date(isoDate).getTime()) / 1000);
  if (seconds < 60) return "just now";
  const minutes = Math.round(seconds / 60);
  if (minutes < 60) return `${minutes}m ago`;
  const hours = Math.round(minutes / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.round(hours / 24);
  return `${days}d ago`;
}

export default function DashboardPage() {
  const { user } = useAdminAuth();
  const { data: stats, isLoading, isError } = useAdminDashboardStats();

  return (
    <div>
      <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Dashboard</p>
      <h1 className="mt-2 font-serif text-3xl text-ink">
        Welcome back{user ? `, ${user.email}` : ""}.
      </h1>

      {isLoading ? (
        <p className="mt-8 text-sm text-ink-faint">Loading…</p>
      ) : isError || !stats ? (
        <p className="mt-8 text-sm text-red-700">Could not load dashboard stats.</p>
      ) : (
        <>
          <div className="mt-6 flex flex-wrap gap-3">
            <Card className="px-4 py-3 text-sm">
              <span className="font-serif text-2xl text-ink">
                {stats.upcoming_events_count}
              </span>
              <span className="ml-2 text-ink-soft">upcoming appearances</span>
            </Card>
            <Card className="px-4 py-3 text-sm">
              <span className="font-serif text-2xl text-ink">{stats.media_count}</span>
              <span className="ml-2 text-ink-soft">media files</span>
            </Card>
          </div>

          <div className="mt-6 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {CONTENT_TYPES.map(({ key, label, path }) => (
              <ContentCard key={key} label={label} path={path} counts={stats[key]} />
            ))}
          </div>

          <Card className="mt-6">
            <h2 className="font-serif text-lg text-ink">Recent activity</h2>
            {stats.recent_activity.length === 0 ? (
              <p className="mt-3 text-sm text-ink-faint">Nothing yet.</p>
            ) : (
              <ul className="mt-4 space-y-2">
                {stats.recent_activity.map((event) => (
                  <li
                    key={event.id}
                    className="flex flex-wrap items-center justify-between gap-2 border-b border-ink/5 pb-2 text-sm last:border-0"
                  >
                    <span className="text-ink-soft">
                      {event.summary || event.action}
                      {event.actor_email ? ` — ${event.actor_email}` : ""}
                    </span>
                    <span className="text-xs text-ink-faint">{timeAgo(event.created_at)}</span>
                  </li>
                ))}
              </ul>
            )}
            <Link
              to="/admin/audit-log"
              className="mt-4 inline-block text-sm text-cobalt hover:underline"
            >
              View full audit log →
            </Link>
          </Card>
        </>
      )}
    </div>
  );
}
