import { useTranslation } from "react-i18next";

import { ErrorState, LoadingState } from "@/components/AsyncState";
import { useExperiences } from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

function formatMonthYear(iso: string, locale: string): string {
  const date = new Date(iso);
  return date.toLocaleDateString(locale === "it" ? "it-IT" : "en-US", {
    month: "long",
    year: "numeric",
  });
}

export default function ExperiencePage() {
  const { t, i18n } = useTranslation();
  const experiences = useExperiences();

  useSeo({
    title: "Experience — Daniele Mario Areddu",
    description: "Professional backend and AI engineering experience of Daniele Mario Areddu.",
    path: "/experience",
    ready: experiences.isSuccess || experiences.isError,
  });

  if (experiences.isLoading) return <LoadingState />;
  if (experiences.isError || !experiences.data)
    return <ErrorState onRetry={() => experiences.refetch()} />;

  return (
    <div className="container-editorial py-16 sm:py-24">
      <h1 className="eyebrow">{t("experience.title")}</h1>

      <ul className="mt-10 space-y-14">
        {experiences.data.map((experience) => (
          <li key={experience.organization} className="border-t border-ink/10 pt-8">
            <div className="flex flex-wrap items-baseline justify-between gap-2">
              <div>
                <p className="font-serif text-2xl text-ink sm:text-3xl">{experience.role}</p>
                <p className="mt-1 text-lg text-ink-soft">{experience.organization}</p>
              </div>
              <p className="font-mono text-sm text-ink-faint">
                {formatMonthYear(experience.start_date, i18n.language)} –{" "}
                {experience.is_current
                  ? t("common.present")
                  : experience.end_date
                    ? formatMonthYear(experience.end_date, i18n.language)
                    : ""}
              </p>
            </div>
            <p className="mt-4 max-w-2xl text-ink-soft">{experience.summary}</p>
            {experience.highlights.length > 0 ? (
              <ul className="mt-4 max-w-2xl list-inside list-disc space-y-1 text-ink-soft">
                {experience.highlights.map((highlight) => (
                  <li key={highlight}>{highlight}</li>
                ))}
              </ul>
            ) : null}
            {experience.technologies.length > 0 ? (
              <ul className="mt-5 flex flex-wrap gap-2">
                {experience.technologies.map((tech) => (
                  <li
                    key={tech}
                    className="rounded-full border border-ink/15 px-3 py-1 text-xs text-ink-faint"
                  >
                    {tech}
                  </li>
                ))}
              </ul>
            ) : null}
          </li>
        ))}
      </ul>
    </div>
  );
}
