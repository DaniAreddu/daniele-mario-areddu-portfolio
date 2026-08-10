import { z } from "zod";

export const REQUEST_TYPES = [
  "speaking_invitation",
  "workshop",
  "engineering_collaboration",
  "community_partnership",
  "podcast_interview",
  "other",
] as const;

export function buildContactSchema(t: (key: string) => string) {
  return z.object({
    name: z.string().min(2, t("contact.form.validation.nameMin")),
    email: z.string().email(t("contact.form.validation.emailInvalid")),
    organization: z.string().max(200).optional().or(z.literal("")),
    request_type: z.enum(REQUEST_TYPES, { message: t("contact.form.validation.required") }),
    event_or_project: z.string().max(200).optional().or(z.literal("")),
    indicative_date: z.string().max(80).optional().or(z.literal("")),
    message: z.string().min(10, t("contact.form.validation.messageMin")),
    consent_given: z.boolean().refine((value) => value === true, {
      message: t("contact.form.validation.consentRequired"),
    }),
    // Honeypot: real users never see or fill this. Kept optional/empty.
    website: z.string().max(0).optional().or(z.literal("")),
  });
}

export type ContactFormValues = z.infer<ReturnType<typeof buildContactSchema>>;
