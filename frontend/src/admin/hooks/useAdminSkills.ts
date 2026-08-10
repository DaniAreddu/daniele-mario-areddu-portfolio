import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  SkillAdmin,
  SkillCategoryAdmin,
  SkillCategoryWritePayload,
  SkillWritePayload,
} from "@/admin/types/skill";

const SKILLS_KEY = ["admin", "skills"] as const;

export function useAdminSkillCategories() {
  return useQuery({
    queryKey: SKILLS_KEY,
    queryFn: () => adminApiFetch<SkillCategoryAdmin[]>("/skills/categories"),
  });
}

function useInvalidateSkills() {
  const queryClient = useQueryClient();
  return () => void queryClient.invalidateQueries({ queryKey: SKILLS_KEY });
}

export function useCreateSkillCategory() {
  const invalidate = useInvalidateSkills();
  return useMutation({
    mutationFn: (payload: SkillCategoryWritePayload) =>
      adminApiFetch<SkillCategoryAdmin>("/skills/categories", {
        method: "POST",
        body: payload,
      }),
    onSuccess: invalidate,
  });
}

export function useUpdateSkillCategory() {
  const invalidate = useInvalidateSkills();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: SkillCategoryWritePayload }) =>
      adminApiFetch<SkillCategoryAdmin>(`/skills/categories/${id}`, {
        method: "PATCH",
        body: payload,
      }),
    onSuccess: invalidate,
  });
}

export function useDeleteSkillCategory() {
  const invalidate = useInvalidateSkills();
  return useMutation({
    mutationFn: (id: number) =>
      adminApiFetch<void>(`/skills/categories/${id}`, { method: "DELETE" }),
    onSuccess: invalidate,
  });
}

export function useCreateSkill() {
  const invalidate = useInvalidateSkills();
  return useMutation({
    mutationFn: (payload: SkillWritePayload) =>
      adminApiFetch<SkillAdmin>("/skills", { method: "POST", body: payload }),
    onSuccess: invalidate,
  });
}

export function useUpdateSkill() {
  const invalidate = useInvalidateSkills();
  return useMutation({
    mutationFn: ({ id, payload }: { id: number; payload: SkillWritePayload }) =>
      adminApiFetch<SkillAdmin>(`/skills/${id}`, { method: "PATCH", body: payload }),
    onSuccess: invalidate,
  });
}

export function useDeleteSkill() {
  const invalidate = useInvalidateSkills();
  return useMutation({
    mutationFn: (id: number) => adminApiFetch<void>(`/skills/${id}`, { method: "DELETE" }),
    onSuccess: invalidate,
  });
}
