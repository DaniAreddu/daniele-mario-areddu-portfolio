import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { Input } from "@/admin/components/ui/Input";
import { LinkButton } from "@/admin/components/ui/LinkButton";
import { Textarea } from "@/admin/components/ui/Textarea";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminCommunityProfile,
  useUpdateCommunityProfile,
} from "@/admin/hooks/useAdminCommunity";
import type { CommunityProfileWritePayload } from "@/admin/types/community";

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

export default function CommunityProfilePage() {
  const { data: profile, isLoading } = useAdminCommunityProfile();
  const updateProfile = useUpdateCommunityProfile();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<CommunityProfileWritePayload>({
    defaultValues: {
      name: "Velletri.dev",
      role_en: "",
      role_it: "",
      mission_en: "",
      mission_it: "",
      description_en: "",
      description_it: "",
      vision_en: "",
      vision_it: "",
      collaboration_en: "",
      collaboration_it: "",
      founded_year: 2023,
      website_url: null,
    },
  });

  useEffect(() => {
    if (profile) {
      form.reset({
        name: profile.name,
        role_en: profile.role_en,
        role_it: profile.role_it,
        mission_en: profile.mission_en,
        mission_it: profile.mission_it,
        description_en: profile.description_en,
        description_it: profile.description_it,
        vision_en: profile.vision_en,
        vision_it: profile.vision_it,
        collaboration_en: profile.collaboration_en,
        collaboration_it: profile.collaboration_it,
        founded_year: profile.founded_year,
        website_url: profile.website_url,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profile]);

  const onSave = form.handleSubmit(async (values) => {
    setServerError(null);
    try {
      await updateProfile.mutateAsync({
        ...values,
        website_url: values.website_url || null,
        founded_year: Number(values.founded_year),
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
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Community</p>
          <h1 className="mt-2 font-serif text-3xl text-ink">Community profile</h1>
          <p className="mt-2 text-sm text-ink-soft">
            A singleton — always live on the public site, no draft state.
          </p>
        </div>
        <LinkButton to="/admin/community" variant="secondary">
          Back to activities
        </LinkButton>
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
          <h2 className="font-serif text-lg text-ink">Identity</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Name" htmlFor="name">
              <Input id="name" {...form.register("name")} />
            </Field>
            <Field label="Founded year" htmlFor="founded_year">
              <Input
                id="founded_year"
                type="number"
                {...form.register("founded_year", { valueAsNumber: true })}
              />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Role (English)" htmlFor="role_en">
              <Input id="role_en" {...form.register("role_en")} />
            </Field>
            <Field label="Role (Italian)" htmlFor="role_it">
              <Input id="role_it" {...form.register("role_it")} />
            </Field>
          </div>
          <Field label="Website URL" htmlFor="website_url">
            <Input id="website_url" {...form.register("website_url")} />
          </Field>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Narrative</h2>
          {(
            [
              ["mission_en", "mission_it", "Mission"],
              ["description_en", "description_it", "Description"],
              ["vision_en", "vision_it", "Vision"],
              ["collaboration_en", "collaboration_it", "Collaboration"],
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
