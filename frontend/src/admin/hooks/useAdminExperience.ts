import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  ExperienceAdminDetail,
  ExperienceListItem,
  ExperienceRevisionSummary,
  ExperienceWritePayload,
} from "@/admin/types/experience";
import type { Experience } from "@/types/api";

const EXPERIENCE_KEY = ["admin", "experience"] as const;

export function useAdminExperienceList(trashed: boolean) {
  return useQuery({
    queryKey: [...EXPERIENCE_KEY, "list", trashed],
    queryFn: () =>
      adminApiFetch<ExperienceListItem[]>(`/experience${trashed ? "?trashed=true" : ""}`),
  });
}

export function useAdminExperienceItem(id: number | undefined) {
  return useQuery({
    queryKey: [...EXPERIENCE_KEY, "detail", id],
    queryFn: () => adminApiFetch<ExperienceAdminDetail>(`/experience/${id}`),
    enabled: id !== undefined,
  });
}

export function useAdminExperiencePreview(id: number | undefined) {
  return useQuery({
    queryKey: [...EXPERIENCE_KEY, "preview", id],
    queryFn: () => adminApiFetch<Experience>(`/experience/${id}/preview`),
    enabled: id !== undefined,
  });
}

export function useAdminExperienceRevisions(id: number | undefined) {
  return useQuery({
    queryKey: [...EXPERIENCE_KEY, "revisions", id],
    queryFn: () => adminApiFetch<ExperienceRevisionSummary[]>(`/experience/${id}/revisions`),
    enabled: id !== undefined,
  });
}

function useInvalidateExperience() {
  const queryClient = useQueryClient();
  return (id?: number) => {
    void queryClient.invalidateQueries({ queryKey: EXPERIENCE_KEY });
    if (id !== undefined) {
      void queryClient.invalidateQueries({ queryKey: [...EXPERIENCE_KEY, "detail", id] });
    }
  };
}

export function useCreateExperience() {
  const invalidate = useInvalidateExperience();
  return useMutation({
    mutationFn: (payload: ExperienceWritePayload) =>
      adminApiFetch<ExperienceAdminDetail>("/experience", { method: "POST", body: payload }),
    onSuccess: () => invalidate(),
  });
}

export function useUpdateExperience(id: number) {
  const invalidate = useInvalidateExperience();
  return useMutation({
    mutationFn: (payload: ExperienceWritePayload) =>
      adminApiFetch<ExperienceAdminDetail>(`/experience/${id}`, {
        method: "PATCH",
        body: payload,
      }),
    onSuccess: () => invalidate(id),
  });
}

function useLifecycleAction(id: number, action: string) {
  const invalidate = useInvalidateExperience();
  return useMutation({
    mutationFn: (body?: unknown) =>
      adminApiFetch<ExperienceAdminDetail>(`/experience/${id}/${action}`, {
        method: "POST",
        body: body ?? {},
      }),
    onSuccess: () => invalidate(id),
  });
}

export function useScheduleExperience(id: number) {
  const invalidate = useInvalidateExperience();
  return useMutation({
    mutationFn: (publishAt: string) =>
      adminApiFetch<ExperienceAdminDetail>(`/experience/${id}/schedule`, {
        method: "POST",
        body: { publish_at: publishAt },
      }),
    onSuccess: () => invalidate(id),
  });
}

export function useUnpublishExperience(id: number) {
  return useLifecycleAction(id, "unpublish");
}
export function useArchiveExperience(id: number) {
  return useLifecycleAction(id, "archive");
}
export function useTrashExperience(id: number) {
  return useLifecycleAction(id, "trash");
}
export function useRestoreExperience(id: number) {
  return useLifecycleAction(id, "restore");
}

export function usePermanentlyDeleteExperience() {
  const invalidate = useInvalidateExperience();
  return useMutation({
    mutationFn: (id: number) => adminApiFetch<void>(`/experience/${id}`, { method: "DELETE" }),
    onSuccess: () => invalidate(),
  });
}

export function useRestoreExperienceRevision(id: number) {
  const invalidate = useInvalidateExperience();
  return useMutation({
    mutationFn: (revisionId: number) =>
      adminApiFetch<ExperienceAdminDetail>(
        `/experience/${id}/revisions/${revisionId}/restore`,
        {
          method: "POST",
        },
      ),
    onSuccess: () => invalidate(id),
  });
}
