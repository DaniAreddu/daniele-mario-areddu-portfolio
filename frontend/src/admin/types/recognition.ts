export type RecognitionKind = "certification" | "award" | "recognition" | "publication";

export interface RecognitionListItem {
  id: number;
  kind: string;
  title_en: string;
  sort_order: number;
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  deleted_at: string | null;
}

export interface RecognitionAdminDetail {
  id: number;
  kind: string;
  title_en: string;
  title_it: string;
  issuer: string | null;
  description_en: string | null;
  description_it: string | null;
  date_awarded: string | null;
  url: string | null;
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

export type RecognitionWritePayload = Omit<
  RecognitionAdminDetail,
  | "id"
  | "publication_status"
  | "publish_at"
  | "unpublish_at"
  | "published_at"
  | "deleted_at"
  | "created_at"
  | "updated_at"
>;

export interface RecognitionRevisionSummary {
  id: number;
  schema_version: number;
  snapshot: Record<string, unknown>;
  created_at: string;
  created_by_email: string | null;
}
