import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  HomepageFeatureAdmin,
  HomepageFeatureWritePayload,
  HomepageSettingsAdmin,
  HomepageSettingsWritePayload,
} from "@/admin/types/siteAdmin";

export function useAdminHomepageSettings() {
  return useQuery({
    queryKey: ["admin", "homepage", "settings"],
    queryFn: () => adminApiFetch<HomepageSettingsAdmin>("/homepage/settings"),
  });
}

function invalidatePublicHomepage(queryClient: ReturnType<typeof useQueryClient>): void {
  // Admin and public pages share one QueryClient (same SPA) — without this,
  // an admin who edits the homepage and navigates to the public site in the
  // same tab would see stale data for the rest of the public query's
  // staleTime.
  void queryClient.invalidateQueries({ queryKey: ["homepage"] });
}

export function useUpdateHomepageSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: HomepageSettingsWritePayload) =>
      adminApiFetch<HomepageSettingsAdmin>("/homepage/settings", {
        method: "PUT",
        body: payload,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "homepage", "settings"] });
      invalidatePublicHomepage(queryClient);
    },
  });
}

export function useAdminHomepageFeatures() {
  return useQuery({
    queryKey: ["admin", "homepage", "features"],
    queryFn: () => adminApiFetch<HomepageFeatureAdmin[]>("/homepage/features"),
  });
}

export function useCreateHomepageFeature() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: HomepageFeatureWritePayload) =>
      adminApiFetch<HomepageFeatureAdmin>("/homepage/features", {
        method: "POST",
        body: payload,
      }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "homepage", "features"] });
      invalidatePublicHomepage(queryClient);
    },
  });
}

export function useDeleteHomepageFeature() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (id: number) =>
      adminApiFetch<void>(`/homepage/features/${id}`, { method: "DELETE" }),
    onSuccess: () => {
      void queryClient.invalidateQueries({ queryKey: ["admin", "homepage", "features"] });
      invalidatePublicHomepage(queryClient);
    },
  });
}
