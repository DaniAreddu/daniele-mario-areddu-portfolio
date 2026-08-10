import { useNavigate, useParams } from "react-router-dom";

import { useAdminEventPreview } from "@/admin/hooks/useAdminEvents";
import { EventDetailPanel } from "@/features/speaking/EventDetailPanel";

/**
 * Renders through the exact same public EventDetailPanel component the
 * live /speaking page uses (fed by the authenticated /preview endpoint),
 * rather than a second bespoke preview UI — so what an admin sees here is
 * exactly what publishing will produce.
 */
export default function SpeakingPreviewPage() {
  const params = useParams<{ id: string }>();
  const eventId = Number(params.id);
  const navigate = useNavigate();
  const { data: event, isLoading, isError } = useAdminEventPreview(eventId);

  return (
    <div className="max-w-2xl">
      <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Preview</p>
      <h1 className="mt-2 font-serif text-3xl text-ink">How this will look publicly</h1>
      <p className="mt-2 text-sm text-ink-soft">
        Visible only to you — publishing will show exactly this on the public Speaking page.
      </p>
      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError || !event ? (
          <p className="text-sm text-red-700">Could not load this appearance.</p>
        ) : (
          <EventDetailPanel
            event={event}
            onClose={() => navigate(`/admin/speaking/${eventId}`)}
          />
        )}
      </div>
    </div>
  );
}
