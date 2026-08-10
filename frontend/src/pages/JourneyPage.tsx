import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { ErrorState, LoadingState } from "@/components/AsyncState";
import { useJourney } from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

const KIND_LABELS: Record<string, string> = {
  education: "Education",
  project: "Project",
  community: "Community",
  speaking: "Speaking",
  experience: "Experience",
  focus: "Focus",
};

export default function JourneyPage() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const journey = useJourney();

  useSeo({
    title: "Journey — Daniele Mario Areddu",
    description:
      "An editorial timeline connecting education, backend and AI engineering work, community building and international speaking.",
    path: "/journey",
    ready: journey.isSuccess || journey.isError,
  });

  if (journey.isLoading) return <LoadingState />;
  if (journey.isError || !journey.data) return <ErrorState onRetry={() => journey.refetch()} />;

  return (
    <div className="container-editorial py-16 sm:py-24">
      <h1 className="eyebrow">{t("journey.title")}</h1>
      <p className="mt-4 max-w-2xl font-serif text-2xl text-ink sm:text-3xl">
        {t("journey.intro")}
      </p>

      <ol className="relative mt-14 space-y-12 border-l border-ink/15 pl-8 sm:pl-12">
        {journey.data.map((milestone, index) => (
          <li key={index} className="relative">
            <span
              aria-hidden="true"
              className="absolute -left-[2.05rem] top-1 h-3 w-3 rounded-full border-2 border-paper bg-cobalt sm:-left-[3.05rem]"
            />
            <div className="flex flex-wrap items-baseline gap-3">
              {milestone.year ? (
                <span className="font-mono text-sm text-cobalt">{milestone.year}</span>
              ) : null}
              <span className="eyebrow">{KIND_LABELS[milestone.kind] ?? milestone.kind}</span>
            </div>
            <p className="mt-2 font-serif text-2xl text-ink">{milestone.title}</p>
            <p className="mt-2 max-w-2xl text-ink-soft">{milestone.text}</p>
            {milestone.event_slug ? (
              <Link
                to={`${localizedPath("/speaking")}?event=${milestone.event_slug}`}
                className="mt-3 inline-block text-sm font-medium text-ink underline decoration-ink/30 underline-offset-4 hover:decoration-ink"
              >
                {t("journey.highlightOnMap")} →
              </Link>
            ) : null}
          </li>
        ))}
      </ol>
    </div>
  );
}
