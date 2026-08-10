import { useParams } from "react-router-dom";

import { Card } from "@/admin/components/ui/Card";
import { useAdminExperiencePreview } from "@/admin/hooks/useAdminExperience";

export default function ExperiencePreviewPage() {
  const params = useParams<{ id: string }>();
  const id = Number(params.id);
  const { data: item, isLoading, isError } = useAdminExperiencePreview(id);

  return (
    <div className="max-w-2xl">
      <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Preview</p>
      <h1 className="mt-2 font-serif text-3xl text-ink">How this will look publicly</h1>
      <p className="mt-2 text-sm text-ink-soft">
        Visible only to you — publishing will show exactly this on the public site.
      </p>
      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError || !item ? (
          <p className="text-sm text-red-700">Could not load this entry.</p>
        ) : (
          <Card className="space-y-4">
            <div>
              <h2 className="font-serif text-2xl text-ink">{item.role}</h2>
              <p className="text-ink-soft">
                {item.organization}
                {item.location ? ` — ${item.location}` : ""}
              </p>
            </div>
            <p className="text-ink-soft">{item.summary}</p>
            {item.highlights.length > 0 ? (
              <ul className="list-disc space-y-1 pl-5 text-sm text-ink-soft">
                {item.highlights.map((highlight) => (
                  <li key={highlight}>{highlight}</li>
                ))}
              </ul>
            ) : null}
            <div className="flex flex-wrap gap-2">
              {item.technologies.map((tech) => (
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
