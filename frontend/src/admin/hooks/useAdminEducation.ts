import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  EducationAdminDetail,
  EducationListItem,
  EducationRevisionSummary,
  EducationWritePayload,
} from "@/admin/types/education";
import type { Education } from "@/types/api";

const EDUCATION_KEY = ["admin", "education"] as const;

export function useAdminEducationList(trashed: boolean) {
  return useQuery({
    queryKey: [...EDUCATION_KEY, "list", trashed],
    queryFn: () =>
      adminApiFetch<EducationListItem[]>(`/education${trashed ? "?trashed=true" : ""}`),
  });
}

export function useAdminEducationItem(id: number | undefined) {
  return useQuery({
    queryKey: [...EDUCATION_KEY, "detail", id],
    queryFn: () => adminApiFetch<EducationAdminDetail>(`/education/${id}`),
    enabled: id !== undefined,
  });
}

export function useAdminEducationPreview(id: number | undefined) {
  return useQuery({
    queryKey: [...EDUCATION_KEY, "preview", id],
    queryFn: () => adminApiFetch<Education>(`/education/${id}/preview`),
    enabled: id !== undefined,
  });
}

export function useAdminEducationRevisions(id: number | undefined) {
  return useQuery({
    queryKey: [...EDUCATION_KEY, "revisions", id],
    queryFn: () => adminApiFetch<EducationRevisionSummary[]>(`/education/${id}/revisions`),
    enabled: id !== undefined,
  });
}

function useInvalidateEducation() {
  const queryClient = useQueryClient();
  return (id?: number) => {
    void queryClient.invalidateQueries({ queryKey: EDUCATION_KEY });
    if (id !== undefined) {
      void queryClient.invalidateQueries({ queryKey: [...EDUCATION_KEY, "detail", id] });
    }
  };
}

export function useCreateEducation() {
  const invalidate = useInvalidateEducation();
  return useMutation({
    mutationFn: (payload: EducationWritePayload) =>
      adminApiFetch<EducationAdminDetail>("/education", { method: "POST", body: payload }),
    onSuccess: () => invalidate(),
  });
}

export function useUpdateEducation(id: number) {
  const invalidate = useInvalidateEducation();
  return useMutation({
    mutationFn: (payload: EducationWritePayload) =>
      adminApiFetch<EducationAdminDetail>(`/education/${id}`, {
        method: "PATCH",
        body: payload,
      }),
    onSuccess: () => invalidate(id),
  });
}

function useLifecycleAction(id: number, action: string) {
  const invalidate = useInvalidateEducation();
  return useMutation({
    mutationFn: (body?: unknown) =>
      adminApiFetch<EducationAdminDetail>(`/education/${id}/${action}`, {
        method: "POST",
        body: body ?? {},
      }),
    onSuccess: () => invalidate(id),
  });
}

export function useScheduleEducation(id: number) {
  const invalidate = useInvalidateEducation();
  return useMutation({
    mutationFn: (publishAt: string) =>
      adminApiFetch<EducationAdminDetail>(`/education/${id}/schedule`, {
        method: "POST",
        body: { publish_at: publishAt },
      }),
    onSuccess: () => invalidate(id),
  });
}

export function useUnpublishEducation(id: number) {
  return useLifecycleAction(id, "unpublish");
}
export function useArchiveEducation(id: number) {
  return useLifecycleAction(id, "archive");
}
export function useTrashEducation(id: number) {
  return useLifecycleAction(id, "trash");
}
export function useRestoreEducation(id: number) {
  return useLifecycleAction(id, "restore");
}

export function usePermanentlyDeleteEducation() {
  const invalidate = useInvalidateEducation();
  return useMutation({
    mutationFn: (id: number) => adminApiFetch<void>(`/education/${id}`, { method: "DELETE" }),
    onSuccess: () => invalidate(),
  });
}

export function useRestoreEducationRevision(id: number) {
  const invalidate = useInvalidateEducation();
  return useMutation({
    mutationFn: (revisionId: number) =>
      adminApiFetch<EducationAdminDetail>(`/education/${id}/revisions/${revisionId}/restore`, {
        method: "POST",
      }),
    onSuccess: () => invalidate(id),
  });
}
