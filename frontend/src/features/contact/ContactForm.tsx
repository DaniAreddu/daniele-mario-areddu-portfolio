import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation } from "@tanstack/react-query";
import { useMemo } from "react";
import { useForm } from "react-hook-form";
import { useTranslation } from "react-i18next";

import {
  buildContactSchema,
  REQUEST_TYPES,
  type ContactFormValues,
} from "@/features/contact/contactSchema";
import { apiFetch, ApiError } from "@/services/apiClient";
import type { ContactResult } from "@/types/api";

const DEFAULT_VALUES: ContactFormValues = {
  name: "",
  email: "",
  organization: "",
  request_type: "speaking_invitation",
  event_or_project: "",
  indicative_date: "",
  message: "",
  consent_given: false,
  website: "",
};

export function ContactForm() {
  const { t } = useTranslation();
  const schema = useMemo(() => buildContactSchema(t), [t]);

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<ContactFormValues>({
    resolver: zodResolver(schema),
    defaultValues: DEFAULT_VALUES,
  });

  const mutation = useMutation({
    mutationFn: (values: ContactFormValues) =>
      apiFetch<ContactResult>("/contact", { method: "POST", body: values }),
  });

  const onSubmit = handleSubmit((values) => {
    // Reset the field values so the form is clean if the user navigates back
    // to it, but keep relying on `mutation.isSuccess` (not RHF's own
    // `isSubmitSuccessful`, which `reset()` immediately clears) to decide
    // whether to show the success screen below.
    mutation.mutate(values, { onSuccess: () => reset(DEFAULT_VALUES) });
  });

  if (mutation.isSuccess) {
    return (
      <div
        role="status"
        className="rounded-2xl border border-ink/10 bg-paper-warm p-8 text-center"
      >
        <p className="font-serif text-2xl text-ink">{t("contact.form.successTitle")}</p>
        <p className="mt-2 text-ink-soft">
          {mutation.data?.email_delivered
            ? t("contact.form.successBody")
            : t("contact.form.successUndeliveredBody")}
        </p>
      </div>
    );
  }

  const isRateLimited = mutation.error instanceof ApiError && mutation.error.status === 429;

  return (
    <form onSubmit={onSubmit} noValidate className="space-y-6">
      {mutation.isError ? (
        <div
          role="alert"
          className="rounded-xl border border-red-300 bg-red-50 p-4 text-sm text-red-800"
        >
          <p className="font-medium">{t("contact.form.errorTitle")}</p>
          <p>
            {isRateLimited ? t("contact.form.rateLimitedBody") : t("contact.form.errorBody")}
          </p>
        </div>
      ) : null}

      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
        <div>
          <label htmlFor="name" className="eyebrow">
            {t("contact.form.name")}
          </label>
          <input
            id="name"
            type="text"
            autoComplete="name"
            aria-invalid={Boolean(errors.name)}
            aria-describedby={errors.name ? "name-error" : undefined}
            className="mt-2 w-full rounded-xl border border-ink/15 bg-paper px-4 py-3"
            {...register("name")}
          />
          {errors.name ? (
            <p id="name-error" role="alert" className="mt-1 text-sm text-red-700">
              {errors.name.message}
            </p>
          ) : null}
        </div>

        <div>
          <label htmlFor="email" className="eyebrow">
            {t("contact.form.email")}
          </label>
          <input
            id="email"
            type="email"
            autoComplete="email"
            aria-invalid={Boolean(errors.email)}
            aria-describedby={errors.email ? "email-error" : undefined}
            className="mt-2 w-full rounded-xl border border-ink/15 bg-paper px-4 py-3"
            {...register("email")}
          />
          {errors.email ? (
            <p id="email-error" role="alert" className="mt-1 text-sm text-red-700">
              {errors.email.message}
            </p>
          ) : null}
        </div>

        <div>
          <label htmlFor="organization" className="eyebrow">
            {t("contact.form.organization")}
          </label>
          <input
            id="organization"
            type="text"
            autoComplete="organization"
            className="mt-2 w-full rounded-xl border border-ink/15 bg-paper px-4 py-3"
            {...register("organization")}
          />
        </div>

        <div>
          <label htmlFor="request_type" className="eyebrow">
            {t("contact.form.requestType")}
          </label>
          <select
            id="request_type"
            className="mt-2 w-full rounded-xl border border-ink/15 bg-paper px-4 py-3"
            {...register("request_type")}
          >
            {REQUEST_TYPES.map((type) => (
              <option key={type} value={type}>
                {t(`contact.form.requestTypes.${type}`)}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="event_or_project" className="eyebrow">
            {t("contact.form.eventOrProject")}
          </label>
          <input
            id="event_or_project"
            type="text"
            className="mt-2 w-full rounded-xl border border-ink/15 bg-paper px-4 py-3"
            {...register("event_or_project")}
          />
        </div>

        <div>
          <label htmlFor="indicative_date" className="eyebrow">
            {t("contact.form.indicativeDate")}
          </label>
          <input
            id="indicative_date"
            type="text"
            className="mt-2 w-full rounded-xl border border-ink/15 bg-paper px-4 py-3"
            {...register("indicative_date")}
          />
        </div>
      </div>

      <div>
        <label htmlFor="message" className="eyebrow">
          {t("contact.form.message")}
        </label>
        <textarea
          id="message"
          rows={5}
          aria-invalid={Boolean(errors.message)}
          aria-describedby={errors.message ? "message-error" : undefined}
          className="mt-2 w-full rounded-xl border border-ink/15 bg-paper px-4 py-3"
          {...register("message")}
        />
        {errors.message ? (
          <p id="message-error" role="alert" className="mt-1 text-sm text-red-700">
            {errors.message.message}
          </p>
        ) : null}
      </div>

      {/* Honeypot field: visually hidden, but present for real browsers/screen
          readers to skip via aria-hidden + tabIndex, so only bots fill it. */}
      <div
        aria-hidden="true"
        className="absolute -left-[9999px] top-auto h-0 w-0 overflow-hidden"
      >
        <label htmlFor="website">Website</label>
        <input
          id="website"
          type="text"
          tabIndex={-1}
          autoComplete="off"
          {...register("website")}
        />
      </div>

      <div className="flex items-start gap-3">
        <input
          id="consent_given"
          type="checkbox"
          aria-invalid={Boolean(errors.consent_given)}
          aria-describedby={errors.consent_given ? "consent-error" : undefined}
          className="mt-1 h-4 w-4 rounded border-ink/30"
          {...register("consent_given")}
        />
        <label htmlFor="consent_given" className="text-sm text-ink-soft">
          {t("contact.form.consent")}
        </label>
      </div>
      {errors.consent_given ? (
        <p id="consent-error" role="alert" className="text-sm text-red-700">
          {errors.consent_given.message}
        </p>
      ) : null}

      <button type="submit" className="btn-primary" disabled={mutation.isPending}>
        {mutation.isPending ? t("contact.form.submitting") : t("contact.form.submit")}
      </button>
    </form>
  );
}
