export interface SiteSettingsAdmin {
  id: number;
  site_name: string;
  public_site_url: string | null;
  default_timezone: string;
  default_language: string;
  maintenance_mode: boolean;
  show_speaking_map: boolean;
  show_statistics: boolean;
  show_now_section: boolean;
  show_projects: boolean;
  show_community: boolean;
  map_default_zoom: number;
  analytics_id: string | null;
  created_at: string;
  updated_at: string;
}

export type SiteSettingsWritePayload = Omit<
  SiteSettingsAdmin,
  "id" | "created_at" | "updated_at"
>;

export interface SeoSettingsAdmin {
  id: number;
  site_title: string;
  title_template: string;
  default_description: string;
  default_og_image_url: string | null;
  twitter_card_type: string;
  robots_default: string;
  canonical_base_url: string | null;
  created_at: string;
  updated_at: string;
}

export type SeoSettingsWritePayload = Omit<
  SeoSettingsAdmin,
  "id" | "created_at" | "updated_at"
>;

export interface NavigationItemAdmin {
  id: number;
  label_en: string;
  label_it: string;
  target: string;
  placement: "header" | "footer";
  is_external: boolean;
  open_in_new_tab: boolean;
  enabled: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export type NavigationItemWritePayload = Omit<
  NavigationItemAdmin,
  "id" | "created_at" | "updated_at"
>;

export interface SocialLinkAdmin {
  id: number;
  label: string;
  url: string;
  icon: string | null;
  enabled: boolean;
  sort_order: number;
  created_at: string;
  updated_at: string;
}

export type SocialLinkWritePayload = Omit<SocialLinkAdmin, "id" | "created_at" | "updated_at">;

export interface RedirectAdmin {
  id: number;
  source_path: string;
  destination_path: string;
  status_code: number;
  enabled: boolean;
  created_at: string;
  updated_at: string;
}

export type RedirectWritePayload = Omit<RedirectAdmin, "id" | "created_at" | "updated_at">;

export interface HomepageSettingsAdmin {
  id: number;
  hero_eyebrow_en: string;
  hero_eyebrow_it: string;
  hero_headline_en: string;
  hero_headline_it: string;
  hero_subheadline_en: string;
  hero_subheadline_it: string;
  primary_cta_label_en: string | null;
  primary_cta_label_it: string | null;
  primary_cta_url: string | null;
  secondary_cta_label_en: string | null;
  secondary_cta_label_it: string | null;
  secondary_cta_url: string | null;
  section_order: string[];
  section_visibility: Record<string, boolean>;
  created_at: string;
  updated_at: string;
}

export type HomepageSettingsWritePayload = Omit<
  HomepageSettingsAdmin,
  "id" | "created_at" | "updated_at"
>;

export interface HomepageFeatureAdmin {
  id: number;
  entity_type: "project" | "event";
  entity_id: number;
  sort_order: number;
}

export type HomepageFeatureWritePayload = Omit<HomepageFeatureAdmin, "id">;
