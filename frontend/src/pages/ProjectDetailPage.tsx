import { ArrowLeft, ArrowUpRight } from "lucide-react";
import { useTranslation } from "react-i18next";
import { Link, Navigate, useParams } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { LoadingState } from "@/components/AsyncState";
import { ApiError } from "@/services/apiClient";
import { useProject } from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

export default function ProjectDetailPage() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const { slug } = useParams<{ slug: string }>();
  const project = useProject(slug);

  useSeo({
    title: project.data
      ? `${project.data.title} — Daniele Mario Areddu`
      : "Project — Daniele Mario Areddu",
    description: project.data?.summary ?? "A backend and AI engineering case study.",
    path: `/projects/${slug ?? ""}`,
    ready: project.isSuccess || project.isError,
  });

  if (project.isLoading) return <LoadingState />;

  if (project.isError) {
    if (project.error instanceof ApiError && project.error.status === 404) {
      return <Navigate to={localizedPath("/projects")} replace />;
    }
    return (
      <div className="container-editorial py-24 text-center">
        <p className="font-serif text-2xl text-ink">{t("projects.notFoundTitle")}</p>
        <p className="mt-2 text-ink-soft">{t("projects.notFoundBody")}</p>
      </div>
    );
  }

  const data = project.data;
  if (!data) return null;

  const sections: [string, string][] = [
    [t("common.problem"), data.problem],
    [t("common.challenge"), data.challenge],
    [t("common.approach"), data.approach],
    [t("common.architecture"), data.architecture],
    [t("common.outcome"), data.outcome],
    [t("common.lessonsLearned"), data.lessons],
  ];

  return (
    <div className="container-editorial py-16 sm:py-24">
      <Link
        to={localizedPath("/projects")}
        className="inline-flex items-center gap-1 text-sm font-medium text-ink-faint hover:text-ink"
      >
        <ArrowLeft size={14} aria-hidden="true" /> {t("common.backToProjects")}
      </Link>

      <h1 className="mt-6 max-w-3xl text-balance font-serif text-4xl leading-tight text-ink sm:text-5xl">
        {data.title}
      </h1>
      <p className="mt-4 max-w-2xl text-lg text-ink-soft">{data.summary}</p>

      {data.external_url ? (
        <a
          href={data.external_url}
          target="_blank"
          rel="noreferrer noopener"
          className="btn-secondary mt-6 inline-flex"
        >
          {t("common.viewProject")} <ArrowUpRight size={14} aria-hidden="true" />
        </a>
      ) : null}

      <div className="mt-14 grid grid-cols-1 gap-12 lg:grid-cols-[2fr_1fr]">
        <div className="space-y-10">
          {sections.map(([label, text]) => (
            <section key={label}>
              <h2 className="eyebrow">{label}</h2>
              <p className="mt-3 max-w-2xl text-ink-soft">{text}</p>
            </section>
          ))}

          {data.key_decisions.length > 0 ? (
            <section>
              <h2 className="eyebrow">{t("common.keyDecisions")}</h2>
              <ul className="mt-3 max-w-2xl list-inside list-disc space-y-2 text-ink-soft">
                {data.key_decisions.map((decision) => (
                  <li key={decision}>{decision}</li>
                ))}
              </ul>
            </section>
          ) : null}
        </div>

        <aside className="space-y-8 border-t border-ink/10 pt-8 lg:border-l lg:border-t-0 lg:pl-8 lg:pt-0">
          <div>
            <h2 className="eyebrow">{t("common.technologies")}</h2>
            <ul className="mt-3 flex flex-wrap gap-2">
              {data.technologies.map((tech) => (
                <li
                  key={tech}
                  className="rounded-full border border-ink/15 px-3 py-1 text-xs text-ink-faint"
                >
                  {tech}
                </li>
              ))}
            </ul>
          </div>
          {data.related_skills.length > 0 ? (
            <div>
              <h2 className="eyebrow">{t("common.relatedSkills")}</h2>
              <ul className="mt-3 flex flex-wrap gap-2">
                {data.related_skills.map((skill) => (
                  <li
                    key={skill}
                    className="rounded-full border border-ink/15 px-3 py-1 text-xs text-ink-faint"
                  >
                    {skill}
                  </li>
                ))}
              </ul>
            </div>
          ) : null}
          <div className="rounded-2xl border border-ink/10 bg-paper-warm p-5">
            <h2 className="eyebrow">{t("common.confidentialityNote")}</h2>
            <p className="mt-2 text-sm text-ink-faint">{data.confidentiality_note}</p>
          </div>
        </aside>
      </div>
    </div>
  );
}
