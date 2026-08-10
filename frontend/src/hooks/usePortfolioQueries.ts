import { useQuery } from "@tanstack/react-query";

import { useLocale } from "@/app/LocaleContext";
import { apiFetch } from "@/services/apiClient";
import type {
  Biography,
  CommunityProfile,
  Education,
  EventFacets,
  EventItem,
  EventStats,
  GeoJsonFeatureCollection,
  JourneyMilestone,
  Passion,
  Profile,
  ProjectDetail,
  ProjectListItem,
  SkillCategory,
  Talk,
  Experience as WorkExperience,
} from "@/types/api";

const STALE_TIME = 5 * 60 * 1000;

export function useProfile() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["profile", locale],
    queryFn: () => apiFetch<Profile>("/profile", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function useBiography() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["biography", locale],
    queryFn: () => apiFetch<Biography>("/biography", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function useEducation() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["education", locale],
    queryFn: () => apiFetch<Education[]>("/education", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function useExperiences() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["experiences", locale],
    queryFn: () => apiFetch<WorkExperience[]>("/experiences", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function useSkills() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["skills", locale],
    queryFn: () => apiFetch<SkillCategory[]>("/skills", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function useProjects() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["projects", locale],
    queryFn: () => apiFetch<ProjectListItem[]>("/projects", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function useProject(slug: string | undefined) {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["project", slug, locale],
    queryFn: () => apiFetch<ProjectDetail>(`/projects/${slug}`, { lang: locale }),
    staleTime: STALE_TIME,
    enabled: Boolean(slug),
  });
}

export interface EventFilters {
  year?: number;
  country?: string;
  continent?: string;
  topic?: string;
  format?: string;
  status?: string;
  q?: string;
  milestones?: boolean;
}

export function useEvents(filters: EventFilters = {}) {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["events", locale, filters],
    queryFn: () => apiFetch<EventItem[]>("/events", { lang: locale, params: { ...filters } }),
    staleTime: STALE_TIME,
  });
}

export function useEvent(slug: string | undefined) {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["event", slug, locale],
    queryFn: () => apiFetch<EventItem>(`/events/${slug}`, { lang: locale }),
    staleTime: STALE_TIME,
    enabled: Boolean(slug),
  });
}

export function useEventFacets() {
  return useQuery({
    queryKey: ["event-facets"],
    queryFn: () => apiFetch<EventFacets>("/events/facets"),
    staleTime: STALE_TIME,
  });
}

export function useEventStats() {
  return useQuery({
    queryKey: ["event-stats"],
    queryFn: () => apiFetch<EventStats>("/events/stats"),
    staleTime: STALE_TIME,
  });
}

export function useEventsGeoJson() {
  return useQuery({
    queryKey: ["events-geojson"],
    queryFn: () => apiFetch<GeoJsonFeatureCollection>("/events/geojson"),
    staleTime: STALE_TIME,
  });
}

export function useTalks() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["talks", locale],
    queryFn: () => apiFetch<Talk[]>("/talks", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function usePassions() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["passions", locale],
    queryFn: () => apiFetch<Passion[]>("/passions", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function useCommunity() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["community", locale],
    queryFn: () => apiFetch<CommunityProfile>("/community", { lang: locale }),
    staleTime: STALE_TIME,
  });
}

export function useJourney() {
  const { locale } = useLocale();
  return useQuery({
    queryKey: ["journey", locale],
    queryFn: () => apiFetch<JourneyMilestone[]>("/journey", { lang: locale }),
    staleTime: STALE_TIME,
  });
}
