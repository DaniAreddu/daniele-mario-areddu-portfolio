import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { Textarea } from "@/admin/components/ui/Textarea";
import { useAdminToast } from "@/admin/components/ui/Toast";
import { useAdminBiography, useUpdateBiography } from "@/admin/hooks/useAdminProfile";
import type { BiographyWritePayload } from "@/admin/types/profile";

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

const FIELD_PAIRS = [
  ["micro_en", "micro_it", "Micro bio (one sentence)"],
  ["short_en", "short_it", "Short bio"],
  ["medium_en", "medium_it", "Medium bio"],
  ["long_en", "long_it", "Long bio"],
  ["speaker_bio_en", "speaker_bio_it", "Speaker bio"],
] as const;

export default function BiographyPage() {
  const { data: biography, isLoading } = useAdminBiography();
  const updateBiography = useUpdateBiography();
  const { showToast } = useAdminToast();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<BiographyWritePayload>({
    defaultValues: {
      micro_en: "",
      micro_it: "",
      short_en: "",
      short_it: "",
      medium_en: "",
      medium_it: "",
      long_en: "",
      long_it: "",
      speaker_bio_en: "",
      speaker_bio_it: "",
    },
  });

  useEffect(() => {
    if (biography) {
      form.reset({
        micro_en: biography.micro_en,
        micro_it: biography.micro_it,
        short_en: biography.short_en,
        short_it: biography.short_it,
        medium_en: biography.medium_en,
        medium_it: biography.medium_it,
        long_en: biography.long_en,
        long_it: biography.long_it,
        speaker_bio_en: biography.speaker_bio_en,
        speaker_bio_it: biography.speaker_bio_it,
      });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [biography]);

  const onSave = form.handleSubmit(async (values) => {
    setServerError(null);
    try {
      await updateBiography.mutateAsync(values);
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
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Biography</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Biography</h1>
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
          {FIELD_PAIRS.map(([enField, itField, label]) => (
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
