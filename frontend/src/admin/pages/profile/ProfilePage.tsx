import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { Input } from "@/admin/components/ui/Input";
import { useAdminToast } from "@/admin/components/ui/Toast";
import { useAdminProfile, useUpdateProfile } from "@/admin/hooks/useAdminProfile";

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

interface ProfileFormValues {
  full_name: string;
  roles_input: string;
  location: string;
  base_country: string;
  availability_en: string;
  availability_it: string;
  tagline_en: string;
  tagline_it: string;
  positioning_statement_en: string;
  positioning_statement_it: string;
  brand_label: string;
  public_email: string;
  github_url: string;
  linkedin_url: string;
  sessionize_url: string;
  talks_count_label: string;
  speaking_years_label: string;
  speaking_regions_label: string;
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

const EMPTY_VALUES: ProfileFormValues = {
  full_name: "",
  roles_input: "",
  location: "",
  base_country: "",
  availability_en: "",
  availability_it: "",
  tagline_en: "",
  tagline_it: "",
  positioning_statement_en: "",
  positioning_statement_it: "",
  brand_label: "",
  public_email: "",
  github_url: "",
  linkedin_url: "",
  sessionize_url: "",
  talks_count_label: "",
  speaking_years_label: "",
  speaking_regions_label: "",
};

export default function ProfilePage() {
  const { data: profile, isLoading } = useAdminProfile();
  const updateProfile = useUpdateProfile();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<ProfileFormValues>({ defaultValues: EMPTY_VALUES });

  useEffect(() => {
    if (profile) {
      form.reset({
        full_name: profile.full_name,
        roles_input: profile.roles.join(", "),
        location: profile.location,
        base_country: profile.base_country,
        availability_en: profile.availability_en,
        availability_it: profile.availability_it,
        tagline_en: profile.tagline_en,
        tagline_it: profile.tagline_it,
        positioning_statement_en: profile.positioning_statement_en,
        positioning_statement_it: profile.positioning_statement_it,
        brand_label: profile.brand_label,
        public_email: profile.public_email,
        github_url: profile.github_url ?? "",
        linkedin_url: profile.linkedin_url ?? "",
        sessionize_url: profile.sessionize_url ?? "",
        talks_count_label: profile.talks_count_label,
        speaking_years_label: profile.speaking_years_label,
        speaking_regions_label: profile.speaking_regions_label,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [profile]);

  const onSave = form.handleSubmit(async (values) => {
    setServerError(null);
    try {
      await updateProfile.mutateAsync({
        full_name: values.full_name,
        roles: values.roles_input
          .split(",")
          .map((role) => role.trim())
          .filter(Boolean),
        location: values.location,
        base_country: values.base_country,
        availability_en: values.availability_en,
        availability_it: values.availability_it,
        tagline_en: values.tagline_en,
        tagline_it: values.tagline_it,
        positioning_statement_en: values.positioning_statement_en,
        positioning_statement_it: values.positioning_statement_it,
        brand_label: values.brand_label,
        public_email: values.public_email,
        github_url: values.github_url || null,
        linkedin_url: values.linkedin_url || null,
        sessionize_url: values.sessionize_url || null,
        talks_count_label: values.talks_count_label,
        speaking_years_label: values.speaking_years_label,
        speaking_regions_label: values.speaking_regions_label,
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
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Profile</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Public profile</h1>
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
          <h2 className="font-serif text-lg text-ink">Identity</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Full name" htmlFor="full_name">
              <Input id="full_name" {...form.register("full_name")} />
            </Field>
            <Field label="Brand label" htmlFor="brand_label">
              <Input id="brand_label" {...form.register("brand_label")} />
            </Field>
          </div>
          <Field label="Roles (comma-separated)" htmlFor="roles_input">
            <Input id="roles_input" {...form.register("roles_input")} />
          </Field>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Location" htmlFor="location">
              <Input id="location" {...form.register("location")} />
            </Field>
            <Field label="Base country" htmlFor="base_country">
              <Input id="base_country" {...form.register("base_country")} />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Availability (English)" htmlFor="availability_en">
              <Input id="availability_en" {...form.register("availability_en")} />
            </Field>
            <Field label="Availability (Italian)" htmlFor="availability_it">
              <Input id="availability_it" {...form.register("availability_it")} />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Positioning</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Tagline (English)" htmlFor="tagline_en">
              <Input id="tagline_en" {...form.register("tagline_en")} />
            </Field>
            <Field label="Tagline (Italian)" htmlFor="tagline_it">
              <Input id="tagline_it" {...form.register("tagline_it")} />
            </Field>
          </div>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <Field label="Positioning statement (English)" htmlFor="positioning_statement_en">
              <Input
                id="positioning_statement_en"
                {...form.register("positioning_statement_en")}
              />
            </Field>
            <Field label="Positioning statement (Italian)" htmlFor="positioning_statement_it">
              <Input
                id="positioning_statement_it"
                {...form.register("positioning_statement_it")}
              />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Contact & links</h2>
          <Field label="Public email" htmlFor="public_email">
            <Input id="public_email" type="email" {...form.register("public_email")} />
          </Field>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Field label="GitHub URL" htmlFor="github_url">
              <Input id="github_url" {...form.register("github_url")} />
            </Field>
            <Field label="LinkedIn URL" htmlFor="linkedin_url">
              <Input id="linkedin_url" {...form.register("linkedin_url")} />
            </Field>
            <Field label="Sessionize URL" htmlFor="sessionize_url">
              <Input id="sessionize_url" {...form.register("sessionize_url")} />
            </Field>
          </div>
        </Card>

        <Card className="space-y-4">
          <h2 className="font-serif text-lg text-ink">Speaking stats labels</h2>
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-3">
            <Field label="Talks count label" htmlFor="talks_count_label">
              <Input id="talks_count_label" {...form.register("talks_count_label")} />
            </Field>
            <Field label="Speaking years label" htmlFor="speaking_years_label">
              <Input id="speaking_years_label" {...form.register("speaking_years_label")} />
            </Field>
            <Field label="Speaking regions label" htmlFor="speaking_regions_label">
              <Input id="speaking_regions_label" {...form.register("speaking_regions_label")} />
            </Field>
          </div>
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
