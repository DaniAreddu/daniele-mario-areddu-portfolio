import { useQuery } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  AuditEventEntry,
  DashboardStats,
  RevisionSummary,
  SearchResult,
  SystemHealth,
} from "@/admin/types/dashboard";

export function useAdminDashboardStats() {
  return useQuery({
    queryKey: ["admin", "dashboard"],
    queryFn: () => adminApiFetch<DashboardStats>("/dashboard"),
    staleTime: 30_000,
  });
}

export function useAdminAuditLog(entityType?: string) {
  return useQuery({
    queryKey: ["admin", "audit-log", entityType ?? "all"],
    queryFn: () =>
      adminApiFetch<AuditEventEntry[]>(
        `/audit-log${entityType ? `?entity_type=${entityType}` : ""}`,
      ),
  });
}

export function useAdminRecentRevisions() {
  return useQuery({
    queryKey: ["admin", "revisions", "recent"],
    queryFn: () => adminApiFetch<RevisionSummary[]>("/revisions/recent"),
  });
}

export function useAdminSystemHealth() {
  return useQuery({
    queryKey: ["admin", "system", "health"],
    queryFn: () => adminApiFetch<SystemHealth>("/system/health"),
    staleTime: 10_000,
  });
}

export function useAdminSearch(query: string) {
  return useQuery({
    queryKey: ["admin", "search", query],
    queryFn: () => adminApiFetch<SearchResult[]>(`/search?q=${encodeURIComponent(query)}`),
    enabled: query.trim().length >= 2,
    staleTime: 10_000,
  });
}
