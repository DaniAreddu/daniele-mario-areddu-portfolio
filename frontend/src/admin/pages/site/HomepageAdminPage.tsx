import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { ConfirmDialog } from "@/admin/components/ui/ConfirmDialog";
import { Input } from "@/admin/components/ui/Input";
import { Select } from "@/admin/components/ui/Select";
import { Textarea } from "@/admin/components/ui/Textarea";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminHomepageFeatures,
  useAdminHomepageSettings,
  useCreateHomepageFeature,
  useDeleteHomepageFeature,
  useUpdateHomepageSettings,
} from "@/admin/hooks/useAdminHomepage";
import type { HomepageSettingsWritePayload } from "@/admin/types/siteAdmin";

const KNOWN_SECTIONS = ["about", "journey", "speaking", "projects", "community"] as const;

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

function Field({
  label,
  htmlFor,
  children,
}: {
  label: string;
  htmlFor: string;
  children: React.ReactNode;
}) {
  return (
    <div>
      <label htmlFor={htmlFor} className="eyebrow">
        {label}
      </label>
      <div className="mt-2">{children}</div>
    </div>
  );
}

function HomepageSettingsForm() {
  const { data: settings, isLoading } = useAdminHomepageSettings();
  const updateSettings = useUpdateHomepageSettings();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);
  const [visibility, setVisibility] = useState<Record<string, boolean>>({});

  const form = useForm<HomepageSettingsWritePayload>({
    defaultValues: {
      hero_eyebrow_en: "",
      hero_eyebrow_it: "",
      hero_headline_en: "",
      hero_headline_it: "",
      hero_subheadline_en: "",
      hero_subheadline_it: "",
      primary_cta_label_en: null,
      primary_cta_label_it: null,
      primary_cta_url: null,
      secondary_cta_label_en: null,
      secondary_cta_label_it: null,
      secondary_cta_url: null,
      section_order: [],
      section_visibility: {},
    },
  });

  useEffect(() => {
    if (settings) {
      form.reset(settings);
      setVisibility(settings.section_visibility);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [settings]);

  const onSave = form.handleSubmit(async (values) => {
    setServerError(null);
    try {
      await updateSettings.mutateAsync({
        ...values,
        primary_cta_label_en: values.primary_cta_label_en || null,
        primary_cta_label_it: values.primary_cta_label_it || null,
        primary_cta_url: values.primary_cta_url || null,
        secondary_cta_label_en: values.secondary_cta_label_en || null,
        secondary_cta_label_it: values.secondary_cta_label_it || null,
        secondary_cta_url: values.secondary_cta_url || null,
        section_visibility: visibility,
      });
      showToast({ title: "Saved" });
    } catch (error) {
      setServerError(describeError(error));
    }
  });

  if (isLoading) {
    return <p className="text-sm text-ink-faint">Loading…</p>;
  }

  return (
    <form className="space-y-8" onSubmit={(event) => event.preventDefault()}>
      {serverError ? (
        <p
          role="alert"
          className="rounded-lg border border-red-300 bg-red-50 p-3 text-sm text-red-800"
        >
          {serverError}
        </p>
      ) : null}

      <Card className="space-y-4">
        <h2 className="font-serif text-lg text-ink">Hero</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="Eyebrow (English)" htmlFor="hero_eyebrow_en">
            <Input id="hero_eyebrow_en" {...form.register("hero_eyebrow_en")} />
          </Field>
          <Field label="Eyebrow (Italian)" htmlFor="hero_eyebrow_it">
            <Input id="hero_eyebrow_it" {...form.register("hero_eyebrow_it")} />
          </Field>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="Headline (English)" htmlFor="hero_headline_en">
            <Textarea id="hero_headline_en" rows={2} {...form.register("hero_headline_en")} />
          </Field>
          <Field label="Headline (Italian)" htmlFor="hero_headline_it">
            <Textarea id="hero_headline_it" rows={2} {...form.register("hero_headline_it")} />
          </Field>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <Field label="Subheadline (English)" htmlFor="hero_subheadline_en">
            <Textarea
              id="hero_subheadline_en"
              rows={2}
              {...form.register("hero_subheadline_en")}
            />
          </Field>
          <Field label="Subheadline (Italian)" htmlFor="hero_subheadline_it">
            <Textarea
              id="hero_subheadline_it"
              rows={2}
              {...form.register("hero_subheadline_it")}
            />
          </Field>
        </div>
      </Card>

      <Card className="space-y-4">
        <h2 className="font-serif text-lg text-ink">Calls to action</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Field label="Primary label (English)" htmlFor="primary_cta_label_en">
            <Input id="primary_cta_label_en" {...form.register("primary_cta_label_en")} />
          </Field>
          <Field label="Primary label (Italian)" htmlFor="primary_cta_label_it">
            <Input id="primary_cta_label_it" {...form.register("primary_cta_label_it")} />
          </Field>
          <Field label="Primary URL" htmlFor="primary_cta_url">
            <Input id="primary_cta_url" {...form.register("primary_cta_url")} />
          </Field>
        </div>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
          <Field label="Secondary label (English)" htmlFor="secondary_cta_label_en">
            <Input id="secondary_cta_label_en" {...form.register("secondary_cta_label_en")} />
          </Field>
          <Field label="Secondary label (Italian)" htmlFor="secondary_cta_label_it">
            <Input id="secondary_cta_label_it" {...form.register("secondary_cta_label_it")} />
          </Field>
          <Field label="Secondary URL" htmlFor="secondary_cta_url">
            <Input id="secondary_cta_url" {...form.register("secondary_cta_url")} />
          </Field>
        </div>
      </Card>

      <Card className="space-y-3">
        <h2 className="font-serif text-lg text-ink">Section visibility</h2>
        {KNOWN_SECTIONS.map((section) => (
          <label
            key={section}
            className="flex items-center gap-3 text-sm capitalize text-ink-soft"
          >
            <input
              type="checkbox"
              className="h-4 w-4 rounded border-ink/30"
              checked={visibility[section] ?? true}
              onChange={(e) => setVisibility({ ...visibility, [section]: e.target.checked })}
            />
            {section}
          </label>
        ))}
      </Card>

      <div className="flex items-center gap-3">
        <Button onClick={() => void onSave()} disabled={form.formState.isSubmitting}>
          Save
        </Button>
      </div>
    </form>
  );
}

function FeaturesEditor() {
  const { data: features, isLoading } = useAdminHomepageFeatures();
  const createFeature = useCreateHomepageFeature();
  const deleteFeature = useDeleteHomepageFeature();
  const { showToast } = useAdminToast();
  const [entityType, setEntityType] = useState<"project" | "event">("project");
  const [entityId, setEntityId] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function handleAdd() {
    const id = Number(entityId);
    if (!id) return;
    setError(null);
    try {
      await createFeature.mutateAsync({
        entity_type: entityType,
        entity_id: id,
        sort_order: 0,
      });
      setEntityId("");
      showToast({ title: "Featured" });
    } catch (addError) {
      setError(describeError(addError));
    }
  }

  return (
    <Card className="mt-8 space-y-4">
      <h2 className="font-serif text-lg text-ink">Featured items</h2>
      <p className="text-sm text-ink-soft">
        Pin published projects or speaking appearances to the homepage, by numeric id (see each
        item's admin list/edit page URL).
      </p>
      {error ? (
        <p role="alert" className="text-sm text-red-700">
          {error}
        </p>
      ) : null}
      <div className="flex flex-wrap items-end gap-3">
        <Select
          value={entityType}
          onChange={(e) => setEntityType(e.target.value as "project" | "event")}
          aria-label="Entity type"
          className="max-w-[10rem]"
        >
          <option value="project">Project</option>
          <option value="event">Event</option>
        </Select>
        <Input
          value={entityId}
          onChange={(e) => setEntityId(e.target.value)}
          placeholder="Entity id"
          aria-label="Entity id"
          className="max-w-[10rem]"
        />
        <Button onClick={() => void handleAdd()} disabled={createFeature.isPending}>
          Feature it
        </Button>
      </div>

      {isLoading ? (
        <p className="text-sm text-ink-faint">Loading…</p>
      ) : features && features.length > 0 ? (
        <ul className="space-y-2">
          {features.map((feature) => (
            <li
              key={feature.id}
              className="flex items-center justify-between rounded-lg border border-ink/10 p-3 text-sm"
            >
              <span>
                {feature.entity_type} #{feature.entity_id}
              </span>
              <ConfirmDialog
                trigger={
                  <Button variant="danger" className="px-3 py-1 text-xs">
                    Remove
                  </Button>
                }
                title="Remove this featured item?"
                description="It will no longer appear on the homepage."
                confirmLabel="Remove"
                onConfirm={() => void deleteFeature.mutateAsync(feature.id)}
              />
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-ink-faint">Nothing featured yet.</p>
      )}
    </Card>
  );
}

export default function HomepageAdminPage() {
  return (
    <div className="max-w-3xl">
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Site</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Homepage</h1>
        <p className="mt-2 text-sm text-ink-soft">
          A singleton — always live on the public site, no draft state.
        </p>
      </div>
      <div className="mt-6">
        <HomepageSettingsForm />
      </div>
      <FeaturesEditor />
    </div>
  );
}
