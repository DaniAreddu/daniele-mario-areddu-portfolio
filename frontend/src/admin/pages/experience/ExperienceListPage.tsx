import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { Badge } from "@/admin/components/ui/Badge";
import { Input } from "@/admin/components/ui/Input";
import { LinkButton } from "@/admin/components/ui/LinkButton";
import { useAdminExperienceList } from "@/admin/hooks/useAdminExperience";
import type { ExperienceListItem } from "@/admin/types/experience";

function publicationTone(status: ExperienceListItem["publication_status"]) {
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

export default function ExperienceListPage() {
  const [showTrashed, setShowTrashed] = useState(false);
  const [search, setSearch] = useState("");
  const { data: items, isLoading, isError } = useAdminExperienceList(showTrashed);

  const filtered = useMemo(() => {
    if (!items) return [];
    const query = search.trim().toLowerCase();
    if (!query) return items;
    return items.filter((item) => item.organization.toLowerCase().includes(query));
  }, [items, search]);

  return (
    <div>
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Experience</p>
          <h1 className="mt-2 font-serif text-3xl text-ink">Work history</h1>
        </div>
        <LinkButton to="/admin/experience/new">New experience</LinkButton>
      </div>

      <div className="mt-6 flex flex-wrap items-center gap-3">
        <Input
          value={search}
          onChange={(event) => setSearch(event.target.value)}
          placeholder="Search by organization"
          className="max-w-xs"
          aria-label="Search experience"
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
        <p className="mt-8 text-sm text-red-700">Could not load experience.</p>
      ) : filtered.length === 0 ? (
        <div className="mt-8 rounded-2xl border border-dashed border-ink/15 p-10 text-center">
          <p className="text-ink-soft">
            {showTrashed ? "Trash is empty." : "No experience yet."}
          </p>
        </div>
      ) : (
        <div className="mt-6 overflow-x-auto rounded-2xl border border-ink/10">
          <table className="w-full min-w-[560px] border-collapse text-left text-sm">
            <thead>
              <tr className="border-b border-ink/10 bg-paper-warm text-xs uppercase tracking-wide text-ink-faint">
                <th className="px-4 py-3 font-medium">Organization</th>
                <th className="px-4 py-3 font-medium">Role</th>
                <th className="px-4 py-3 font-medium">Current</th>
                <th className="px-4 py-3 font-medium">Visibility</th>
              </tr>
            </thead>
            <tbody>
              {filtered.map((item) => (
                <tr key={item.id} className="border-b border-ink/5 last:border-0">
                  <td className="px-4 py-3">
                    <Link
                      to={`/admin/experience/${item.id}`}
                      className="font-medium text-ink hover:text-cobalt"
                    >
                      {item.organization}
                    </Link>
                  </td>
                  <td className="px-4 py-3 text-ink-soft">{item.role_en}</td>
                  <td className="px-4 py-3 text-ink-soft">{item.is_current ? "Yes" : "—"}</td>
                  <td className="px-4 py-3">
                    <Badge tone={publicationTone(item.publication_status)}>
                      {item.publication_status}
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
