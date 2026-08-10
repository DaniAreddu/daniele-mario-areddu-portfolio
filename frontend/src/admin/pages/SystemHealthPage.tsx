import { Badge } from "@/admin/components/ui/Badge";
import { Card } from "@/admin/components/ui/Card";
import { useAdminSystemHealth } from "@/admin/hooks/useAdminDashboard";

function StatusBadge({ ok }: { ok: boolean }) {
  return <Badge tone={ok ? "success" : "danger"}>{ok ? "OK" : "FAILING"}</Badge>;
}

export default function SystemHealthPage() {
  const { data: health, isLoading, isError } = useAdminSystemHealth();

  return (
    <div className="max-w-2xl">
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">System</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">System health</h1>
      </div>

      {isLoading ? (
        <p className="mt-8 text-sm text-ink-faint">Loading…</p>
      ) : isError || !health ? (
        <p className="mt-8 text-sm text-red-700">Could not load system health.</p>
      ) : (
        <Card className="mt-6 space-y-4">
          <div className="flex items-center justify-between border-b border-ink/5 pb-3">
            <span className="text-sm text-ink-soft">Database connectivity</span>
            <StatusBadge ok={health.database_ok} />
          </div>
          <div className="flex items-center justify-between border-b border-ink/5 pb-3">
            <span className="text-sm text-ink-soft">Migrations</span>
            <Badge
              tone={
                health.migration_status === "up_to_date"
                  ? "success"
                  : health.migration_status === "behind"
                    ? "warning"
                    : "neutral"
              }
            >
              {health.migration_status === "up_to_date"
                ? "Up to date"
                : health.migration_status === "behind"
                  ? `Behind (${health.current_migration ?? "?"} → ${health.head_migration ?? "?"})`
                  : "Unknown"}
            </Badge>
          </div>
          <div className="flex items-center justify-between border-b border-ink/5 pb-3">
            <span className="text-sm text-ink-soft">
              Media storage ({health.storage_backend})
            </span>
            <StatusBadge ok={health.storage_ok} />
          </div>
        </Card>
      )}
    </div>
  );
}
