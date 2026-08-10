import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  BiographyAdmin,
  BiographyWritePayload,
  ProfileAdmin,
  ProfileWritePayload,
} from "@/admin/types/profile";

export function useAdminProfile() {
  return useQuery({
    queryKey: ["admin", "profile"],
    queryFn: () => adminApiFetch<ProfileAdmin>("/profile"),
  });
}

export function useUpdateProfile() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: ProfileWritePayload) =>
      adminApiFetch<ProfileAdmin>("/profile", { method: "PUT", body: payload }),
    onSuccess: () => void queryClient.invalidateQueries({ queryKey: ["admin", "profile"] }),
  });
}

export function useAdminBiography() {
  return useQuery({
    queryKey: ["admin", "biography"],
    queryFn: () => adminApiFetch<BiographyAdmin>("/biography"),
  });
}

export function useUpdateBiography() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: BiographyWritePayload) =>
      adminApiFetch<BiographyAdmin>("/biography", { method: "PUT", body: payload }),
    onSuccess: () => void queryClient.invalidateQueries({ queryKey: ["admin", "biography"] }),
  });
}
