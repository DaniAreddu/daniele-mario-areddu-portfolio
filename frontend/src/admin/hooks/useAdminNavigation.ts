import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type { NavigationItemAdmin, NavigationItemWritePayload } from "@/admin/types/siteAdmin";

const KEY = ["admin", "navigation"] as const;

export function useAdminNavigationList() {
  return useQuery({
    queryKey: KEY,
    queryFn: () => adminApiFetch<NavigationItemAdmin[]>("/navigation"),
  });
}

function useInvalidate() {
  const queryClient = useQueryClient();
  return () => {
    void queryClient.invalidateQueries({ queryKey: KEY });
    // Admin and public pages share one QueryClient (same SPA) — without this,
    // an admin who edits navigation and navigates to the public site in the
    // same tab would see stale data for the rest of the public query's
    // staleTime.
    void queryClient.invalidateQueries({ queryKey: ["navigation"] });
  };
}

export function useCreateNavigationItem() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: (payload: NavigationItemWritePayload) =>
      adminApiFetch<NavigationItemAdmin>("/navigation", { method: "POST", body: payload }),
    onSuccess: invalidate,
  });
}

export function useUpdateNavigationItem() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: NavigationItemWritePayload }) =>
      adminApiFetch<NavigationItemAdmin>(`/navigation/${id}`, {
        method: "PATCH",
        body: payload,
      }),
    onSuccess: invalidate,
  });
}

export function useDeleteNavigationItem() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: (id: number) => adminApiFetch<void>(`/navigation/${id}`, { method: "DELETE" }),
    onSuccess: invalidate,
  });
}
