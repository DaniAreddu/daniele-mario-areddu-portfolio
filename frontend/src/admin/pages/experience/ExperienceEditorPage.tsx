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
  useAdminExperienceItem,
  useAdminExperienceRevisions,
  useArchiveExperience,
  useCreateExperience,
  usePermanentlyDeleteExperience,
  useRestoreExperience,
  useRestoreExperienceRevision,
  useScheduleExperience,
  useTrashExperience,
  useUnpublishExperience,
  useUpdateExperience,
} from "@/admin/hooks/useAdminExperience";
import {
  defaultExperienceFormValues,
  experienceFormSchema,
  experienceFormValuesToPayload,
  experienceToFormValues,
  type ExperienceFormValues,
} from "@/admin/pages/experience/experienceFormSchema";
import type { ExperienceAdminDetail } from "@/admin/types/experience";

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

export default function ExperienceEditorPage() {
  const params = useParams<{ id: string }>();
  const isNew = params.id === undefined;
  const itemId = isNew ? undefined : Number(params.id);
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);

  const { data: item, isLoading } = useAdminExperienceItem(itemId);
  const { data: revisions } = useAdminExperienceRevisions(itemId);

  const form = useForm<ExperienceFormValues>({
    resolver: zodResolver(experienceFormSchema),
    defaultValues: defaultExperienceFormValues(),
  });

  useEffect(() => {
    if (item) form.reset(experienceToFormValues(item));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [item]);

  const createMutation = useCreateExperience();
  const updateMutation = useUpdateExperience(itemId ?? -1);
  const scheduleMutation = useScheduleExperience(itemId ?? -1);
  const unpublishMutation = useUnpublishExperience(itemId ?? -1);
  const archiveMutation = useArchiveExperience(itemId ?? -1);
  const trashMutation = useTrashExperience(itemId ?? -1);
  const restoreMutation = useRestoreExperience(itemId ?? -1);
  const deleteMutation = usePermanentlyDeleteExperience();
  const restoreRevisionMutation = useRestoreExperienceRevision(itemId ?? -1);

  async function persist(values: ExperienceFormValues): Promise<ExperienceAdminDetail> {
    const payload = experienceFormValuesToPayload(values);
    if (isNew) {
      const created = await createMutation.mutateAsync(payload);
      navigate(`/admin/experience/${created.id}`, { replace: true });
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
      await adminApiFetch(`/experience/${saved.id}/publish`, { method: "POST" });
      await queryClient.invalidateQueries({ queryKey: ["admin", "experience"] });
      showToast({ title: "Published" });
      navigate(`/admin/experience/${saved.id}`, { replace: true });
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
          <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Experience</p>
          <h1 className="mt-2 font-serif text-3xl text-ink">
            {isNew ? "New experience" : form.watch("organization") || "Edit experience"}
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
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field
              label="Organization"
              htmlFor="organization"
              error={form.formState.errors.organization?.message}
            >
              <Input id="organization" {...form.register("organization")} />
            </Field>
            <Field label="Location" htmlFor="location">
              <Input id="location" {...form.register("location")} />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field
              label="Role (English)"
              htmlFor="role_en"
              error={form.formState.errors.role_en?.message}
            >
              <Input id="role_en" {...form.register("role_en")} />
            </Field>
            <Field label="Role (Italian)" htmlFor="role_it">
              <Input id="role_it" {...form.register("role_it")} />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Employment type" htmlFor="employment_type">
              <Input
                id="employment_type"
                placeholder="full-time, contract, ..."
                {...form.register("employment_type")}
              />
            </Field>
            <Field label="Location mode" htmlFor="location_mode">
              <Input
                id="location_mode"
                placeholder="remote, hybrid, on-site"
                {...form.register("location_mode")}
              />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Field
              label="Start date"
              htmlFor="start_date"
              error={form.formState.errors.start_date?.message}
            >
              <Input id="start_date" type="date" {...form.register("start_date")} />
            </Field>
            <Field label="End date" htmlFor="end_date">
              <Input id="end_date" type="date" {...form.register("end_date")} />
            </Field>
            <div className="flex items-end pb-2">
              <label className="flex items-center gap-3 text-sm text-ink-soft">
                <input
                  type="checkbox"
                  className="h-4 w-4 rounded border-ink/30"
                  {...form.register("is_current")}
                />
                Current position
              </label>
            </div>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Summary (English)" htmlFor="summary_en">
              <Textarea id="summary_en" rows={2} {...form.register("summary_en")} />
            </Field>
            <Field label="Summary (Italian)" htmlFor="summary_it">
              <Textarea id="summary_it" rows={2} {...form.register("summary_it")} />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Detail</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Long description (English)" htmlFor="long_description_en">
              <Textarea
                id="long_description_en"
                rows={4}
                {...form.register("long_description_en")}
              />
            </Field>
            <Field label="Long description (Italian)" htmlFor="long_description_it">
              <Textarea
                id="long_description_it"
                rows={4}
                {...form.register("long_description_it")}
              />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Highlights — English (one per line)" htmlFor="highlights_en_input">
              <Textarea
                id="highlights_en_input"
                rows={4}
                {...form.register("highlights_en_input")}
              />
            </Field>
            <Field label="Highlights — Italian (one per line)" htmlFor="highlights_it_input">
              <Textarea
                id="highlights_it_input"
                rows={4}
                {...form.register("highlights_it_input")}
              />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field
              label="Achievements — English (one per line)"
              htmlFor="achievements_en_input"
            >
              <Textarea
                id="achievements_en_input"
                rows={4}
                {...form.register("achievements_en_input")}
              />
            </Field>
            <Field
              label="Achievements — Italian (one per line)"
              htmlFor="achievements_it_input"
            >
              <Textarea
                id="achievements_it_input"
                rows={4}
                {...form.register("achievements_it_input")}
              />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Presentation</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field
              label="Company URL"
              htmlFor="company_url"
              error={form.formState.errors.company_url?.message}
            >
              <Input id="company_url" {...form.register("company_url")} />
            </Field>
            <Field label="Logo media URL" htmlFor="logo_media_url">
              <Input id="logo_media_url" {...form.register("logo_media_url")} />
            </Field>
          </div>
          <Field label="Tags (comma-separated)" htmlFor="tags_input">
            <Input
              id="tags_input"
              placeholder="Python, FastAPI, PostgreSQL"
              {...form.register("tags_input")}
            />
          </Field>
          <label className="flex items-center gap-3 text-sm text-ink-soft">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-ink/30"
              {...form.register("is_featured")}
            />
            Featured on homepage
          </label>
          <Field label="Display order" htmlFor="sort_order">
            <Input id="sort_order" type="number" {...form.register("sort_order")} />
          </Field>
          <Field label="Internal notes (never shown publicly)" htmlFor="internal_notes">
            <Textarea id="internal_notes" rows={3} {...form.register("internal_notes")} />
          </Field>
        </Card>

        <div className="flex flex-wrap items-center gap-3 border-t border-ink/10 pt-6">
          <LinkButton to="/admin/experience" variant="secondary">
            Back to list
          </LinkButton>
          {!isNew && item ? (
            <LinkButton to={`/admin/experience/${item.id}/preview`} variant="secondary">
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
                  title="Move this entry to trash?"
                  description="It will disappear from the public site immediately. You can restore it from the trash at any time."
                  confirmLabel="Move to trash"
                  onConfirm={() => void trashMutation.mutateAsync(undefined)}
                />
              )}
              {item.deleted_at ? (
                <ConfirmDialog
                  trigger={<Button variant="danger">Delete permanently</Button>}
                  title="Permanently delete this entry?"
                  description="This cannot be undone."
                  confirmLabel="Delete permanently"
                  onConfirm={async () => {
                    await deleteMutation.mutateAsync(item.id);
                    navigate("/admin/experience");
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
