import { useState } from "react";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { ConfirmDialog } from "@/admin/components/ui/ConfirmDialog";
import { Input } from "@/admin/components/ui/Input";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminRedirectList,
  useCreateRedirect,
  useDeleteRedirect,
} from "@/admin/hooks/useAdminRedirects";
import type { RedirectWritePayload } from "@/admin/types/siteAdmin";

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

function emptyPayload(): RedirectWritePayload {
  return { source_path: "", destination_path: "", status_code: 301, enabled: true };
}

function NewRedirectForm() {
  const [values, setValues] = useState<RedirectWritePayload>(emptyPayload());
  const [error, setError] = useState<string | null>(null);
  const createRedirect = useCreateRedirect();
  const { showToast } = useAdminToast();

  async function handleCreate() {
    if (!values.source_path.trim() || !values.destination_path.trim()) return;
    setError(null);
    try {
      await createRedirect.mutateAsync(values);
      setValues(emptyPayload());
      showToast({ title: "Added" });
    } catch (createError) {
      setError(describeError(createError));
    }
  }

  return (
    <Card className="space-y-3">
      <h2 className="font-serif text-lg text-ink">New redirect</h2>
      {error ? (
        <p role="alert" className="text-sm text-red-700">
          {error}
        </p>
      ) : null}
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <Input
          value={values.source_path}
          onChange={(e) => setValues({ ...values, source_path: e.target.value })}
          placeholder="/old-path"
          aria-label="Source path"
        />
        <Input
          value={values.destination_path}
          onChange={(e) => setValues({ ...values, destination_path: e.target.value })}
          placeholder="/new-path"
          aria-label="Destination path"
        />
        <Input
          type="number"
          value={values.status_code}
          onChange={(e) => setValues({ ...values, status_code: Number(e.target.value) })}
          aria-label="Status code"
        />
      </div>
      <p className="text-xs text-ink-faint">
        Both paths must be internal (start with /) — external redirect targets are not
        supported.
      </p>
      <Button onClick={() => void handleCreate()} disabled={createRedirect.isPending}>
        Add
      </Button>
    </Card>
  );
}

export default function RedirectsPage() {
  const { data: redirects, isLoading, isError } = useAdminRedirectList();
  const deleteRedirect = useDeleteRedirect();
  const { showToast } = useAdminToast();

  return (
    <div className="max-w-3xl">
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Site</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Redirects</h1>
      </div>

      <div className="mt-6">
        <NewRedirectForm />
      </div>

      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError ? (
          <p className="text-sm text-red-700">Could not load redirects.</p>
        ) : redirects && redirects.length > 0 ? (
          <div className="overflow-x-auto rounded-2xl border border-ink/10">
            <table className="w-full min-w-[480px] border-collapse text-left text-sm">
              <thead>
                <tr className="border-b border-ink/10 bg-paper-warm text-xs uppercase tracking-wide text-ink-faint">
                  <th className="px-4 py-3 font-medium">From</th>
                  <th className="px-4 py-3 font-medium">To</th>
                  <th className="px-4 py-3 font-medium">Status</th>
                  <th className="px-4 py-3 font-medium" />
                </tr>
              </thead>
              <tbody>
                {redirects.map((redirect) => (
                  <tr key={redirect.id} className="border-b border-ink/5 last:border-0">
                    <td className="px-4 py-3 font-mono text-xs">{redirect.source_path}</td>
                    <td className="px-4 py-3 font-mono text-xs">{redirect.destination_path}</td>
                    <td className="px-4 py-3 text-ink-soft">{redirect.status_code}</td>
                    <td className="px-4 py-3 text-right">
                      <ConfirmDialog
                        trigger={
                          <Button variant="danger" className="px-3 py-1 text-xs">
                            Delete
                          </Button>
                        }
                        title="Delete this redirect?"
                        description="Requests to this path will stop being redirected."
                        confirmLabel="Delete"
                        onConfirm={async () => {
                          await deleteRedirect.mutateAsync(redirect.id);
                          showToast({ title: "Deleted" });
                        }}
                      />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-ink/15 p-10 text-center">
            <p className="text-ink-soft">No redirects yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
