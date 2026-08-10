import { zodResolver } from "@hookform/resolvers/zod";
import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate, useParams } from "react-router-dom";

import { AdminApiError, adminApiFetch } from "@/admin/api/adminApiClient";
import { Badge } from "@/admin/components/ui/Badge";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { ConfirmDialog } from "@/admin/components/ui/ConfirmDialog";
import { Input } from "@/admin/components/ui/Input";
import { LinkButton } from "@/admin/components/ui/LinkButton";
import { Textarea } from "@/admin/components/ui/Textarea";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminActivity,
  useAdminActivityRevisions,
  useArchiveActivity,
  useCreateActivity,
  usePermanentlyDeleteActivity,
  useRestoreActivity,
  useRestoreActivityRevision,
  useScheduleActivity,
  useTrashActivity,
  useUnpublishActivity,
  useUpdateActivity,
} from "@/admin/hooks/useAdminCommunity";
import {
  activityFormSchema,
  activityFormValuesToPayload,
  activityToFormValues,
  defaultActivityFormValues,
  type ActivityFormValues,
} from "@/admin/pages/community/activityFormSchema";
import type { CommunityActivityAdminDetail } from "@/admin/types/community";

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

function Field({
  label,
  htmlFor,
  error,
  children,
}: {
  label: string;
  htmlFor: string;
  error?: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label htmlFor={htmlFor} className="eyebrow">
        {label}
      </label>
      <div className="mt-2">{children}</div>
      {error ? (
        <p role="alert" className="mt-1 text-sm text-red-700">
          {error}
        </p>
      ) : null}
    </div>
  );
}

