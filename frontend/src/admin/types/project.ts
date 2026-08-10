export interface AdminProjectListItem {
  id: number;
  slug: string;
  title_en: string;
  is_featured: boolean;
  sort_order: number;
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  deleted_at: string | null;
}

export interface ProjectAdminDetail {
  id: number;
  slug: string;
  title_en: string;
  title_it: string;
  summary_en: string;
  summary_it: string;
  problem_en: string;
  problem_it: string;
  challenge_en: string;
  challenge_it: string;
  approach_en: string;
  approach_it: string;
  architecture_en: string;
  architecture_it: string;
  key_decisions_en: string[];
  key_decisions_it: string[];
  outcome_en: string;
  outcome_it: string;
  lessons_en: string;
  lessons_it: string;
  confidentiality_note_en: string;
  confidentiality_note_it: string;
  external_url: string | null;
  is_featured: boolean;
  sort_order: number;
  internal_notes: string | null;
  tags: string[];
  related_skills: string[];
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  publish_at: string | null;
  unpublish_at: string | null;
  published_at: string | null;
  deleted_at: string | null;
  created_at: string;
  updated_at: string;
}

export type ProjectWritePayload = Omit<
  ProjectAdminDetail,
  | "id"
  | "slug"
  | "tags"
  | "related_skills"
  | "publication_status"
  | "publish_at"
  | "unpublish_at"
  | "published_at"
  | "deleted_at"
  | "created_at"
  | "updated_at"
> & { tag_labels: string[] };

export type ProjectCreatePayload = ProjectWritePayload & { slug: string };

export interface ProjectRevisionSummary {
  id: number;
  schema_version: number;
  snapshot: Record<string, unknown>;
  created_at: string;
  created_by_email: string | null;
}
