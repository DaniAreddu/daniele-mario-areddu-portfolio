import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch, adminApiUpload } from "@/admin/api/adminApiClient";
import type { MediaAsset, MediaUsage } from "@/admin/types/media";

const MEDIA_KEY = ["admin", "media"] as const;

export function useAdminMediaList() {
  return useQuery({
    queryKey: MEDIA_KEY,
    queryFn: () => adminApiFetch<MediaAsset[]>("/media"),
  });
}

export function useAdminMediaUsage(id: number | undefined) {
  return useQuery({
    queryKey: [...MEDIA_KEY, "usage", id],
    queryFn: () => adminApiFetch<MediaUsage>(`/media/${id}/usage`),
    enabled: id !== undefined,
  });
}

function useInvalidateMedia() {
  const queryClient = useQueryClient();
  return () => void queryClient.invalidateQueries({ queryKey: MEDIA_KEY });
}

export function useUploadMedia() {
  const invalidate = useInvalidateMedia();
  return useMutation({
    mutationFn: (file: File) => adminApiUpload<MediaAsset>("/media", file),
    onSuccess: invalidate,
  });
}

export function useUpdateMedia() {
  const invalidate = useInvalidateMedia();
  return useMutation({
    mutationFn: ({
      id,
      altText,
      caption,
    }: {
      id: number;
      altText: string | null;
      caption: string | null;
    }) =>
      adminApiFetch<MediaAsset>(`/media/${id}`, {
        method: "PATCH",
        body: { alt_text: altText, caption },
      }),
    onSuccess: invalidate,
  });
}

export function useDeleteMedia() {
  const invalidate = useInvalidateMedia();
  return useMutation({
    mutationFn: ({ id, force }: { id: number; force?: boolean }) =>
      adminApiFetch<void>(`/media/${id}${force ? "?force=true" : ""}`, { method: "DELETE" }),
    onSuccess: invalidate,
  });
}
