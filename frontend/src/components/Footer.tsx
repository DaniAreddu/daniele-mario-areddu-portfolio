import { useTranslation } from "react-i18next";
import { NavLink } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { SocialIcon } from "@/components/SocialIcon";
import { useHomepage, useProfile, useSocialLinks } from "@/hooks/usePortfolioQueries";

export function Footer() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const { data: profile } = useProfile();
  const { data: socialLinks } = useSocialLinks();
  const { data: homepage } = useHomepage();
  const year = new Date().getFullYear();
  // Falls back to the static translation only while the CMS value hasn't
  // loaded yet — the admin-managed homepage headline is the source of truth
  // (see /admin/homepage), not a value duplicated here.
  const tagline = homepage?.hero_headline || t("footer.tagline");

  return (
    <footer className="border-t border-ink/10 bg-paper-warm">
      <div className="container-editorial flex flex-col gap-8 py-12 sm:flex-row sm:items-end sm:justify-between">
        <div className="max-w-md">
          <p className="whitespace-pre-line font-serif text-xl text-ink">{tagline}</p>
          <p className="eyebrow mt-3">{t("footer.basedIn")}</p>
          {socialLinks && socialLinks.length > 0 ? (
            <div className="mt-4 flex items-center gap-4">
              {socialLinks.map((link) => (
                <a
                  key={link.label}
                  href={link.url}
                  target="_blank"
                  rel="noreferrer noopener"
                  aria-label={link.label}
                  className="text-ink-faint hover:text-ink"
                >
                  <SocialIcon name={link.icon} className="h-5 w-5" />
                </a>
              ))}
            </div>
          ) : null}
        </div>

        <div className="flex flex-col gap-3 text-sm text-ink-faint sm:items-end">
          {profile ? (
            <a href={`mailto:${profile.public_email}`} className="hover:text-ink">
              {profile.public_email}
            </a>
          ) : null}
          <NavLink to={localizedPath("/privacy")} className="hover:text-ink">
            {t("footer.privacy")}
          </NavLink>
          <p>
            © {year} {profile?.full_name ?? "Daniele Mario Areddu"}. {t("footer.rights")}
          </p>
        </div>
      </div>
    </footer>
  );
}
