import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type { SocialLinkAdmin, SocialLinkWritePayload } from "@/admin/types/siteAdmin";

const KEY = ["admin", "social-links"] as const;

export function useAdminSocialLinkList() {
  return useQuery({
    queryKey: KEY,
    queryFn: () => adminApiFetch<SocialLinkAdmin[]>("/social-links"),
  });
}

function useInvalidate() {
  const queryClient = useQueryClient();
  return () => {
    void queryClient.invalidateQueries({ queryKey: KEY });
    // Admin and public pages share one QueryClient (same SPA) — without this,
    // an admin who edits a link and navigates to the public site in the same
    // tab would see stale data for the rest of the public query's staleTime.
    void queryClient.invalidateQueries({ queryKey: ["social-links"] });
  };
}

export function useCreateSocialLink() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: (payload: SocialLinkWritePayload) =>
      adminApiFetch<SocialLinkAdmin>("/social-links", { method: "POST", body: payload }),
    onSuccess: invalidate,
  });
}

export function useUpdateSocialLink() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: SocialLinkWritePayload }) =>
      adminApiFetch<SocialLinkAdmin>(`/social-links/${id}`, { method: "PATCH", body: payload }),
    onSuccess: invalidate,
  });
}

export function useDeleteSocialLink() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: (id: number) =>
      adminApiFetch<void>(`/social-links/${id}`, { method: "DELETE" }),
    onSuccess: invalidate,
  });
}
