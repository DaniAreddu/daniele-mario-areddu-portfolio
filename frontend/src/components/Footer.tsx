import { useTranslation } from "react-i18next";
import { NavLink } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { useProfile } from "@/hooks/usePortfolioQueries";

export function Footer() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const { data: profile } = useProfile();
  const year = new Date().getFullYear();

  return (
    <footer className="border-t border-ink/10 bg-paper-warm">
      <div className="container-editorial flex flex-col gap-8 py-12 sm:flex-row sm:items-end sm:justify-between">
        <div className="max-w-md">
          <p className="font-serif text-xl text-ink">{t("footer.tagline")}</p>
          <p className="eyebrow mt-3">{t("footer.basedIn")}</p>
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
            © {year} Daniele Mario Areddu. {t("footer.rights")}
          </p>
        </div>
      </div>
    </footer>
  );
}
