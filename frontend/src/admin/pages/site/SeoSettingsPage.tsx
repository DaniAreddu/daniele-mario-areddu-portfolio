import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { Input } from "@/admin/components/ui/Input";
import { Textarea } from "@/admin/components/ui/Textarea";
import { useAdminToast } from "@/admin/components/ui/Toast";
import { useAdminSeoSettings, useUpdateSeoSettings } from "@/admin/hooks/useAdminSiteSettings";
import type { SeoSettingsWritePayload } from "@/admin/types/siteAdmin";

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

export default function SeoSettingsPage() {
  const { data: settings, isLoading } = useAdminSeoSettings();
  const updateSettings = useUpdateSeoSettings();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<SeoSettingsWritePayload>({
    defaultValues: {
      site_title: "",
      title_template: "%s — Daniele Mario Areddu",
      default_description: "",
      default_og_image_url: null,
      twitter_card_type: "summary_large_image",
      robots_default: "index,follow",
      canonical_base_url: null,
    },
  });

  useEffect(() => {
    if (settings) {
      form.reset({
        site_title: settings.site_title,
        title_template: settings.title_template,
        default_description: settings.default_description,
        default_og_image_url: settings.default_og_image_url,
        twitter_card_type: settings.twitter_card_type,
        robots_default: settings.robots_default,
        canonical_base_url: settings.canonical_base_url,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [settings]);

  const onSave = form.handleSubmit(async (values) => {
    setServerError(null);
    try {
      await updateSettings.mutateAsync({
        ...values,
        default_og_image_url: values.default_og_image_url || null,
        canonical_base_url: values.canonical_base_url || null,
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
        <h1 className="mt-2 font-serif text-3xl text-ink">SEO settings</h1>
        <p className="mt-2 text-sm text-ink-soft">
          Global defaults. Individual pages can still override these.
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
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Site title" htmlFor="site_title">
              <Input id="site_title" {...form.register("site_title")} />
            </Field>
            <Field label="Title template (%s = page title)" htmlFor="title_template">
              <Input id="title_template" {...form.register("title_template")} />
            </Field>
          </div>
          <Field label="Default description" htmlFor="default_description">
            <Textarea
              id="default_description"
              rows={3}
              {...form.register("default_description")}
            />
          </Field>
          <Field label="Default OG image URL" htmlFor="default_og_image_url">
            <Input id="default_og_image_url" {...form.register("default_og_image_url")} />
          </Field>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Twitter card type" htmlFor="twitter_card_type">
              <Input id="twitter_card_type" {...form.register("twitter_card_type")} />
            </Field>
            <Field label="Default robots directive" htmlFor="robots_default">
              <Input id="robots_default" {...form.register("robots_default")} />
            </Field>
          </div>
          <Field label="Canonical base URL" htmlFor="canonical_base_url">
            <Input id="canonical_base_url" {...form.register("canonical_base_url")} />
          </Field>
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
