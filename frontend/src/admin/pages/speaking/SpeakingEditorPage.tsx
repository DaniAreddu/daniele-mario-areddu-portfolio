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
import { Select } from "@/admin/components/ui/Select";
import { Textarea } from "@/admin/components/ui/Textarea";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminEvent,
  useAdminEventRevisions,
  useArchiveEvent,
  useCheckDuplicates,
  useCreateEvent,
  usePermanentlyDeleteEvent,
  useRestoreEvent,
  useRestoreRevision,
  useScheduleEvent,
  useTrashEvent,
  useUnpublishEvent,
  useUpdateEvent,
} from "@/admin/hooks/useAdminEvents";
import {
  defaultFormValues,
  EVENT_FORMATS,
  EVENT_STATUSES,
  type EventFormValues,
  eventFormSchema,
  eventToFormValues,
  formValuesToPayload,
} from "@/admin/pages/speaking/eventFormSchema";
import type { EventAdminDetail } from "@/admin/types/event";

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

function MapPreview({
  latitude,
  longitude,
}: {
  latitude: number | string | undefined;
  longitude: number | string | undefined;
}) {
  // react-hook-form's `watch()` returns the raw uncontrolled input value for
  // a `type="number"` field, which is a STRING (not a number) unless
  // `valueAsNumber` is set on `register()` — this component must not assume
  // otherwise. `Number.isNaN` only ever returns true for the actual NaN
  // value, not a numeric-looking string, so parsing must happen first.
  const lat = typeof latitude === "number" ? latitude : parseFloat(latitude ?? "");
  const lon = typeof longitude === "number" ? longitude : parseFloat(longitude ?? "");

  if (Number.isNaN(lat) || Number.isNaN(lon)) {
    return (
      <p className="rounded-lg border border-dashed border-ink/15 p-4 text-sm text-ink-faint">
        Add coordinates to preview the location on a map.
      </p>
    );
  }
  // Deliberately not an embedded iframe: the site's CSP has no frame-src
  // allowance for a third-party map host, and loosening a site-wide
  // security header for one admin convenience isn't worth it — a plain
  // link (unaffected by CSP) is simpler and just as useful here.
  const href = `https://www.openstreetmap.org/?mlat=${lat}&mlon=${lon}#map=13/${lat}/${lon}`;
  return (
    <div className="rounded-lg border border-ink/10 bg-paper-warm p-4 text-sm">
      <p className="font-mono text-ink">
        {lat.toFixed(4)}, {lon.toFixed(4)}
      </p>
      <a
        href={href}
        target="_blank"
        rel="noreferrer noopener"
        className="mt-1 inline-block text-cobalt underline"
      >
        Open in OpenStreetMap ↗
      </a>
    </div>
  );
}

