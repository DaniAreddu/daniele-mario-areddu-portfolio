export interface ContentTypeCounts {
  published: number;
  draft: number;
  scheduled: number;
  archived: number;
  trashed: number;
}

export interface AuditEventEntry {
  id: number;
  actor_email: string | null;
  action: string;
  entity_type: string | null;
  entity_id: number | null;
  summary: string;
  context: Record<string, unknown>;
  created_at: string;
}

export interface DashboardStats {
  events: ContentTypeCounts;
  projects: ContentTypeCounts;
  experience: ContentTypeCounts;
  education: ContentTypeCounts;
  community_activities: ContentTypeCounts;
  recognition: ContentTypeCounts;
  media_count: number;
  upcoming_events_count: number;
  recent_activity: AuditEventEntry[];
}

export interface RevisionSummary {
  id: number;
  entity_type: string;
  entity_id: number;
  created_by_email: string | null;
  created_at: string;
}

export interface SystemHealth {
  database_ok: boolean;
  migration_status: "up_to_date" | "behind" | "unknown";
  current_migration: string | null;
  head_migration: string | null;
  storage_ok: boolean;
  storage_backend: string;
}

export interface SearchResult {
  entity_type: string;
  entity_id: number;
  title: string;
  admin_path: string;
}
