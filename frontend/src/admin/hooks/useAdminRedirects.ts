import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type { RedirectAdmin, RedirectWritePayload } from "@/admin/types/siteAdmin";

const KEY = ["admin", "redirects"] as const;

export function useAdminRedirectList() {
  return useQuery({
    queryKey: KEY,
    queryFn: () => adminApiFetch<RedirectAdmin[]>("/redirects"),
  });
}

function useInvalidate() {
  const queryClient = useQueryClient();
  return () => void queryClient.invalidateQueries({ queryKey: KEY });
}

export function useCreateRedirect() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: (payload: RedirectWritePayload) =>
      adminApiFetch<RedirectAdmin>("/redirects", { method: "POST", body: payload }),
    onSuccess: invalidate,
  });
}

export function useUpdateRedirect() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: RedirectWritePayload }) =>
      adminApiFetch<RedirectAdmin>(`/redirects/${id}`, { method: "PATCH", body: payload }),
    onSuccess: invalidate,
  });
}

export function useDeleteRedirect() {
  const invalidate = useInvalidate();
  return useMutation({
    mutationFn: (id: number) => adminApiFetch<void>(`/redirects/${id}`, { method: "DELETE" }),
    onSuccess: invalidate,
  });
}
