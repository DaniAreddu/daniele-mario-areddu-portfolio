import { createContext, useContext, useEffect, useMemo, useRef, type ReactNode } from "react";
import { useLocation, useNavigate } from "react-router-dom";

import { DEFAULT_LOCALE, LOCALE_STORAGE_KEY, type Locale } from "@/i18n";
import i18n from "@/i18n";

interface LocaleContextValue {
  locale: Locale;
  /** Builds the path for `targetPath` (an unprefixed, English-style path
   * such as "/about" or "/") under the given locale. */
  localizedPath: (targetPath: string, targetLocale?: Locale) => string;
}

const LocaleContext = createContext<LocaleContextValue | null>(null);

function localeFromPathname(pathname: string): Locale {
  return pathname === "/it" || pathname.startsWith("/it/") ? "it" : DEFAULT_LOCALE;
}

export function localizedPathFor(targetPath: string, targetLocale: Locale): string {
  const normalized = targetPath === "/" ? "" : targetPath;
  return targetLocale === "it" ? `/it${normalized}` : normalized || "/";
}

export function LocaleProvider({ children }: { children: ReactNode }) {
  const location = useLocation();
  const navigate = useNavigate();
  const locale = localeFromPathname(location.pathname);
  const checkedInitialRedirect = useRef(false);

  // Honor a previously chosen language only on a bare, unprefixed landing at
  // "/". Direct links to a specific locale (e.g. shared "/about") always win.
  useEffect(() => {
    if (checkedInitialRedirect.current) return;
    checkedInitialRedirect.current = true;
    if (location.pathname !== "/") return;
    try {
      const stored = window.localStorage.getItem(LOCALE_STORAGE_KEY);
      if (stored === "it") navigate("/it", { replace: true });
    } catch {
      // Storage unavailable: fall back to the default English landing page.
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    void i18n.changeLanguage(locale);
    document.documentElement.lang = locale;
  }, [locale]);

  useEffect(() => {
    try {
      window.localStorage.setItem(LOCALE_STORAGE_KEY, locale);
    } catch {
      // Storage can be unavailable (private browsing, disabled cookies); locale
      // still works for the current session via the URL.
    }
  }, [locale]);

  const value = useMemo<LocaleContextValue>(
    () => ({
      locale,
      localizedPath: (targetPath, targetLocale) =>
        localizedPathFor(targetPath, targetLocale ?? locale),
    }),
    [locale],
  );

  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function useLocale(): LocaleContextValue {
  const context = useContext(LocaleContext);
  if (!context) throw new Error("useLocale must be used within LocaleProvider");
  return context;
}
