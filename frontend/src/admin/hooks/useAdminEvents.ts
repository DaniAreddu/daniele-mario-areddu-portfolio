import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { adminApiFetch } from "@/admin/api/adminApiClient";
import type {
  DuplicateCandidate,
  EventAdminDetail,
  EventCreatePayload,
  EventListItem,
  EventUpdatePayload,
  RevisionDiff,
  RevisionSummary,
  TagSummary,
} from "@/admin/types/event";
import type { EventItem } from "@/types/api";

const EVENTS_KEY = ["admin", "events"] as const;

export function useAdminEventList(trashed: boolean) {
  return useQuery({
    queryKey: [...EVENTS_KEY, "list", trashed],
    queryFn: () => adminApiFetch<EventListItem[]>(`/events${trashed ? "?trashed=true" : ""}`),
  });
}

export function useAdminEvent(eventId: number | undefined) {
  return useQuery({
    queryKey: [...EVENTS_KEY, "detail", eventId],
    queryFn: () => adminApiFetch<EventAdminDetail>(`/events/${eventId}`),
    enabled: eventId !== undefined,
  });
}

export function useAdminEventPreview(eventId: number | undefined) {
  return useQuery({
    queryKey: [...EVENTS_KEY, "preview", eventId],
    queryFn: () => adminApiFetch<EventItem>(`/events/${eventId}/preview`),
    enabled: eventId !== undefined,
  });
}

export function useAdminTags() {
  return useQuery({
    queryKey: ["admin", "tags"],
    queryFn: () => adminApiFetch<TagSummary[]>("/tags"),
    staleTime: 60_000,
  });
}

export function useCheckDuplicates(eventName: string, city: string, year: number | null) {
  return useQuery({
    queryKey: [...EVENTS_KEY, "duplicates", eventName, city, year],
    queryFn: () =>
      adminApiFetch<DuplicateCandidate[]>(
        `/events/check-duplicates?${new URLSearchParams({
          event_name: eventName,
          year: String(year),
          ...(city ? { city } : {}),
        }).toString()}`,
      ),
    enabled: eventName.trim().length > 1 && year !== null,
    staleTime: 10_000,
  });
}

export function useAdminEventRevisions(eventId: number | undefined) {
  return useQuery({
    queryKey: [...EVENTS_KEY, "revisions", eventId],
    queryFn: () => adminApiFetch<RevisionSummary[]>(`/events/${eventId}/revisions`),
    enabled: eventId !== undefined,
  });
}

export function useRevisionDiff(eventId: number | undefined, revisionId: number | null) {
  return useQuery({
    queryKey: [...EVENTS_KEY, "revision-diff", eventId, revisionId],
    queryFn: () =>
      adminApiFetch<RevisionDiff>(`/events/${eventId}/revisions/${revisionId}/diff`),
    enabled: eventId !== undefined && revisionId !== null,
  });
}

function useInvalidateEvents() {
  const queryClient = useQueryClient();
  return (eventId?: number) => {
    void queryClient.invalidateQueries({ queryKey: EVENTS_KEY });
    if (eventId !== undefined) {
      void queryClient.invalidateQueries({ queryKey: [...EVENTS_KEY, "detail", eventId] });
    }
  };
}

export function useCreateEvent() {
  const invalidate = useInvalidateEvents();
  return useMutation({
    mutationFn: (payload: EventCreatePayload) =>
      adminApiFetch<EventAdminDetail>("/events", { method: "POST", body: payload }),
    onSuccess: () => invalidate(),
  });
}

export function useUpdateEvent(eventId: number) {
  const invalidate = useInvalidateEvents();
  return useMutation({
    mutationFn: (payload: EventUpdatePayload) =>
      adminApiFetch<EventAdminDetail>(`/events/${eventId}`, { method: "PATCH", body: payload }),
    onSuccess: () => invalidate(eventId),
  });
}

function useLifecycleAction(eventId: number, action: string) {
  const invalidate = useInvalidateEvents();
  return useMutation({
    mutationFn: (body?: unknown) =>
      adminApiFetch<EventAdminDetail>(`/events/${eventId}/${action}`, {
        method: "POST",
        body: body ?? {},
      }),
    onSuccess: () => invalidate(eventId),
  });
}

export function usePublishEvent(eventId: number) {
  return useLifecycleAction(eventId, "publish");
}
export function useUnpublishEvent(eventId: number) {
  return useLifecycleAction(eventId, "unpublish");
}
export function useArchiveEvent(eventId: number) {
  return useLifecycleAction(eventId, "archive");
}
export function useTrashEvent(eventId: number) {
  return useLifecycleAction(eventId, "trash");
}
export function useRestoreEvent(eventId: number) {
  return useLifecycleAction(eventId, "restore");
}

export function useScheduleEvent(eventId: number) {
  const invalidate = useInvalidateEvents();
  return useMutation({
    mutationFn: (publishAt: string) =>
      adminApiFetch<EventAdminDetail>(`/events/${eventId}/schedule`, {
        method: "POST",
        body: { publish_at: publishAt },
      }),
    onSuccess: () => invalidate(eventId),
  });
}

export function usePermanentlyDeleteEvent() {
  const invalidate = useInvalidateEvents();
  return useMutation({
    mutationFn: (eventId: number) =>
      adminApiFetch<void>(`/events/${eventId}`, { method: "DELETE" }),
    onSuccess: () => invalidate(),
  });
}

export function useRestoreRevision(eventId: number) {
  const invalidate = useInvalidateEvents();
  return useMutation({
    mutationFn: (revisionId: number) =>
      adminApiFetch<EventAdminDetail>(`/events/${eventId}/revisions/${revisionId}/restore`, {
        method: "POST",
      }),
    onSuccess: () => invalidate(eventId),
  });
}
