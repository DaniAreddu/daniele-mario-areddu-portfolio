import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  RecognitionAdminDetail,
  RecognitionListItem,
  RecognitionRevisionSummary,
  RecognitionWritePayload,
} from "@/admin/types/recognition";
import type { RecognitionOut } from "@/types/api";

const RECOGNITION_KEY = ["admin", "recognition"] as const;

export function useAdminRecognitionList(trashed: boolean) {
  return useQuery({
    queryKey: [...RECOGNITION_KEY, "list", trashed],
    queryFn: () =>
      adminApiFetch<RecognitionListItem[]>(`/recognition${trashed ? "?trashed=true" : ""}`),
  });
}

export function useAdminRecognitionItem(id: number | undefined) {
  return useQuery({
    queryKey: [...RECOGNITION_KEY, "detail", id],
    queryFn: () => adminApiFetch<RecognitionAdminDetail>(`/recognition/${id}`),
    enabled: id !== undefined,
  });
}

export function useAdminRecognitionPreview(id: number | undefined) {
  return useQuery({
    queryKey: [...RECOGNITION_KEY, "preview", id],
    queryFn: () => adminApiFetch<RecognitionOut>(`/recognition/${id}/preview`),
    enabled: id !== undefined,
  });
}

export function useAdminRecognitionRevisions(id: number | undefined) {
  return useQuery({
    queryKey: [...RECOGNITION_KEY, "revisions", id],
    queryFn: () => adminApiFetch<RecognitionRevisionSummary[]>(`/recognition/${id}/revisions`),
    enabled: id !== undefined,
  });
}

function useInvalidateRecognition() {
  const queryClient = useQueryClient();
  return (id?: number) => {
    void queryClient.invalidateQueries({ queryKey: RECOGNITION_KEY });
    if (id !== undefined) {
      void queryClient.invalidateQueries({ queryKey: [...RECOGNITION_KEY, "detail", id] });
    }
  };
}

export function useCreateRecognition() {
  const invalidate = useInvalidateRecognition();
  return useMutation({
    mutationFn: (payload: RecognitionWritePayload) =>
      adminApiFetch<RecognitionAdminDetail>("/recognition", { method: "POST", body: payload }),
    onSuccess: () => invalidate(),
  });
}

export function useUpdateRecognition(id: number) {
  const invalidate = useInvalidateRecognition();
  return useMutation({
    mutationFn: (payload: RecognitionWritePayload) =>
      adminApiFetch<RecognitionAdminDetail>(`/recognition/${id}`, {
        method: "PATCH",
        body: payload,
      }),
    onSuccess: () => invalidate(id),
  });
}

function useLifecycleAction(id: number, action: string) {
  const invalidate = useInvalidateRecognition();
  return useMutation({
    mutationFn: (body?: unknown) =>
      adminApiFetch<RecognitionAdminDetail>(`/recognition/${id}/${action}`, {
        method: "POST",
        body: body ?? {},
      }),
    onSuccess: () => invalidate(id),
  });
}

export function useScheduleRecognition(id: number) {
  const invalidate = useInvalidateRecognition();
  return useMutation({
    mutationFn: (publishAt: string) =>
      adminApiFetch<RecognitionAdminDetail>(`/recognition/${id}/schedule`, {
        method: "POST",
        body: { publish_at: publishAt },
      }),
    onSuccess: () => invalidate(id),
  });
}

export function useUnpublishRecognition(id: number) {
  return useLifecycleAction(id, "unpublish");
}
export function useArchiveRecognition(id: number) {
  return useLifecycleAction(id, "archive");
}
export function useTrashRecognition(id: number) {
  return useLifecycleAction(id, "trash");
}
export function useRestoreRecognition(id: number) {
  return useLifecycleAction(id, "restore");
}

export function usePermanentlyDeleteRecognition() {
  const invalidate = useInvalidateRecognition();
  return useMutation({
    mutationFn: (id: number) => adminApiFetch<void>(`/recognition/${id}`, { method: "DELETE" }),
    onSuccess: () => invalidate(),
  });
}

export function useRestoreRecognitionRevision(id: number) {
  const invalidate = useInvalidateRecognition();
  return useMutation({
    mutationFn: (revisionId: number) =>
      adminApiFetch<RecognitionAdminDetail>(
        `/recognition/${id}/revisions/${revisionId}/restore`,
        {
          method: "POST",
        },
      ),
    onSuccess: () => invalidate(id),
  });
}