export default function ActivityEditorPage() {
  const params = useParams<{ id: string }>();
  const isNew = params.id === undefined;
  const itemId = isNew ? undefined : Number(params.id);
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);

  const { data: item, isLoading } = useAdminActivity(itemId);
  const { data: revisions } = useAdminActivityRevisions(itemId);

  const form = useForm<ActivityFormValues>({
    resolver: zodResolver(activityFormSchema),
    defaultValues: defaultActivityFormValues(),
  });

  useEffect(() => {
    if (item) form.reset(activityToFormValues(item));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [item]);

  const createMutation = useCreateActivity();
  const updateMutation = useUpdateActivity(itemId ?? -1);
  const scheduleMutation = useScheduleActivity(itemId ?? -1);
  const unpublishMutation = useUnpublishActivity(itemId ?? -1);
  const archiveMutation = useArchiveActivity(itemId ?? -1);
  const trashMutation = useTrashActivity(itemId ?? -1);
  const restoreMutation = useRestoreActivity(itemId ?? -1);
  const deleteMutation = usePermanentlyDeleteActivity();
  const restoreRevisionMutation = useRestoreActivityRevision(itemId ?? -1);

  async function persist(values: ActivityFormValues): Promise<CommunityActivityAdminDetail> {
    const payload = activityFormValuesToPayload(values);
    if (isNew) {
      const created = await createMutation.mutateAsync(payload);
      navigate(`/admin/community/${created.id}`, { replace: true });
      return created;
    }
    return updateMutation.mutateAsync(payload);
  }

  const onSaveDraft = form.handleSubmit(async (values) => {
    setServerError(null);
    try {
      await persist(values);
      showToast({ title: "Saved" });
    } catch (error) {
      setServerError(describeError(error));
    }
  });

  const onPublish = form.handleSubmit(async (values) => {
    setServerError(null);
    try {
      const saved = await persist(values);
      await adminApiFetch(`/community/activities/${saved.id}/publish`, { method: "POST" });
      await queryClient.invalidateQueries({ queryKey: ["admin", "community"] });
      showToast({ title: "Published" });
      navigate(`/admin/community/${saved.id}`, { replace: true });
    } catch (error) {
      setServerError(describeError(error));
    }
  });

  if (!isNew && isLoading) {
    return <p className="text-sm text-ink-faint">Loading…</p>;
  }

  return (
    <div className="max-w-3xl">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Community</p>
          <h1 className="mt-2 font-serif text-3xl text-ink">
            {isNew ? "New activity" : form.watch("title_en") || "Edit activity"}
          </h1>
        </div>
        {item ? <Badge tone="cobalt">{item.publication_status}</Badge> : null}
      </div>

      {serverError ? (
        <p
          role="alert"
          className="mt-4 rounded-lg border border-red-300 bg-red-50 p-3 text-sm text-red-800"
        >
          {serverError}
        </p>
      ) : null}

      <form className="mt-6 space-y-8" onSubmit={(event) => event.preventDefault()}>
        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">General</h2>
          <Field label="Slug" htmlFor="slug" error={form.formState.errors.slug?.message}>
            <Input id="slug" disabled={!isNew} {...form.register("slug")} />
          </Field>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field
              label="Title (English)"
              htmlFor="title_en"
              error={form.formState.errors.title_en?.message}
            >
              <Input id="title_en" {...form.register("title_en")} />
            </Field>
            <Field label="Title (Italian)" htmlFor="title_it">
              <Input id="title_it" {...form.register("title_it")} />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Description (English)" htmlFor="description_en">
              <Textarea id="description_en" rows={3} {...form.register("description_en")} />
            </Field>
            <Field label="Description (Italian)" htmlFor="description_it">
              <Textarea id="description_it" rows={3} {...form.register("description_it")} />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Activity date" htmlFor="activity_date">
              <Input id="activity_date" type="date" {...form.register("activity_date")} />
            </Field>
            <Field
              label="Activity type"
              htmlFor="activity_type"
              error={form.formState.errors.activity_type?.message}
            >
              <Input
                id="activity_type"
                placeholder="meetup, workshop, conference, ..."
                {...form.register("activity_type")}
              />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Presentation</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="URL" htmlFor="url" error={form.formState.errors.url?.message}>
              <Input id="url" {...form.register("url")} />
            </Field>
            <Field label="Logo media URL" htmlFor="logo_media_url">
              <Input id="logo_media_url" {...form.register("logo_media_url")} />
            </Field>
          </div>
          <label className="flex items-center gap-3 text-sm text-ink-soft">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-ink/30"
              {...form.register("is_featured")}
            />
            Featured
          </label>
          <Field label="Display order" htmlFor="sort_order">
            <Input id="sort_order" type="number" {...form.register("sort_order")} />
          </Field>
          <Field label="Internal notes (never shown publicly)" htmlFor="internal_notes">
            <Textarea id="internal_notes" rows={3} {...form.register("internal_notes")} />
          </Field>
        </Card>

        <div className="flex flex-wrap items-center gap-3 border-t border-ink/10 pt-6">
          <LinkButton to="/admin/community" variant="secondary">
            Back to list
          </LinkButton>
          {!isNew && item ? (
            <LinkButton to={`/admin/community/${item.id}/preview`} variant="secondary">
              Preview
            </LinkButton>
          ) : null}
          <Button
            variant="secondary"
            onClick={() => void onSaveDraft()}
            disabled={form.formState.isSubmitting}
          >
            Save draft
          </Button>
          {item?.publication_status !== "PUBLISHED" ? (
            <Button onClick={() => void onPublish()}>Publish</Button>
          ) : (
            <Button
              variant="secondary"
              onClick={() => void unpublishMutation.mutateAsync(undefined)}
            >
              Unpublish
            </Button>
          )}
          {!isNew && item ? (
            <>
              <Button
                variant="secondary"
                onClick={() => void archiveMutation.mutateAsync(undefined)}
              >
                Archive
              </Button>
              {item.deleted_at ? (
                <Button
                  variant="secondary"
                  onClick={() => void restoreMutation.mutateAsync(undefined)}
                >
                  Restore from trash
                </Button>
              ) : (
                <ConfirmDialog
                  trigger={<Button variant="danger">Move to trash</Button>}
                  title="Move this activity to trash?"
                  description="It will disappear from the public site immediately. You can restore it from the trash at any time."
                  confirmLabel="Move to trash"
                  onConfirm={() => void trashMutation.mutateAsync(undefined)}
                />
              )}
              {item.deleted_at ? (
                <ConfirmDialog
                  trigger={<Button variant="danger">Delete permanently</Button>}
                  title="Permanently delete this activity?"
                  description="This cannot be undone."
                  confirmLabel="Delete permanently"
                  onConfirm={async () => {
                    await deleteMutation.mutateAsync(item.id);
                    navigate("/admin/community");
                  }}
                />
              ) : null}
            </>
          ) : null}
        </div>

        {!isNew && item ? (
          <div className="flex flex-wrap items-center gap-3 border-t border-ink/10 pt-6">
            <label htmlFor="schedule-date" className="eyebrow">
              Schedule publication for
            </label>
            <Input
              id="schedule-date"
              type="datetime-local"
              className="max-w-xs"
              onChange={(changeEvent) => {
                const value = changeEvent.target.value;
                if (value) void scheduleMutation.mutateAsync(new Date(value).toISOString());
              }}
            />
          </div>
        ) : null}
      </form>

      {!isNew && revisions && revisions.length > 0 ? (
        <Card className="mt-8">
          <h2 className="font-serif text-lg text-ink">Revision history</h2>
          <ul className="mt-4 space-y-3">
            {revisions.map((revision) => (
              <li
                key={revision.id}
                className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-ink/10 p-3 text-sm"
              >
                <span className="text-ink-soft">
                  {new Date(revision.created_at).toLocaleString()}
                  {revision.created_by_email ? ` — ${revision.created_by_email}` : ""}
                </span>
                <ConfirmDialog
                  trigger={<Button variant="secondary">Restore</Button>}
                  title="Restore this revision?"
                  description="The current content will be saved as a new revision first, so this can always be undone."
                  confirmLabel="Restore"
                  variant="primary"
                  onConfirm={() => void restoreRevisionMutation.mutateAsync(revision.id)}
                />
              </li>
            ))}
          </ul>
        </Card>
      ) : null}
    </div>
  );
}
