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
  useAdminProject,
  useAdminProjectRevisions,
  useArchiveProject,
  useCreateProject,
  usePermanentlyDeleteProject,
  useRestoreProject,
  useRestoreProjectRevision,
  useTrashProject,
  useUnpublishProject,
  useUpdateProject,
} from "@/admin/hooks/useAdminProjects";
import {
  defaultProjectFormValues,
  type ProjectFormValues,
  projectFormSchema,
  projectFormValuesToPayload,
  projectToFormValues,
} from "@/admin/pages/projects/projectFormSchema";
import type { ProjectAdminDetail } from "@/admin/types/project";

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

export default function ProjectsEditorPage() {
  const params = useParams<{ id: string }>();
  const isNew = params.id === undefined;
  const projectId = isNew ? undefined : Number(params.id);
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);

  const { data: project, isLoading } = useAdminProject(projectId);
  const { data: revisions } = useAdminProjectRevisions(projectId);

  const form = useForm<ProjectFormValues>({
    resolver: zodResolver(projectFormSchema),
    defaultValues: defaultProjectFormValues(),
  });

  useEffect(() => {
    if (project) form.reset(projectToFormValues(project));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [project]);

  const createMutation = useCreateProject();
  const updateMutation = useUpdateProject(projectId ?? -1);
  const unpublishMutation = useUnpublishProject(projectId ?? -1);
  const archiveMutation = useArchiveProject(projectId ?? -1);
  const trashMutation = useTrashProject(projectId ?? -1);
  const restoreMutation = useRestoreProject(projectId ?? -1);
  const deleteMutation = usePermanentlyDeleteProject();
  const restoreRevisionMutation = useRestoreProjectRevision(projectId ?? -1);

  async function persist(values: ProjectFormValues): Promise<ProjectAdminDetail> {
    const payload = projectFormValuesToPayload(values);
    if (isNew) {
      const created = await createMutation.mutateAsync({ ...payload, slug: values.slug });
      navigate(`/admin/projects/${created.id}`, { replace: true });
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
      await adminApiFetch(`/projects/${saved.id}/publish`, { method: "POST" });
      await queryClient.invalidateQueries({ queryKey: ["admin", "projects"] });
      showToast({ title: "Published" });
      navigate(`/admin/projects/${saved.id}`, { replace: true });
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
          <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Projects</p>
          <h1 className="mt-2 font-serif text-3xl text-ink">
            {isNew ? "New project" : form.watch("title_en") || "Edit project"}
          </h1>
        </div>
        {project ? <Badge tone="cobalt">{project.publication_status}</Badge> : null}
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
            <Field label="Summary (English)" htmlFor="summary_en">
              <Textarea id="summary_en" rows={2} {...form.register("summary_en")} />
            </Field>
            <Field label="Summary (Italian)" htmlFor="summary_it">
              <Textarea id="summary_it" rows={2} {...form.register("summary_it")} />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Case study</h2>
          {(
            [
              ["problem_en", "problem_it", "Problem"],
              ["challenge_en", "challenge_it", "Challenge"],
              ["approach_en", "approach_it", "Approach"],
              ["architecture_en", "architecture_it", "Architecture"],
              ["outcome_en", "outcome_it", "Outcome"],
              ["lessons_en", "lessons_it", "Lessons learned"],
            ] as const
          ).map(([enField, itField, label]) => (
            <div key={enField} className="grid grid-cols-1 gap-4 sm:grid-cols-2">
              <Field label={`${label} (English)`} htmlFor={enField}>
                <Textarea id={enField} rows={3} {...form.register(enField)} />
              </Field>
              <Field label={`${label} (Italian)`} htmlFor={itField}>
                <Textarea id={itField} rows={3} {...form.register(itField)} />
              </Field>
            </div>
          ))}
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field
              label="Key decisions — English (one per line)"
              htmlFor="key_decisions_en_input"
            >
              <Textarea
                id="key_decisions_en_input"
                rows={4}
                {...form.register("key_decisions_en_input")}
              />
            </Field>
            <Field
              label="Key decisions — Italian (one per line)"
              htmlFor="key_decisions_it_input"
            >
              <Textarea
                id="key_decisions_it_input"
                rows={4}
                {...form.register("key_decisions_it_input")}
              />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Confidentiality note (English)" htmlFor="confidentiality_note_en">
              <Textarea
                id="confidentiality_note_en"
                rows={2}
                {...form.register("confidentiality_note_en")}
              />
            </Field>
            <Field label="Confidentiality note (Italian)" htmlFor="confidentiality_note_it">
              <Textarea
                id="confidentiality_note_it"
                rows={2}
                {...form.register("confidentiality_note_it")}
              />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Presentation</h2>
          <Field
            label="External URL"
            htmlFor="external_url"
            error={form.formState.errors.external_url?.message}
          >
            <Input id="external_url" {...form.register("external_url")} />
          </Field>
          <Field label="Technologies / tags (comma-separated)" htmlFor="tags_input">
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
          <LinkButton to="/admin/projects" variant="secondary">
            Back to list
          </LinkButton>
          {!isNew && project ? (
            <LinkButton to={`/admin/projects/${project.id}/preview`} variant="secondary">
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
          {project?.publication_status !== "PUBLISHED" ? (
            <Button onClick={() => void onPublish()}>Publish</Button>
          ) : (
            <Button
              variant="secondary"
              onClick={() => void unpublishMutation.mutateAsync(undefined)}
            >
              Unpublish
            </Button>
          )}
          {!isNew && project ? (
            <>
              <Button
                variant="secondary"
                onClick={() => void archiveMutation.mutateAsync(undefined)}
              >
                Archive
              </Button>
              {project.deleted_at ? (
                <Button
                  variant="secondary"
                  onClick={() => void restoreMutation.mutateAsync(undefined)}
                >
                  Restore from trash
                </Button>
              ) : (
                <ConfirmDialog
                  trigger={<Button variant="danger">Move to trash</Button>}
                  title="Move this project to trash?"
                  description="It will disappear from the public site immediately. You can restore it from the trash at any time."
                  confirmLabel="Move to trash"
                  onConfirm={() => void trashMutation.mutateAsync(undefined)}
                />
              )}
              {project.deleted_at ? (
                <ConfirmDialog
                  trigger={<Button variant="danger">Delete permanently</Button>}
                  title="Permanently delete this project?"
                  description="This cannot be undone."
                  confirmLabel="Delete permanently"
                  onConfirm={async () => {
                    await deleteMutation.mutateAsync(project.id);
                    navigate("/admin/projects");
                  }}
                />
              ) : null}
            </>
          ) : null}
        </div>
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
