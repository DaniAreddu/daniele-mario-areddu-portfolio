import { useParams } from "react-router-dom";

import { Card } from "@/admin/components/ui/Card";
import { useAdminProjectPreview } from "@/admin/hooks/useAdminProjects";

/**
 * A lighter-weight preview than Speaking's (which reuses the public
 * EventDetailPanel component directly) — ProjectDetailPage fetches from the
 * public, published-only endpoint internally, so it can't be reused as-is
 * for a draft. This renders the same underlying data the public page would.
 */
export default function ProjectsPreviewPage() {
  const params = useParams<{ id: string }>();
  const projectId = Number(params.id);
  const { data: project, isLoading, isError } = useAdminProjectPreview(projectId);

  return (
    <div className="max-w-2xl">
      <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Preview</p>
      <h1 className="mt-2 font-serif text-3xl text-ink">How this will look publicly</h1>
      <p className="mt-2 text-sm text-ink-soft">
        Visible only to you — publishing will show exactly this on the public Projects page.
      </p>
      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError || !project ? (
          <p className="text-sm text-red-700">Could not load this project.</p>
        ) : (
          <Card className="space-y-4">
            <h2 className="font-serif text-2xl text-ink">{project.title}</h2>
            <p className="text-ink-soft">{project.summary}</p>
            {project.external_url ? (
              <a
                href={project.external_url}
                target="_blank"
                rel="noreferrer noopener"
                className="text-cobalt underline"
              >
                View project ↗
              </a>
            ) : null}
            <div className="flex flex-wrap gap-2">
              {project.technologies.map((tech) => (
                <span
                  key={tech}
                  className="rounded-full border border-ink/15 px-3 py-1 text-xs text-ink-faint"
                >
                  {tech}
                </span>
              ))}
            </div>
          </Card>
        )}
      </div>
    </div>
  );
}
