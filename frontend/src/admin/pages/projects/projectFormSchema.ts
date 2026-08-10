import { z } from "zod";

import type { ProjectAdminDetail, ProjectWritePayload } from "@/admin/types/project";

const optionalUrl = z
  .string()
  .refine((value) => !value || /^https?:\/\//.test(value), {
    message: "Must start with http:// or https://",
  })
  .optional()
  .or(z.literal(""));

export const projectFormSchema = z.object({
  slug: z
    .string()
    .min(1, "Slug is required.")
    .regex(/^[a-z0-9]+(?:-[a-z0-9]+)*$/, "Use lowercase letters, numbers, and hyphens only."),
  title_en: z.string().min(1, "Title is required."),
  title_it: z.string().optional().or(z.literal("")),
  summary_en: z.string().optional().or(z.literal("")),
  summary_it: z.string().optional().or(z.literal("")),
  problem_en: z.string().optional().or(z.literal("")),
  problem_it: z.string().optional().or(z.literal("")),
  challenge_en: z.string().optional().or(z.literal("")),
  challenge_it: z.string().optional().or(z.literal("")),
  approach_en: z.string().optional().or(z.literal("")),
  approach_it: z.string().optional().or(z.literal("")),
  architecture_en: z.string().optional().or(z.literal("")),
  architecture_it: z.string().optional().or(z.literal("")),
  key_decisions_en_input: z.string().optional().or(z.literal("")),
  key_decisions_it_input: z.string().optional().or(z.literal("")),
  outcome_en: z.string().optional().or(z.literal("")),
  outcome_it: z.string().optional().or(z.literal("")),
  lessons_en: z.string().optional().or(z.literal("")),
  lessons_it: z.string().optional().or(z.literal("")),
  confidentiality_note_en: z.string().optional().or(z.literal("")),
  confidentiality_note_it: z.string().optional().or(z.literal("")),
  external_url: optionalUrl,
  is_featured: z.boolean(),
  sort_order: z.coerce.number().int(),
  internal_notes: z.string().optional().or(z.literal("")),
  tags_input: z.string().optional().or(z.literal("")),
});

export type ProjectFormValues = z.infer<typeof projectFormSchema>;

function linesToList(value: string | undefined): string[] {
  return (value ?? "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

export function defaultProjectFormValues(): ProjectFormValues {
  return {
    slug: "",
    title_en: "",
    title_it: "",
    summary_en: "",
    summary_it: "",
    problem_en: "",
    problem_it: "",
    challenge_en: "",
    challenge_it: "",
    approach_en: "",
    approach_it: "",
    architecture_en: "",
    architecture_it: "",
    key_decisions_en_input: "",
    key_decisions_it_input: "",
    outcome_en: "",
    outcome_it: "",
    lessons_en: "",
    lessons_it: "",
    confidentiality_note_en: "",
    confidentiality_note_it: "",
    external_url: "",
    is_featured: false,
    sort_order: 0,
    internal_notes: "",
    tags_input: "",
  };
}

export function projectToFormValues(project: ProjectAdminDetail): ProjectFormValues {
  return {
    slug: project.slug,
    title_en: project.title_en,
    title_it: project.title_it,
    summary_en: project.summary_en,
    summary_it: project.summary_it,
    problem_en: project.problem_en,
    problem_it: project.problem_it,
    challenge_en: project.challenge_en,
    challenge_it: project.challenge_it,
    approach_en: project.approach_en,
    approach_it: project.approach_it,
    architecture_en: project.architecture_en,
    architecture_it: project.architecture_it,
    key_decisions_en_input: project.key_decisions_en.join("\n"),
    key_decisions_it_input: project.key_decisions_it.join("\n"),
    outcome_en: project.outcome_en,
    outcome_it: project.outcome_it,
    lessons_en: project.lessons_en,
    lessons_it: project.lessons_it,
    confidentiality_note_en: project.confidentiality_note_en,
    confidentiality_note_it: project.confidentiality_note_it,
    external_url: project.external_url ?? "",
    is_featured: project.is_featured,
    sort_order: project.sort_order,
    internal_notes: project.internal_notes ?? "",
    tags_input: project.tags.join(", "),
  };
}

export function projectFormValuesToPayload(values: ProjectFormValues): ProjectWritePayload {
  return {
    title_en: values.title_en,
    title_it: values.title_it || "",
    summary_en: values.summary_en || "",
    summary_it: values.summary_it || "",
    problem_en: values.problem_en || "",
    problem_it: values.problem_it || "",
    challenge_en: values.challenge_en || "",
    challenge_it: values.challenge_it || "",
    approach_en: values.approach_en || "",
    approach_it: values.approach_it || "",
    architecture_en: values.architecture_en || "",
    architecture_it: values.architecture_it || "",
    key_decisions_en: linesToList(values.key_decisions_en_input),
    key_decisions_it: linesToList(values.key_decisions_it_input),
    outcome_en: values.outcome_en || "",
    outcome_it: values.outcome_it || "",
    lessons_en: values.lessons_en || "",
    lessons_it: values.lessons_it || "",
    confidentiality_note_en: values.confidentiality_note_en || "",
    confidentiality_note_it: values.confidentiality_note_it || "",
    external_url: values.external_url || null,
    is_featured: values.is_featured,
    sort_order: values.sort_order,
    internal_notes: values.internal_notes || null,
    tag_labels: (values.tags_input ?? "")
      .split(",")
      .map((label) => label.trim())
      .filter(Boolean),
  };
}
