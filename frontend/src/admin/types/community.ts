export interface CommunityActivityListItem {
  id: number;
  slug: string;
  title_en: string;
  activity_type: string;
  sort_order: number;
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  deleted_at: string | null;
}

export interface CommunityActivityAdminDetail {
  id: number;
  slug: string;
  title_en: string;
  title_it: string;
  description_en: string;
  description_it: string;
  activity_date: string | null;
  activity_type: string;
  url: string | null;
  logo_media_url: string | null;
  is_featured: boolean;
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

export type CommunityActivityWritePayload = Omit<
  CommunityActivityAdminDetail,
  | "id"
  | "publication_status"
  | "publish_at"
  | "unpublish_at"
  | "published_at"
  | "deleted_at"
  | "created_at"
  | "updated_at"
>;

export interface CommunityActivityRevisionSummary {
  id: number;
  schema_version: number;
  snapshot: Record<string, unknown>;
  created_at: string;
  created_by_email: string | null;
}

export interface CommunityProfileAdmin {
  id: number;
  name: string;
  role_en: string;
  role_it: string;
  mission_en: string;
  mission_it: string;
  description_en: string;
  description_it: string;
  vision_en: string;
  vision_it: string;
  collaboration_en: string;
  collaboration_it: string;
  founded_year: number;
  website_url: string | null;
  created_at: string;
  updated_at: string;
}

export type CommunityProfileWritePayload = Omit<
  CommunityProfileAdmin,
  "id" | "created_at" | "updated_at"
>;
