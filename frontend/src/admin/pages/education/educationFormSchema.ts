import { z } from "zod";

import type { EducationAdminDetail, EducationWritePayload } from "@/admin/types/education";

const optionalUrl = z
  .string()
  .refine((value) => !value || /^https?:\/\//.test(value), {
    message: "Must start with http:// or https://",
  })
  .optional()
  .or(z.literal(""));

export const educationFormSchema = z.object({
  institution: z.string().min(1, "Institution is required."),
  degree_en: z.string().min(1, "Degree is required."),
  degree_it: z.string().optional().or(z.literal("")),
  field: z.string().optional().or(z.literal("")),
  location: z.string().optional().or(z.literal("")),
  start_year: z
    .string()
    .refine((value) => !value || /^\d{4}$/.test(value), { message: "Use a 4-digit year." })
    .optional()
    .or(z.literal("")),
  end_year: z
    .string()
    .refine((value) => !value || /^\d{4}$/.test(value), { message: "Use a 4-digit year." })
    .optional()
    .or(z.literal("")),
  is_ongoing: z.boolean(),
  description_en: z.string().optional().or(z.literal("")),
  description_it: z.string().optional().or(z.literal("")),
  activities_input: z.string().optional().or(z.literal("")),
  url: optionalUrl,
  logo_media_url: z.string().optional().or(z.literal("")),
  sort_order: z.coerce.number().int(),
  internal_notes: z.string().optional().or(z.literal("")),
});

export type EducationFormValues = z.infer<typeof educationFormSchema>;

function linesToList(value: string | undefined): string[] {
  return (value ?? "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

export function defaultEducationFormValues(): EducationFormValues {
  return {
    institution: "",
    degree_en: "",
    degree_it: "",
    field: "",
    location: "",
    start_year: "",
    end_year: "",
    is_ongoing: false,
    description_en: "",
    description_it: "",
    activities_input: "",
    url: "",
    logo_media_url: "",
    sort_order: 0,
    internal_notes: "",
  };
}

export function educationToFormValues(item: EducationAdminDetail): EducationFormValues {
  return {
    institution: item.institution,
    degree_en: item.degree_en,
    degree_it: item.degree_it,
    field: item.field ?? "",
    location: item.location,
    start_year: item.start_year === null ? "" : String(item.start_year),
    end_year: item.end_year === null ? "" : String(item.end_year),
    is_ongoing: item.is_ongoing,
    description_en: item.description_en ?? "",
    description_it: item.description_it ?? "",
    activities_input: item.activities.join("\n"),
    url: item.url ?? "",
    logo_media_url: item.logo_media_url ?? "",
    sort_order: item.sort_order,
    internal_notes: item.internal_notes ?? "",
  };
}

export function educationFormValuesToPayload(
  values: EducationFormValues,
): EducationWritePayload {
  return {
    institution: values.institution,
    degree_en: values.degree_en,
    degree_it: values.degree_it || "",
    field: values.field || null,
    location: values.location || "",
    start_year: values.start_year ? Number(values.start_year) : null,
    end_year: values.end_year ? Number(values.end_year) : null,
    is_ongoing: values.is_ongoing,
    description_en: values.description_en || null,
    description_it: values.description_it || null,
    activities: linesToList(values.activities_input),
    url: values.url || null,
    logo_media_url: values.logo_media_url || null,
    sort_order: values.sort_order,
    internal_notes: values.internal_notes || null,
  };
}
