export interface MediaAsset {
  id: number;
  storage_key: string;
  url: string;
  original_filename: string;
  mime_type: string;
  size_bytes: number;
  width: number | null;
  height: number | null;
  alt_text: string | null;
  caption: string | null;
  variants: Record<string, string>;
  uploaded_by_email: string | null;
  created_at: string;
}

export interface MediaUsage {
  reference_count: number;
  referenced_in: string[];
}
