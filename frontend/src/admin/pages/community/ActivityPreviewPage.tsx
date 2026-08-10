import { useParams } from "react-router-dom";

import { Card } from "@/admin/components/ui/Card";
import { useAdminActivityPreview } from "@/admin/hooks/useAdminCommunity";

export default function ActivityPreviewPage() {
  const params = useParams<{ id: string }>();
  const id = Number(params.id);
  const { data: item, isLoading, isError } = useAdminActivityPreview(id);

  return (
    <div className="max-w-2xl">
      <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Preview</p>
      <h1 className="mt-2 font-serif text-3xl text-ink">How this will look publicly</h1>
      <p className="mt-2 text-sm text-ink-soft">
        Visible only to you — publishing will show exactly this on the public Community page.
      </p>
      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError || !item ? (
          <p className="text-sm text-red-700">Could not load this activity.</p>
        ) : (
          <Card className="space-y-2">
            <h2 className="font-serif text-2xl text-ink">{item.title}</h2>
            <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">
              {item.activity_type}
              {item.activity_date ? ` — ${item.activity_date}` : ""}
            </p>
            <p className="text-ink-soft">{item.description}</p>
            {item.url ? (
              <a
                href={item.url}
                target="_blank"
                rel="noreferrer noopener"
                className="text-cobalt underline"
              >
                Visit ↗
              </a>
            ) : null}
          </Card>
        )}
      </div>
    </div>
  );
}
