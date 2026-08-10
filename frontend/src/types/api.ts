export interface Profile {
  full_name: string;
  roles: string[];
  location: string;
  base_country: string;
  availability: string;
  tagline: string;
  positioning_statement: string;
  brand_label: string;
  public_email: string;
  github_url: string | null;
  linkedin_url: string | null;
  sessionize_url: string | null;
  talks_count_label: string;
  speaking_years_label: string;
  speaking_regions_label: string;
}

export interface Biography {
  micro: string;
  short: string;
  medium: string;
  long: string;
  speaker_bio: string;
}

export interface Education {
  institution: string;
  degree: string;
  location: string;
  start_year: number | null;
  end_year: number | null;
  is_ongoing: boolean;
  description: string | null;
}

export interface Experience {
  organization: string;
  role: string;
  location: string;
  start_date: string;
  end_date: string | null;
  is_current: boolean;
  summary: string;
  highlights: string[];
  technologies: string[];
}

export interface Skill {
  name: string;
  context: string | null;
}

export interface SkillCategory {
  slug: string;
  name: string;
  description: string | null;
  skills: Skill[];
}

export interface ProjectListItem {
  slug: string;
  title: string;
  summary: string;
  technologies: string[];
  is_featured: boolean;
  external_url: string | null;
}

export interface ProjectDetail extends ProjectListItem {
  problem: string;
  challenge: string;
  approach: string;
  architecture: string;
  key_decisions: string[];
  outcome: string;
  lessons: string;
  confidentiality_note: string;
  related_skills: string[];
}

export interface Talk {
  slug: string;
  title: string;
  language: string;
  summary: string | null;
  topics: string[];
  is_featured: boolean;
  event_slugs: string[];
}

export interface EventItem {
  slug: string;
  event_name: string;
  session_title: string | null;
  short_description: string | null;
  full_description: string | null;
  start_date: string | null;
  end_date: string | null;
  year: number;
  /** Known even when the exact day isn't (e.g. "September 2026"). */
  month: number | null;
  city: string | null;
  country: string | null;
  continent: string | null;
  latitude: number | null;
  longitude: number | null;
  venue: string | null;
  format: string;
  language: string;
  topics: string[];
  event_url: string | null;
  slides_url: string | null;
  recording_url: string | null;
  image: string | null;
  /** "completed" for past engagements; "upcoming" / "incoming" for engagements
   * that haven't happened yet — never inferred, always set explicitly in the
   * source data (see docs/event-management.md). */
  status: string;
  sessions_count: number;
  is_featured: boolean;
  /** A small, curated set of major geographic-expansion moments — distinct
   * from is_featured, which highlights notable session content. */
  is_international_milestone: boolean;
  talk_title: string | null;
}

export interface EventFacets {
  years: number[];
  countries: string[];
  continents: string[];
  topics: string[];
  event_names: string[];
  formats: string[];
}

export interface EventStats {
  total_events: number;
  total_countries: number;
  total_cities: number;
  total_continents: number;
  first_year: number;
  last_year: number;
  international_count: number;
  upcoming_count: number;
  gdg_devfest_count: number;
}

export interface GeoJsonFeature {
  type: "Feature";
  geometry: { type: "Point"; coordinates: [number, number] };
  properties: {
    slug: string;
    event_name: string;
    session_title: string | null;
    city: string | null;
    country: string | null;
    continent: string | null;
    year: number;
    month: number | null;
    start_date: string | null;
    end_date: string | null;
    format: string;
    topics: string[];
    status: string;
    is_featured: boolean;
    is_international_milestone: boolean;
    event_url: string | null;
  };
}

export interface GeoJsonFeatureCollection {
  type: "FeatureCollection";
  features: GeoJsonFeature[];
}

export interface Passion {
  slug: string;
  title: string;
  text: string;
  motif_label: string | null;
}

export interface CommunityActivity {
  slug: string;
  title: string;
  description: string;
  activity_date: string | null;
  activity_type: string;
  url: string | null;
}

export interface CommunityProfile {
  name: string;
  role: string;
  mission: string;
  description: string;
  vision: string;
  collaboration: string;
  founded_year: number;
  website_url: string | null;
  activities: CommunityActivity[];
}

export interface JourneyMilestone {
  year: number | null;
  title: string;
  text: string;
  kind: string;
  event_slug: string | null;
}

export type ContactRequestType =
  | "speaking_invitation"
  | "workshop"
  | "engineering_collaboration"
  | "community_partnership"
  | "podcast_interview"
  | "other";

export interface ContactPayload {
  name: string;
  email: string;
  organization?: string;
  request_type: ContactRequestType;
  event_or_project?: string;
  indicative_date?: string;
  message: string;
  consent_given: boolean;
  website?: string;
}

export interface ContactResult {
  received: boolean;
  email_delivered: boolean;
}

export interface ApiErrorBody {
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}
