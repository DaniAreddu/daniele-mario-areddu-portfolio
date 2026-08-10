import { useState } from "react";

import { Card } from "@/admin/components/ui/Card";
import { Select } from "@/admin/components/ui/Select";
import { useAdminAuditLog, useAdminRecentRevisions } from "@/admin/hooks/useAdminDashboard";

const ENTITY_TYPES = [
  "",
  "event",
  "project",
  "experience",
  "education",
  "community_activity",
  "recognition",
  "skill",
  "skill_category",
  "media_asset",
  "navigation_item",
  "social_link",
  "redirect",
  "profile",
  "biography",
  "community_profile",
  "site_settings",
  "seo_settings",
  "homepage_settings",
  "homepage_feature",
];

export default function AuditLogPage() {
  const [entityType, setEntityType] = useState("");
  const { data: events, isLoading, isError } = useAdminAuditLog(entityType || undefined);
  const { data: revisions } = useAdminRecentRevisions();

  return (
    <div>
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Activity</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Audit log</h1>
      </div>

      <div className="mt-6 max-w-xs">
        <Select
          value={entityType}
          onChange={(e) => setEntityType(e.target.value)}
          aria-label="Filter by content type"
        >
          <option value="">All content types</option>
          {ENTITY_TYPES.filter(Boolean).map((type) => (
            <option key={type} value={type}>
              {type.replace(/_/g, " ")}
            </option>
          ))}
        </Select>
      </div>

      <Card className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError ? (
          <p className="text-sm text-red-700">Could not load the audit log.</p>
        ) : events && events.length > 0 ? (
          <ul className="space-y-3">
            {events.map((event) => (
              <li
                key={event.id}
                className="flex flex-wrap items-center justify-between gap-3 border-b border-ink/5 pb-3 text-sm last:border-0"
              >
                <div>
                  <p className="text-ink">{event.summary || event.action}</p>
                  <p className="font-mono text-xs text-ink-faint">
                    {event.action}
                    {event.entity_type ? ` · ${event.entity_type}#${event.entity_id}` : ""}
                    {event.actor_email ? ` · ${event.actor_email}` : ""}
                  </p>
                </div>
                <span className="whitespace-nowrap text-xs text-ink-faint">
                  {new Date(event.created_at).toLocaleString()}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-sm text-ink-faint">No audit events yet.</p>
        )}
      </Card>

      <Card className="mt-6">
        <h2 className="font-serif text-lg text-ink">Recent revisions</h2>
        {revisions && revisions.length > 0 ? (
          <ul className="mt-4 space-y-2">
            {revisions.map((revision) => (
              <li
                key={revision.id}
                className="flex flex-wrap items-center justify-between gap-2 border-b border-ink/5 pb-2 text-sm last:border-0"
              >
                <span className="font-mono text-xs text-ink-faint">
                  {revision.entity_type}#{revision.entity_id}
                </span>
                <span className="text-ink-soft">
                  {revision.created_by_email ?? "unknown"} —{" "}
                  {new Date(revision.created_at).toLocaleString()}
                </span>
              </li>
            ))}
          </ul>
        ) : (
          <p className="mt-3 text-sm text-ink-faint">No revisions yet.</p>
        )}
      </Card>
    </div>
  );
}
