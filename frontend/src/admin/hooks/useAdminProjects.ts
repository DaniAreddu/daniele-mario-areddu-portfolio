import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  AdminProjectListItem,
  ProjectAdminDetail,
  ProjectCreatePayload,
  ProjectRevisionSummary,
  ProjectWritePayload,
} from "@/admin/types/project";
import type { ProjectDetail } from "@/types/api";

const PROJECTS_KEY = ["admin", "projects"] as const;

export function useAdminProjectList(trashed: boolean) {
  return useQuery({
    queryKey: [...PROJECTS_KEY, "list", trashed],
    queryFn: () =>
      adminApiFetch<AdminProjectListItem[]>(`/projects${trashed ? "?trashed=true" : ""}`),
  });
}

export function useAdminProject(projectId: number | undefined) {
  return useQuery({
    queryKey: [...PROJECTS_KEY, "detail", projectId],
    queryFn: () => adminApiFetch<ProjectAdminDetail>(`/projects/${projectId}`),
    enabled: projectId !== undefined,
  });
}

export function useAdminProjectPreview(projectId: number | undefined) {
  return useQuery({
    queryKey: [...PROJECTS_KEY, "preview", projectId],
    queryFn: () => adminApiFetch<ProjectDetail>(`/projects/${projectId}/preview`),
    enabled: projectId !== undefined,
  });
}

export function useAdminProjectRevisions(projectId: number | undefined) {
  return useQuery({
    queryKey: [...PROJECTS_KEY, "revisions", projectId],
    queryFn: () => adminApiFetch<ProjectRevisionSummary[]>(`/projects/${projectId}/revisions`),
    enabled: projectId !== undefined,
  });
}

function useInvalidateProjects() {
  const queryClient = useQueryClient();
  return (projectId?: number) => {
    void queryClient.invalidateQueries({ queryKey: PROJECTS_KEY });
    if (projectId !== undefined) {
      void queryClient.invalidateQueries({ queryKey: [...PROJECTS_KEY, "detail", projectId] });
    }
  };
}

export function useCreateProject() {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: (payload: ProjectCreatePayload) =>
      adminApiFetch<ProjectAdminDetail>("/projects", { method: "POST", body: payload }),
    onSuccess: () => invalidate(),
  });
}

export function useUpdateProject(projectId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: (payload: ProjectWritePayload) =>
      adminApiFetch<ProjectAdminDetail>(`/projects/${projectId}`, {
        method: "PATCH",
        body: payload,
      }),
    onSuccess: () => invalidate(projectId),
  });
}

function useLifecycleAction(projectId: number, action: string) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: (body?: unknown) =>
      adminApiFetch<ProjectAdminDetail>(`/projects/${projectId}/${action}`, {
        method: "POST",
        body: body ?? {},
      }),
    onSuccess: () => invalidate(projectId),
  });
}

export function usePublishProject(projectId: number) {
  return useLifecycleAction(projectId, "publish");
}
export function useUnpublishProject(projectId: number) {
  return useLifecycleAction(projectId, "unpublish");
}
export function useArchiveProject(projectId: number) {
  return useLifecycleAction(projectId, "archive");
}
export function useTrashProject(projectId: number) {
  return useLifecycleAction(projectId, "trash");
}
export function useRestoreProject(projectId: number) {
  return useLifecycleAction(projectId, "restore");
}

export function usePermanentlyDeleteProject() {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: (projectId: number) =>
      adminApiFetch<void>(`/projects/${projectId}`, { method: "DELETE" }),
    onSuccess: () => invalidate(),
  });
}

export function useRestoreProjectRevision(projectId: number) {
  const invalidate = useInvalidateProjects();
  return useMutation({
    mutationFn: (revisionId: number) =>
      adminApiFetch<ProjectAdminDetail>(
        `/projects/${projectId}/revisions/${revisionId}/restore`,
        {
          method: "POST",
        },
      ),
    onSuccess: () => invalidate(projectId),
  });
}
