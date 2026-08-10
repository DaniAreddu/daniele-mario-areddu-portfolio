import { useParams } from "react-router-dom";

import { Card } from "@/admin/components/ui/Card";
import { useAdminEducationPreview } from "@/admin/hooks/useAdminEducation";

export default function EducationPreviewPage() {
  const params = useParams<{ id: string }>();
  const id = Number(params.id);
  const { data: item, isLoading, isError } = useAdminEducationPreview(id);

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
          <Card className="space-y-2">
            <h2 className="font-serif text-2xl text-ink">{item.degree}</h2>
            <p className="text-ink-soft">
              {item.institution}
              {item.location ? ` — ${item.location}` : ""}
            </p>
            <p className="text-sm text-ink-faint">
              {item.start_year ?? "?"} – {item.is_ongoing ? "present" : (item.end_year ?? "?")}
            </p>
            {item.description ? <p className="text-ink-soft">{item.description}</p> : null}
          </Card>
        )}
      </div>
    </div>
  );
}
