import { z } from "zod";

import type {
  CommunityActivityAdminDetail,
  CommunityActivityWritePayload,
} from "@/admin/types/community";

const optionalUrl = z
  .string()
  .refine((value) => !value || /^https?:\/\//.test(value), {
    message: "Must start with http:// or https://",
  })
  .optional()
  .or(z.literal(""));

export const activityFormSchema = z.object({
  slug: z
    .string()
    .min(1, "Slug is required.")
    .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "Use lowercase letters, numbers, and hyphens only."),
  title_en: z.string().min(1, "Title is required."),
  title_it: z.string().optional().or(z.literal("")),
  description_en: z.string().optional().or(z.literal("")),
  description_it: z.string().optional().or(z.literal("")),
  activity_date: z.string().optional().or(z.literal("")),
  activity_type: z.string().min(1, "Activity type is required."),
  url: optionalUrl,
  logo_media_url: z.string().optional().or(z.literal("")),
  is_featured: z.boolean(),
  sort_order: z.coerce.number().int(),
  internal_notes: z.string().optional().or(z.literal("")),
});

export type ActivityFormValues = z.infer<typeof activityFormSchema>;

export function defaultActivityFormValues(): ActivityFormValues {
  return {
    slug: "",
    title_en: "",
    title_it: "",
    description_en: "",
    description_it: "",
    activity_date: "",
    activity_type: "meetup",
    url: "",
    logo_media_url: "",
    is_featured: false,
    sort_order: 0,
    internal_notes: "",
  };
}

export function activityToFormValues(item: CommunityActivityAdminDetail): ActivityFormValues {
  return {
    slug: item.slug,
    title_en: item.title_en,
    title_it: item.title_it,
    description_en: item.description_en,
    description_it: item.description_it,
    activity_date: item.activity_date ?? "",
    activity_type: item.activity_type,
    url: item.url ?? "",
    logo_media_url: item.logo_media_url ?? "",
    is_featured: item.is_featured,
    sort_order: item.sort_order,
    internal_notes: item.internal_notes ?? "",
  };
}

export function activityFormValuesToPayload(
  values: ActivityFormValues,
): CommunityActivityWritePayload {
  return {
    slug: values.slug,
    title_en: values.title_en,
    title_it: values.title_it || "",
    description_en: values.description_en || "",
    description_it: values.description_it || "",
    activity_date: values.activity_date || null,
    activity_type: values.activity_type,
    url: values.url || null,
    logo_media_url: values.logo_media_url || null,
    is_featured: values.is_featured,
    sort_order: values.sort_order,
    internal_notes: values.internal_notes || null,
  };
}
