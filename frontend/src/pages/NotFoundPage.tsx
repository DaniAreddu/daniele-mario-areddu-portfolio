import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { useSeo } from "@/hooks/useSeo";

export default function NotFoundPage() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();

  useSeo({
    title: "Page not found — Daniele Mario Areddu",
    description: "The page you're looking for doesn't exist or has moved.",
    path: "/404",
    noIndex: true,
  });

  return (
    <div className="container-editorial flex min-h-[60vh] flex-col items-center justify-center py-24 text-center">
      <p className="font-mono text-sm text-cobalt">404</p>
      <h1 className="mt-4 font-serif text-4xl text-ink sm:text-5xl">{t("notFound.title")}</h1>
      <p className="mt-4 max-w-md text-ink-soft">{t("notFound.body")}</p>
      <Link to={localizedPath("/")} className="btn-primary mt-8">
        {t("notFound.cta")}
      </Link>
    </div>
  );
}
