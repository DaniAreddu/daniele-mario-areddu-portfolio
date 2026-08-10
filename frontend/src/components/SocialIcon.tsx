import {
  Github,
  Globe,
  Instagram,
  Linkedin,
  Mail,
  Rss,
  Twitter,
  Youtube,
  type LucideIcon,
} from "lucide-react";

// Kept in sync with the backend's ALLOWED_ICONS allow-list
// (backend/app/schemas/social_link_admin.py) — an icon name that isn't a
// key here just renders nothing rather than crashing. Lucide has no
// dedicated Mastodon glyph, so "mastodon"/"sessionize" fall back to Globe.
const ICONS: Record<string, LucideIcon> = {
  github: Github,
  linkedin: Linkedin,
  twitter: Twitter,
  mastodon: Globe,
  youtube: Youtube,
  instagram: Instagram,
  rss: Rss,
  mail: Mail,
  globe: Globe,
  sessionize: Globe,
};

export function SocialIcon({ name, className }: { name: string | null; className?: string }) {
  if (!name) return null;
  const Icon = ICONS[name];
  if (!Icon) return null;
  return <Icon className={className} aria-hidden="true" />;
}
