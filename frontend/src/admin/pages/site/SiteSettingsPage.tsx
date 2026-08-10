import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { Input } from "@/admin/components/ui/Input";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminSiteSettings,
  useUpdateSiteSettings,
} from "@/admin/hooks/useAdminSiteSettings";
import type { SiteSettingsWritePayload } from "@/admin/types/siteAdmin";

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

const TOGGLES = [
  ["maintenance_mode", "Maintenance mode (shows a maintenance notice publicly)"],
  ["show_speaking_map", "Show speaking map"],
  ["show_statistics", "Show statistics"],
  ["show_now_section", 'Show "now" section'],
  ["show_projects", "Show projects section"],
  ["show_community", "Show community section"],
] as const;

export default function SiteSettingsPage() {
  const { data: settings, isLoading } = useAdminSiteSettings();
  const updateSettings = useUpdateSiteSettings();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<SiteSettingsWritePayload>({
    defaultValues: {
      site_name: "",
      public_site_url: null,
      default_timezone: "Europe/Rome",
      default_language: "en",
      maintenance_mode: false,
      show_speaking_map: true,
      show_statistics: true,
      show_now_section: false,
      show_projects: true,
      show_community: true,
      map_default_zoom: 2,
      analytics_id: null,
    },
  });

  useEffect(() => {
    if (settings) {
      form.reset({
        site_name: settings.site_name,
        public_site_url: settings.public_site_url,
        default_timezone: settings.default_timezone,
        default_language: settings.default_language,
        maintenance_mode: settings.maintenance_mode,
        show_speaking_map: settings.show_speaking_map,
        show_statistics: settings.show_statistics,
        show_now_section: settings.show_now_section,
        show_projects: settings.show_projects,
        show_community: settings.show_community,
        map_default_zoom: settings.map_default_zoom,
        analytics_id: settings.analytics_id,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [settings]);

  const onSave = form.handleSubmit(async (values) => {
    setServerError(null);
    try {
      await updateSettings.mutateAsync({
        ...values,
        public_site_url: values.public_site_url || null,
        analytics_id: values.analytics_id || null,
        map_default_zoom: Number(values.map_default_zoom),
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
    <div className="max-w-3xl">
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Site</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Site settings</h1>
        <p className="mt-2 text-sm text-ink-soft">
          A singleton — always live on the public site, no draft state.
        </p>
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
            <Field label="Site name" htmlFor="site_name">
              <Input id="site_name" {...form.register("site_name")} />
            </Field>
            <Field label="Public site URL" htmlFor="public_site_url">
              <Input id="public_site_url" {...form.register("public_site_url")} />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Field label="Default timezone" htmlFor="default_timezone">
              <Input id="default_timezone" {...form.register("default_timezone")} />
            </Field>
            <Field label="Default language" htmlFor="default_language">
              <Input id="default_language" {...form.register("default_language")} />
            </Field>
            <Field label="Map default zoom" htmlFor="map_default_zoom">
              <Input
                id="map_default_zoom"
                type="number"
                {...form.register("map_default_zoom", { valueAsNumber: true })}
              />
            </Field>
          </div>
          <Field label="Analytics ID" htmlFor="analytics_id">
            <Input id="analytics_id" {...form.register("analytics_id")} />
          </Field>
        </Card>

        <Card className="space-y-3">
          <h2 className="font-serif text-lg text-ink">Feature toggles</h2>
          {TOGGLES.map(([field, label]) => (
            <label key={field} className="flex items-center gap-3 text-sm text-ink-soft">
              <input
                type="checkbox"
                className="h-4 w-4 rounded border-ink/30"
                {...form.register(field)}
              />
              {label}
            </label>
          ))}
        </Card>

        <div className="flex items-center gap-3 border-t border-ink/10 pt-6">
          <Button onClick={() => void onSave()} disabled={form.formState.isSubmitting}>
            Save
          </Button>
        </div>
      </form>
    </div>
  );
}
