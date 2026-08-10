export interface ProfileAdmin {
  id: number;
  full_name: string;
  roles: string[];
  location: string;
  base_country: string;
  availability_en: string;
  availability_it: string;
  tagline_en: string;
  tagline_it: string;
  positioning_statement_en: string;
  positioning_statement_it: string;
  brand_label: string;
  public_email: string;
  github_url: string | null;
  linkedin_url: string | null;
  sessionize_url: string | null;
  talks_count_label: string;
  speaking_years_label: string;
  speaking_regions_label: string;
  created_at: string;
  updated_at: string;
}

export type ProfileWritePayload = Omit<ProfileAdmin, "id" | "created_at" | "updated_at">;

export interface BiographyAdmin {
  id: number;
  micro_en: string;
  micro_it: string;
  short_en: string;
  short_it: string;
  medium_en: string;
  medium_it: string;
  long_en: string;
  long_it: string;
  speaker_bio_en: string;
  speaker_bio_it: string;
  created_at: string;
  updated_at: string;
}

export type BiographyWritePayload = Omit<BiographyAdmin, "id" | "created_at" | "updated_at">;
