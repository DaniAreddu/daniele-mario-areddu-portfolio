import { useTranslation } from "react-i18next";
import { useLocation, useNavigate } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { SUPPORTED_LOCALES, type Locale } from "@/i18n";

/** Maps the current pathname (in the active locale) to its English-canonical,
 * unprefixed equivalent, so we can rebuild the path for the target locale. */
function toCanonicalPath(pathname: string, locale: Locale): string {
  if (locale !== "it") return pathname;
  const withoutPrefix = pathname.replace(/^\/it/, "");
  return withoutPrefix === "" ? "/" : withoutPrefix;
}

export function LanguageSwitcher() {
  const { t } = useTranslation();
  const { locale, localizedPath } = useLocale();
  const location = useLocation();
  const navigate = useNavigate();

  const canonicalPath = toCanonicalPath(location.pathname, locale);

  return (
    <div
      role="group"
      aria-label={t("language.label")}
      className="flex items-center gap-1 text-sm"
    >
      {SUPPORTED_LOCALES.map((code) => (
        <button
          key={code}
          type="button"
          aria-current={locale === code ? "true" : undefined}
          onClick={() => navigate(localizedPath(canonicalPath, code) + location.search)}
          className={`rounded-full px-2.5 py-1 font-mono text-xs uppercase tracking-wide transition-colors ${
            locale === code
              ? "bg-ink text-paper"
              : "text-ink-faint hover:bg-ink/5 hover:text-ink"
          }`}
        >
          {code}
        </button>
      ))}
    </div>
  );
}
