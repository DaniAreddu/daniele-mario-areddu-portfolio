import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "@/i18n/locales/en.json";
import it from "@/i18n/locales/it.json";

export const SUPPORTED_LOCALES = ["en", "it"] as const;
export type Locale = (typeof SUPPORTED_LOCALES)[number];
export const DEFAULT_LOCALE: Locale = "en";
export const LOCALE_STORAGE_KEY = "areddu_locale";

void i18n.use(initReactI18next).init({
  resources: { en: { translation: en }, it: { translation: it } },
  lng: DEFAULT_LOCALE,
  fallbackLng: DEFAULT_LOCALE,
  interpolation: { escapeValue: false },
  returnEmptyString: false,
});

export default i18n;
