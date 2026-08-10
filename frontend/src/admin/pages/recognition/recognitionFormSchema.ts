import { z } from "zod";

import type {
  RecognitionAdminDetail,
  RecognitionWritePayload,
} from "@/admin/types/recognition";

const optionalUrl = z
  .string()
  .refine((value) => !value || /^https?:\/\//.test(value), {
    message: "Must start with http:// or https://",
  })
  .optional()
  .or(z.literal(""));

export const RECOGNITION_KINDS = [
  "certification",
  "award",
  "recognition",
  "publication",
] as const;

export const recognitionFormSchema = z.object({
  kind: z.enum(RECOGNITION_KINDS),
  title_en: z.string().min(1, "Title is required."),
  title_it: z.string().optional().or(z.literal("")),
  issuer: z.string().optional().or(z.literal("")),
  description_en: z.string().optional().or(z.literal("")),
  description_it: z.string().optional().or(z.literal("")),
  date_awarded: z.string().optional().or(z.literal("")),
  url: optionalUrl,
  sort_order: z.coerce.number().int(),
  internal_notes: z.string().optional().or(z.literal("")),
});

export type RecognitionFormValues = z.infer<typeof recognitionFormSchema>;

export function defaultRecognitionFormValues(): RecognitionFormValues {
  return {
    kind: "certification",
    title_en: "",
    title_it: "",
    issuer: "",
    description_en: "",
    description_it: "",
    date_awarded: "",
    url: "",
    sort_order: 0,
    internal_notes: "",
  };
}

export function recognitionToFormValues(item: RecognitionAdminDetail): RecognitionFormValues {
  return {
    kind: item.kind as RecognitionFormValues["kind"],
    title_en: item.title_en,
    title_it: item.title_it,
    issuer: item.issuer ?? "",
    description_en: item.description_en ?? "",
    description_it: item.description_it ?? "",
    date_awarded: item.date_awarded ?? "",
    url: item.url ?? "",
    sort_order: item.sort_order,
    internal_notes: item.internal_notes ?? "",
  };
}

export function recognitionFormValuesToPayload(
  values: RecognitionFormValues,
): RecognitionWritePayload {
  return {
    kind: values.kind,
    title_en: values.title_en,
    title_it: values.title_it || "",
    issuer: values.issuer || null,
    description_en: values.description_en || null,
    description_it: values.description_it || null,
    date_awarded: values.date_awarded || null,
    url: values.url || null,
    sort_order: values.sort_order,
    internal_notes: values.internal_notes || null,
  };
}
