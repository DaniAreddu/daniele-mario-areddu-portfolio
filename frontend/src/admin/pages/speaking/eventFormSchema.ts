import { z } from "zod";

import type { EventAdminDetail, EventWritePayload } from "@/admin/types/event";

const optionalUrl = z
  .string()
  .refine((value) => !value || /^https?:\/\//.test(value), {
    message: "Must start with http:// or https://",
  })
  .optional()
  .or(z.literal(""));

// `z.coerce.number()` turns "" into 0 (JS: Number("") === 0), not NaN — so
// an empty-string branch placed AFTER it in a union never gets a chance to
// match. Checking the literal first is required, not stylistic, for every
// optional numeric field backed by a text/number input that starts empty.
function optionalNumber(numberSchema: z.ZodTypeAny) {
  return z.union([z.literal(""), numberSchema]);
}

export const eventFormSchema = z.object({
  slug: z
    .string()
    .min(1, "Slug is required.")
    .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "Use lowercase letters, numbers, and hyphens only."),
  event_name: z.string().min(1, "Event name is required."),
  session_title: z.string().optional().or(z.literal("")),
  short_description_en: z.string().optional().or(z.literal("")),
  short_description_it: z.string().optional().or(z.literal("")),
  full_description_en: z.string().optional().or(z.literal("")),
  full_description_it: z.string().optional().or(z.literal("")),
  format: z.string().min(1),
  language: z.string().min(1),
  year: z.coerce.number().int().min(2000).max(2100),
  month: optionalNumber(z.coerce.number().int().min(1).max(12)).optional(),
  start_date: z.string().optional().or(z.literal("")),
  end_date: z.string().optional().or(z.literal("")),
  status: z.string().min(1),
  city: z.string().optional().or(z.literal("")),
  country: z.string().optional().or(z.literal("")),
  continent: z.string().optional().or(z.literal("")),
  latitude: optionalNumber(z.coerce.number().min(-90).max(90)).optional(),
  longitude: optionalNumber(z.coerce.number().min(-180).max(180)).optional(),
  venue: z.string().optional().or(z.literal("")),
  event_url: optionalUrl,
  slides_url: optionalUrl,
  recording_url: optionalUrl,
  image: optionalUrl,
  talk_id: optionalNumber(z.coerce.number().int()).optional(),
  tags_input: z.string().optional().or(z.literal("")),
  sessions_count: z.coerce.number().int().min(1),
  is_featured: z.boolean(),
  is_international_milestone: z.boolean(),
  internal_notes: z.string().optional().or(z.literal("")),
});

export type EventFormValues = z.infer<typeof eventFormSchema>;

export const EVENT_FORMATS = [
  "conference",
  "devfest",
  "meetup",
  "user_group",
  "lightning_talk",
  "community",
] as const;

export const EVENT_STATUSES = [
  "confirmed",
  "upcoming",
  "incoming",
  "completed",
  "cancelled",
] as const;

export function defaultFormValues(): EventFormValues {
  return {
    slug: "",
    event_name: "",
    session_title: "",
    short_description_en: "",
    short_description_it: "",
    full_description_en: "",
    full_description_it: "",
    format: "conference",
    language: "en",
    year: new Date().getUTCFullYear(),
    month: "",
    start_date: "",
    end_date: "",
    status: "confirmed",
    city: "",
    country: "",
    continent: "",
    latitude: "",
    longitude: "",
    venue: "",
    event_url: "",
    slides_url: "",
    recording_url: "",
    image: "",
    talk_id: "",
    tags_input: "",
    sessions_count: 1,
    is_featured: false,
    is_international_milestone: false,
    internal_notes: "",
  };
}

export function eventToFormValues(event: EventAdminDetail): EventFormValues {
  return {
    slug: event.slug,
    event_name: event.event_name,
    session_title: event.session_title ?? "",
    short_description_en: event.short_description_en ?? "",
    short_description_it: event.short_description_it ?? "",
    full_description_en: event.full_description_en ?? "",
    full_description_it: event.full_description_it ?? "",
    format: event.format,
    language: event.language,
    year: event.year,
    month: event.month ?? "",
    start_date: event.start_date ?? "",
    end_date: event.end_date ?? "",
    status: event.status,
    city: event.city ?? "",
    country: event.country ?? "",
    continent: event.continent ?? "",
    latitude: event.latitude ?? "",
    longitude: event.longitude ?? "",
    venue: event.venue ?? "",
    event_url: event.event_url ?? "",
    slides_url: event.slides_url ?? "",
    recording_url: event.recording_url ?? "",
    image: event.image ?? "",
    talk_id: event.talk_id ?? "",
    tags_input: event.tags.join(", "),
    sessions_count: event.sessions_count,
    is_featured: event.is_featured,
    is_international_milestone: event.is_international_milestone,
    internal_notes: event.internal_notes ?? "",
  };
}

function emptyToNull(value: string | undefined): string | null {
  return value && value.trim() !== "" ? value : null;
}

export function formValuesToPayload(values: EventFormValues): EventWritePayload {
  return {
    slug: values.slug,
    event_name: values.event_name,
    talk_id: values.talk_id === "" || values.talk_id === undefined ? null : values.talk_id,
    session_title: emptyToNull(values.session_title),
    short_description_en: emptyToNull(values.short_description_en),
    short_description_it: emptyToNull(values.short_description_it),
    full_description_en: emptyToNull(values.full_description_en),
    full_description_it: emptyToNull(values.full_description_it),
    start_date: emptyToNull(values.start_date),
    end_date: emptyToNull(values.end_date),
    year: values.year,
    month: values.month === "" || values.month === undefined ? null : values.month,
    city: emptyToNull(values.city),
    country: emptyToNull(values.country),
    continent: emptyToNull(values.continent),
    latitude: values.latitude === "" || values.latitude === undefined ? null : values.latitude,
    longitude:
      values.longitude === "" || values.longitude === undefined ? null : values.longitude,
    venue: emptyToNull(values.venue),
    format: values.format,
    language: values.language,
    event_url: emptyToNull(values.event_url),
    slides_url: emptyToNull(values.slides_url),
    recording_url: emptyToNull(values.recording_url),
    image: emptyToNull(values.image),
    status: values.status,
    sessions_count: values.sessions_count,
    is_featured: values.is_featured,
    is_international_milestone: values.is_international_milestone,
    internal_notes: emptyToNull(values.internal_notes),
    tag_labels: (values.tags_input ?? "")
      .split(",")
      .map((label) => label.trim())
      .filter(Boolean),
  };
}
