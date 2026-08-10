import { useTranslation } from "react-i18next";

import { ErrorState, LoadingState } from "@/components/AsyncState";
import { usePassions } from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

export default function PassionsPage() {
  const { t } = useTranslation();
  const passions = usePassions();

  useSeo({
    title: "Beyond the work — Daniele Mario Areddu",
    description:
      "What drives Daniele Mario Areddu beyond engineering: AI beyond demos, international travel, aviation, geography and community.",
    path: "/passions",
    ready: passions.isSuccess || passions.isError,
  });

  if (passions.isLoading) return <LoadingState />;
  if (passions.isError || !passions.data)
    return <ErrorState onRetry={() => passions.refetch()} />;

  return (
    <div className="container-editorial py-16 sm:py-24">
      <h1 className="eyebrow">{t("passions.title")}</h1>

      <ul className="mt-10 grid grid-cols-1 gap-x-12 gap-y-14 sm:grid-cols-2">
        {passions.data.map((passion, index) => (
          <li key={passion.slug} className="border-t border-ink/15 pt-6">
            <span className="font-mono text-xs text-ink-faint">
              {String(index + 1).padStart(2, "0")}
            </span>
            <p className="mt-2 font-serif text-2xl text-ink">{passion.title}</p>
            <p className="mt-3 text-ink-soft">{passion.text}</p>
            {passion.motif_label ? (
              <p className="mt-4 font-mono text-xs uppercase tracking-wide text-cobalt">
                {passion.motif_label}
              </p>
            ) : null}
          </li>
        ))}
      </ul>
    </div>
  );
}
