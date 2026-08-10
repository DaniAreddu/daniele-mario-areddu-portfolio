import { z } from "zod";

import type { ExperienceAdminDetail, ExperienceWritePayload } from "@/admin/types/experience";

const optionalUrl = z
  .string()
  .refine((value) => !value || /^https?:\/\//.test(value), {
    message: "Must start with http:// or https://",
  })
  .optional()
  .or(z.literal(""));

export const experienceFormSchema = z.object({
  organization: z.string().min(1, "Organization is required."),
  role_en: z.string().min(1, "Role is required."),
  role_it: z.string().optional().or(z.literal("")),
  employment_type: z.string().optional().or(z.literal("")),
  location: z.string().optional().or(z.literal("")),
  location_mode: z.string().optional().or(z.literal("")),
  start_date: z.string().min(1, "Start date is required."),
  end_date: z.string().optional().or(z.literal("")),
  is_current: z.boolean(),
  summary_en: z.string().optional().or(z.literal("")),
  summary_it: z.string().optional().or(z.literal("")),
  long_description_en: z.string().optional().or(z.literal("")),
  long_description_it: z.string().optional().or(z.literal("")),
  highlights_en_input: z.string().optional().or(z.literal("")),
  highlights_it_input: z.string().optional().or(z.literal("")),
  achievements_en_input: z.string().optional().or(z.literal("")),
  achievements_it_input: z.string().optional().or(z.literal("")),
  company_url: optionalUrl,
  logo_media_url: z.string().optional().or(z.literal("")),
  is_featured: z.boolean(),
  sort_order: z.coerce.number().int(),
  internal_notes: z.string().optional().or(z.literal("")),
  tags_input: z.string().optional().or(z.literal("")),
});

export type ExperienceFormValues = z.infer<typeof experienceFormSchema>;

function linesToList(value: string | undefined): string[] {
  return (value ?? "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

export function defaultExperienceFormValues(): ExperienceFormValues {
  return {
    organization: "",
    role_en: "",
    role_it: "",
    employment_type: "",
    location: "",
    location_mode: "",
    start_date: "",
    end_date: "",
    is_current: false,
    summary_en: "",
    summary_it: "",
    long_description_en: "",
    long_description_it: "",
    highlights_en_input: "",
    highlights_it_input: "",
    achievements_en_input: "",
    achievements_it_input: "",
    company_url: "",
    logo_media_url: "",
    is_featured: false,
    sort_order: 0,
    internal_notes: "",
    tags_input: "",
  };
}

export function experienceToFormValues(item: ExperienceAdminDetail): ExperienceFormValues {
  return {
    organization: item.organization,
    role_en: item.role_en,
    role_it: item.role_it,
    employment_type: item.employment_type ?? "",
    location: item.location,
    location_mode: item.location_mode ?? "",
    start_date: item.start_date,
    end_date: item.end_date ?? "",
    is_current: item.is_current,
    summary_en: item.summary_en,
    summary_it: item.summary_it,
    long_description_en: item.long_description_en ?? "",
    long_description_it: item.long_description_it ?? "",
    highlights_en_input: item.highlights_en.join("\n"),
    highlights_it_input: item.highlights_it.join("\n"),
    achievements_en_input: item.achievements_en.join("\n"),
    achievements_it_input: item.achievements_it.join("\n"),
    company_url: item.company_url ?? "",
    logo_media_url: item.logo_media_url ?? "",
    is_featured: item.is_featured,
    sort_order: item.sort_order,
    internal_notes: item.internal_notes ?? "",
    tags_input: item.tags.join(", "),
  };
}

export function experienceFormValuesToPayload(
  values: ExperienceFormValues,
): ExperienceWritePayload {
  return {
    organization: values.organization,
    role_en: values.role_en,
    role_it: values.role_it || "",
    employment_type: values.employment_type || null,
    location: values.location || "",
    location_mode: values.location_mode || null,
    start_date: values.start_date,
    end_date: values.end_date || null,
    is_current: values.is_current,
    summary_en: values.summary_en || "",
    summary_it: values.summary_it || "",
    long_description_en: values.long_description_en || null,
    long_description_it: values.long_description_it || null,
    highlights_en: linesToList(values.highlights_en_input),
    highlights_it: linesToList(values.highlights_it_input),
    achievements_en: linesToList(values.achievements_en_input),
    achievements_it: linesToList(values.achievements_it_input),
    company_url: values.company_url || null,
    logo_media_url: values.logo_media_url || null,
    is_featured: values.is_featured,
    sort_order: values.sort_order,
    internal_notes: values.internal_notes || null,
    tag_labels: (values.tags_input ?? "")
      .split(",")
      .map((label) => label.trim())
      .filter(Boolean),
  };
}
