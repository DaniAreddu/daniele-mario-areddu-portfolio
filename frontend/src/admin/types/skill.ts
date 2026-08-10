export interface SkillAdmin {
  id: number;
  category_id: number;
  name: string;
  context_en: string | null;
  context_it: string | null;
  is_featured: boolean;
  enabled: boolean;
  sort_order: number;
}

export interface SkillCategoryAdmin {
  id: number;
  slug: string;
  name_en: string;
  name_it: string;
  description_en: string | null;
  description_it: string | null;
  sort_order: number;
  enabled: boolean;
  skills: SkillAdmin[];
}

export interface SkillWritePayload {
  category_id: number;
  name: string;
  context_en: string | null;
  context_it: string | null;
  is_featured: boolean;
  enabled: boolean;
  sort_order: number;
}

export interface SkillCategoryWritePayload {
  slug: string;
  name_en: string;
  name_it: string;
  description_en: string | null;
  description_it: string | null;
  sort_order: number;
  enabled: boolean;
}