export default function SpeakingEditorPage() {
  const params = useParams<{ id: string }>();
  const isNew = params.id === undefined;
  const eventId = isNew ? undefined : Number(params.id);
  const navigate = useNavigate();
  const queryClient = useQueryClient();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);
  const [restoringRevisionId, setRestoringRevisionId] = useState<number | null>(null);

  const { data: event, isLoading } = useAdminEvent(eventId);
  const { data: revisions } = useAdminEventRevisions(eventId);

  const form = useForm<EventFormValues>({
    resolver: zodResolver(eventFormSchema),
    defaultValues: defaultFormValues(),
  });

  useEffect(() => {
    if (event) form.reset(eventToFormValues(event));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [event]);

  const createMutation = useCreateEvent();
  const updateMutation = useUpdateEvent(eventId ?? -1);
  const unpublishMutation = useUnpublishEvent(eventId ?? -1);
  const archiveMutation = useArchiveEvent(eventId ?? -1);
  const trashMutation = useTrashEvent(eventId ?? -1);
  const restoreMutation = useRestoreEvent(eventId ?? -1);
  const scheduleMutation = useScheduleEvent(eventId ?? -1);
  const deleteMutation = usePermanentlyDeleteEvent();
  const restoreRevisionMutation = useRestoreRevision(eventId ?? -1);

  const watchedName = form.watch("event_name");
  const watchedCity = form.watch("city");
  const watchedYear = form.watch("year");
  const { data: duplicates } = useCheckDuplicates(
    watchedName ?? "",
    watchedCity ?? "",
    isNew ? (watchedYear ?? null) : null,
  );

  async function persist(values: EventFormValues): Promise<EventAdminDetail> {
    const payload = formValuesToPayload(values);
    if (isNew) {
      const created = await createMutation.mutateAsync(payload);
      navigate(`/admin/speaking/${created.id}`, { replace: true });
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
      await adminApiFetch(`/events/${saved.id}/publish`, { method: "POST" });
      await queryClient.invalidateQueries({ queryKey: ["admin", "events"] });
      showToast({ title: "Published" });
      navigate(`/admin/speaking/${saved.id}`, { replace: true });
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
          <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Speaking</p>
          <h1 className="mt-2 font-serif text-3xl text-ink">
            {isNew ? "New appearance" : form.watch("event_name") || "Edit appearance"}
          </h1>
        </div>
        {event ? <Badge tone="cobalt">{event.publication_status}</Badge> : null}
      </div>

      {serverError ? (
        <p
          role="alert"
          className="mt-4 rounded-lg border border-red-300 bg-red-50 p-3 text-sm text-red-800"
        >
          {serverError}
        </p>
      ) : null}

      {duplicates && duplicates.length > 0 ? (
        <div
          role="alert"
          className="mt-4 rounded-lg border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900"
        >
          <p className="font-medium">Possible duplicate found.</p>
          <ul className="mt-1 list-inside list-disc">
            {duplicates.map((candidate) => (
              <li key={candidate.slug}>
                {candidate.event_name}
                {candidate.city ? ` — ${candidate.city}` : ""} ({candidate.year})
              </li>
            ))}
          </ul>
        </div>
      ) : null}

      <form className="mt-6 space-y-8" onSubmit={(event_) => event_.preventDefault()}>
        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">General</h2>
          <Field label="Slug" htmlFor="slug" error={form.formState.errors.slug?.message}>
            <Input id="slug" disabled={!isNew} {...form.register("slug")} />
          </Field>
          <Field
            label="Event name"
            htmlFor="event_name"
            error={form.formState.errors.event_name?.message}
          >
            <Input id="event_name" {...form.register("event_name")} />
          </Field>
          <Field label="Session title" htmlFor="session_title">
            <Input id="session_title" {...form.register("session_title")} />
          </Field>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Format" htmlFor="format">
              <Select id="format" {...form.register("format")}>
                {EVENT_FORMATS.map((format) => (
                  <option key={format} value={format}>
                    {format.replace("_", " ")}
                  </option>
                ))}
              </Select>
            </Field>
            <Field label="Language" htmlFor="language">
              <Select id="language" {...form.register("language")}>
                <option value="en">English</option>
                <option value="it">Italian</option>
              </Select>
            </Field>
          </div>
          <Field label="Short description (English)" htmlFor="short_description_en">
            <Textarea
              id="short_description_en"
              rows={2}
              {...form.register("short_description_en")}
            />
          </Field>
          <Field label="Short description (Italian)" htmlFor="short_description_it">
            <Textarea
              id="short_description_it"
              rows={2}
              {...form.register("short_description_it")}
            />
          </Field>
          <Field label="Full description (English)" htmlFor="full_description_en">
            <Textarea
              id="full_description_en"
              rows={4}
              {...form.register("full_description_en")}
            />
          </Field>
          <Field label="Full description (Italian)" htmlFor="full_description_it">
            <Textarea
              id="full_description_it"
              rows={4}
              {...form.register("full_description_it")}
            />
          </Field>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Schedule</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Field label="Year" htmlFor="year" error={form.formState.errors.year?.message}>
              <Input id="year" type="number" {...form.register("year")} />
            </Field>
            <Field label="Month (if known)" htmlFor="month">
              <Input id="month" type="number" min={1} max={12} {...form.register("month")} />
            </Field>
            <Field label="Status" htmlFor="status">
              <Select id="status" {...form.register("status")}>
                {EVENT_STATUSES.map((status) => (
                  <option key={status} value={status}>
                    {status}
                  </option>
                ))}
              </Select>
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Start date (if known)" htmlFor="start_date">
              <Input id="start_date" type="date" {...form.register("start_date")} />
            </Field>
            <Field label="End date (if known)" htmlFor="end_date">
              <Input id="end_date" type="date" {...form.register("end_date")} />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Location</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Field label="City" htmlFor="city">
              <Input id="city" {...form.register("city")} />
            </Field>
            <Field label="Country" htmlFor="country">
              <Input id="country" {...form.register("country")} />
            </Field>
            <Field label="Continent" htmlFor="continent">
              <Input id="continent" {...form.register("continent")} />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field
              label="Latitude"
              htmlFor="latitude"
              error={form.formState.errors.latitude?.message as string | undefined}
            >
              <Input id="latitude" type="number" step="any" {...form.register("latitude")} />
            </Field>
            <Field
              label="Longitude"
              htmlFor="longitude"
              error={form.formState.errors.longitude?.message as string | undefined}
            >
              <Input id="longitude" type="number" step="any" {...form.register("longitude")} />
            </Field>
          </div>
          <Field label="Venue" htmlFor="venue">
            <Input id="venue" {...form.register("venue")} />
          </Field>
          <MapPreview
            latitude={form.watch("latitude") ?? ""}
            longitude={form.watch("longitude") ?? ""}
          />
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Links &amp; tags</h2>
          <Field
            label="Event website"
            htmlFor="event_url"
            error={form.formState.errors.event_url?.message}
          >
            <Input id="event_url" {...form.register("event_url")} />
          </Field>
          <Field label="Slides URL" htmlFor="slides_url">
            <Input id="slides_url" {...form.register("slides_url")} />
          </Field>
          <Field label="Recording URL" htmlFor="recording_url">
            <Input id="recording_url" {...form.register("recording_url")} />
          </Field>
          <Field label="Cover image URL" htmlFor="image">
            <Input id="image" {...form.register("image")} />
          </Field>
          <Field label="Tags (comma-separated)" htmlFor="tags_input">
            <Input
              id="tags_input"
              placeholder="AI, Backend, FastAPI"
              {...form.register("tags_input")}
            />
          </Field>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Presentation</h2>
          <label className="flex items-center gap-3 text-sm text-ink-soft">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-ink/30"
              {...form.register("is_featured")}
            />
            Featured talk
          </label>
          <label className="flex items-center gap-3 text-sm text-ink-soft">
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-ink/30"
              {...form.register("is_international_milestone")}
            />
            International milestone
          </label>
          <Field label="Sessions count" htmlFor="sessions_count">
            <Input
              id="sessions_count"
              type="number"
              min={1}
              {...form.register("sessions_count")}
            />
          </Field>
          <Field label="Internal notes (never shown publicly)" htmlFor="internal_notes">
            <Textarea id="internal_notes" rows={3} {...form.register("internal_notes")} />
          </Field>
        </Card>

        <div className="flex flex-wrap items-center gap-3 border-t border-ink/10 pt-6">
          <LinkButton to="/admin/speaking" variant="secondary">
            Back to list
          </LinkButton>
          {!isNew && event ? (
            <LinkButton to={`/admin/speaking/${event.id}/preview`} variant="secondary">
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
          {event?.publication_status !== "PUBLISHED" ? (
            <Button onClick={() => void onPublish()}>Publish</Button>
          ) : (
            <Button
              variant="secondary"
              onClick={() =>
                eventId !== undefined && void unpublishMutation.mutateAsync(undefined)
              }
            >
              Unpublish
            </Button>
          )}
          {!isNew && event ? (
            <>
              <Button
                variant="secondary"
                onClick={() => void archiveMutation.mutateAsync(undefined)}
              >
                Archive
              </Button>
              {event.deleted_at ? (
                <Button
                  variant="secondary"
                  onClick={() => void restoreMutation.mutateAsync(undefined)}
                >
                  Restore from trash
                </Button>
              ) : (
                <ConfirmDialog
                  trigger={<Button variant="danger">Move to trash</Button>}
                  title="Move this appearance to trash?"
                  description="It will disappear from the public site immediately. You can restore it from the trash at any time."
                  confirmLabel="Move to trash"
                  onConfirm={() => void trashMutation.mutateAsync(undefined)}
                />
              )}
              {event.deleted_at ? (
                <ConfirmDialog
                  trigger={<Button variant="danger">Delete permanently</Button>}
                  title="Permanently delete this appearance?"
                  description="This cannot be undone — the event and its history will be gone for good."
                  confirmLabel="Delete permanently"
                  onConfirm={async () => {
                    await deleteMutation.mutateAsync(event.id);
                    navigate("/admin/speaking");
                  }}
                />
              ) : null}
            </>
          ) : null}
        </div>

        {!isNew && event ? (
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
                  trigger={
                    <Button
                      variant="secondary"
                      onClick={() => setRestoringRevisionId(revision.id)}
                    >
                      Restore
                    </Button>
                  }
                  title="Restore this revision?"
                  description="The current content will be saved as a new revision first, so this can always be undone."
                  confirmLabel="Restore"
                  variant="primary"
                  onConfirm={() => {
                    if (restoringRevisionId !== null) {
                      void restoreRevisionMutation.mutateAsync(restoringRevisionId);
                    }
                  }}
                />
              </li>
            ))}
          </ul>
        </Card>
      ) : null}
    </div>
  );
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
