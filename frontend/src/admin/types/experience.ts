export interface ExperienceListItem {
  id: number;
  organization: string;
  role_en: string;
  is_current: boolean;
  sort_order: number;
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  deleted_at: string | null;
}

export interface ExperienceAdminDetail {
  id: number;
  organization: string;
  role_en: string;
  role_it: string;
  employment_type: string | null;
  location: string;
  location_mode: string | null;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  summary_en: string;
  summary_it: string;
  long_description_en: string | null;
  long_description_it: string | null;
  highlights_en: string[];
  highlights_it: string[];
  achievements_en: string[];
  achievements_it: string[];
  company_url: string | null;
  logo_media_url: string | null;
  is_featured: boolean;
  sort_order: number;
  internal_notes: string | null;
  tags: string[];
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  publish_at: string | null;
  unpublish_at: string | null;
  published_at: string | null;
  deleted_at: string | null;
  created_at: string;
  updated_at: string;
}

export type ExperienceWritePayload = Omit<
  ExperienceAdminDetail,
  | "id"
  | "tags"
  | "publication_status"
  | "publish_at"
  | "unpublish_at"
  | "published_at"
  | "deleted_at"
  | "created_at"
  | "updated_at"
> & { tag_labels: string[] };

export interface ExperienceRevisionSummary {
  id: number;
  schema_version: number;
  snapshot: Record<string, unknown>;
  created_at: string;
  created_by_email: string | null;
}
