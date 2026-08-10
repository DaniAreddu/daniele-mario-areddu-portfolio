export interface EventListItem {
  id: number;
  slug: string;
  event_name: string;
  city: string | null;
  country: string | null;
  year: number;
  month: number | null;
  status: string;
  publication_status: "DRAFT" | "SCHEDULED" | "PUBLISHED" | "ARCHIVED";
  is_featured: boolean;
  is_international_milestone: boolean;
  deleted_at: string | null;
}

export interface EventAdminDetail {
  id: number;
  slug: string;
  event_name: string;
  talk_id: number | null;
  session_title: string | null;
  short_description_en: string | null;
  short_description_it: string | null;
  full_description_en: string | null;
  full_description_it: string | null;
  start_date: string | null;
  end_date: string | null;
  year: number;
  month: number | null;
  city: string | null;
  country: string | null;
  continent: string | null;
  latitude: number | null;
  longitude: number | null;
  venue: string | null;
  format: string;
  language: string;
  event_url: string | null;
  slides_url: string | null;
  recording_url: string | null;
  image: string | null;
  status: string;
  sessions_count: number;
  is_featured: boolean;
  is_international_milestone: boolean;
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

export type EventWritePayload = Omit<
  EventAdminDetail,
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

export type EventCreatePayload = Omit<EventWritePayload, "slug"> & { slug: string };
export type EventUpdatePayload = EventWritePayload;

export interface DuplicateCandidate {
  slug: string;
  event_name: string;
  city: string | null;
  year: number;
}

export interface RevisionSummary {
  id: number;
  schema_version: number;
  snapshot: Record<string, unknown>;
  created_at: string;
  created_by_email: string | null;
}

export interface RevisionDiff {
  current: Record<string, unknown>;
  snapshot: Record<string, unknown>;
}

export interface TagSummary {
  slug: string;
  label: string;
}
