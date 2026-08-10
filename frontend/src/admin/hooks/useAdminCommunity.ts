import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  CommunityActivityAdminDetail,
  CommunityActivityListItem,
  CommunityActivityRevisionSummary,
  CommunityActivityWritePayload,
  CommunityProfileAdmin,
  CommunityProfileWritePayload,
} from "@/admin/types/community";
import type { CommunityActivity } from "@/types/api";

const COMMUNITY_KEY = ["admin", "community"] as const;

export function useAdminCommunityProfile() {
  return useQuery({
    queryKey: [...COMMUNITY_KEY, "profile"],
    queryFn: () => adminApiFetch<CommunityProfileAdmin>("/community/profile"),
  });
}

export function useUpdateCommunityProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: CommunityProfileWritePayload) =>
      adminApiFetch<CommunityProfileAdmin>("/community/profile", {
        method: "PUT",
        body: payload,
      }),
    onSuccess: () =>
      void queryClient.invalidateQueries({ queryKey: [...COMMUNITY_KEY, "profile"] }),
  });
}

export function useAdminActivityList(trashed: boolean) {
  return useQuery({
    queryKey: [...COMMUNITY_KEY, "activities", "list", trashed],
    queryFn: () =>
      adminApiFetch<CommunityActivityListItem[]>(
        `/community/activities${trashed ? "?trashed=true" : ""}`,
      ),
  });
}

export function useAdminActivity(id: number | undefined) {
  return useQuery({
    queryKey: [...COMMUNITY_KEY, "activities", "detail", id],
    queryFn: () => adminApiFetch<CommunityActivityAdminDetail>(`/community/activities/${id}`),
    enabled: id !== undefined,
  });
}

export function useAdminActivityPreview(id: number | undefined) {
  return useQuery({
    queryKey: [...COMMUNITY_KEY, "activities", "preview", id],
    queryFn: () => adminApiFetch<CommunityActivity>(`/community/activities/${id}/preview`),
    enabled: id !== undefined,
  });
}

export function useAdminActivityRevisions(id: number | undefined) {
  return useQuery({
    queryKey: [...COMMUNITY_KEY, "activities", "revisions", id],
    queryFn: () =>
      adminApiFetch<CommunityActivityRevisionSummary[]>(
        `/community/activities/${id}/revisions`,
      ),
    enabled: id !== undefined,
  });
}

function useInvalidateActivities() {
  const queryClient = useQueryClient();
  return (id?: number) => {
    void queryClient.invalidateQueries({ queryKey: [...COMMUNITY_KEY, "activities"] });
    if (id !== undefined) {
      void queryClient.invalidateQueries({
        queryKey: [...COMMUNITY_KEY, "activities", "detail", id],
      });
    }
  };
}

export function useCreateActivity() {
  const invalidate = useInvalidateActivities();
  return useMutation({
    mutationFn: (payload: CommunityActivityWritePayload) =>
      adminApiFetch<CommunityActivityAdminDetail>("/community/activities", {
        method: "POST",
        body: payload,
      }),
    onSuccess: () => invalidate(),
  });
}

export function useUpdateActivity(id: number) {
  const invalidate = useInvalidateActivities();
  return useMutation({
    mutationFn: (payload: CommunityActivityWritePayload) =>
      adminApiFetch<CommunityActivityAdminDetail>(`/community/activities/${id}`, {
        method: "PATCH",
        body: payload,
      }),
    onSuccess: () => invalidate(id),
  });
}

function useLifecycleAction(id: number, action: string) {
  const invalidate = useInvalidateActivities();
  return useMutation({
    mutationFn: (body?: unknown) =>
      adminApiFetch<CommunityActivityAdminDetail>(`/community/activities/${id}/${action}`, {
        method: "POST",
        body: body ?? {},
      }),
    onSuccess: () => invalidate(id),
  });
}

export function useScheduleActivity(id: number) {
  const invalidate = useInvalidateActivities();
  return useMutation({
    mutationFn: (publishAt: string) =>
      adminApiFetch<CommunityActivityAdminDetail>(`/community/activities/${id}/schedule`, {
        method: "POST",
        body: { publish_at: publishAt },
      }),
    onSuccess: () => invalidate(id),
  });
}

export function useUnpublishActivity(id: number) {
  return useLifecycleAction(id, "unpublish");
}
export function useArchiveActivity(id: number) {
  return useLifecycleAction(id, "archive");
}
export function useTrashActivity(id: number) {
  return useLifecycleAction(id, "trash");
}
export function useRestoreActivity(id: number) {
  return useLifecycleAction(id, "restore");
}

export function usePermanentlyDeleteActivity() {
  const invalidate = useInvalidateActivities();
  return useMutation({
    mutationFn: (id: number) =>
      adminApiFetch<void>(`/community/activities/${id}`, { method: "DELETE" }),
    onSuccess: () => invalidate(),
  });
}

export function useRestoreActivityRevision(id: number) {
  const invalidate = useInvalidateActivities();
  return useMutation({
    mutationFn: (revisionId: number) =>
      adminApiFetch<CommunityActivityAdminDetail>(
        `/community/activities/${id}/revisions/${revisionId}/restore`,
        { method: "POST" },
      ),
    onSuccess: () => invalidate(id),
  });
}
