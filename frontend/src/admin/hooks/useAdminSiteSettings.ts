import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  SeoSettingsAdmin,
  SeoSettingsWritePayload,
  SiteSettingsAdmin,
  SiteSettingsWritePayload,
} from "@/admin/types/siteAdmin";

export function useAdminSiteSettings() {
  return useQuery({
    queryKey: ["admin", "site-settings"],
    queryFn: () => adminApiFetch<SiteSettingsAdmin>("/site-settings"),
  });
}

export function useUpdateSiteSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: SiteSettingsWritePayload) =>
      adminApiFetch<SiteSettingsAdmin>("/site-settings", { method: "PUT", body: payload }),
    onSuccess: () =>
      void queryClient.invalidateQueries({ queryKey: ["admin", "site-settings"] }),
  });
}

export function useAdminSeoSettings() {
  return useQuery({
    queryKey: ["admin", "seo-settings"],
    queryFn: () => adminApiFetch<SeoSettingsAdmin>("/seo-settings"),
  });
}

export function useUpdateSeoSettings() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: SeoSettingsWritePayload) =>
      adminApiFetch<SeoSettingsAdmin>("/seo-settings", { method: "PUT", body: payload }),
    onSuccess: () =>
      void queryClient.invalidateQueries({ queryKey: ["admin", "seo-settings"] }),
  });
}
