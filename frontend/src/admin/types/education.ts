export interface EducationListItem {
  id: number;
  institution: string;
  degree_en: string;
  sort_order: number;
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  deleted_at: string | null;
}

export interface EducationAdminDetail {
  id: number;
  institution: string;
  degree_en: string;
  degree_it: string;
  field: string | null;
  location: string;
  start_year: number | null;
  end_year: number | null;
  is_ongoing: boolean;
  description_en: string | null;
  description_it: string | null;
  activities: string[];
  url: string | null;
  logo_media_url: string | null;
  sort_order: number;
  internal_notes: string | null;
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  publish_at: string | null;
  unpublish_at: string | null;
  published_at: string | null;
  deleted_at: string | null;
  created_at: string;
  updated_at: string;
}

export type EducationWritePayload = Omit<
  EducationAdminDetail,
  | "id"
  | "publication_status"
  | "publish_at"
  | "unpublish_at"
  | "published_at"
  | "deleted_at"
  | "created_at"
  | "updated_at"
>;

export interface EducationRevisionSummary {
  id: number;
  schema_version: number;
  snapshot: Record<string, unknown>;
  created_at: string;
  created_by_email: string | null;
}
