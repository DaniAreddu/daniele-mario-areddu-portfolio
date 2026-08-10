import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { ErrorState, LoadingState } from "@/components/AsyncState";
import { useProjects } from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

export default function ProjectsPage() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const projects = useProjects();

  useSeo({
    title: "Projects — Daniele Mario Areddu",
    description:
      "Selected backend and AI engineering case studies from Daniele Mario Areddu, with clear confidentiality boundaries.",
    path: "/projects",
    ready: projects.isSuccess || projects.isError,
  });

  if (projects.isLoading) return <LoadingState />;
  if (projects.isError || !projects.data)
    return <ErrorState onRetry={() => projects.refetch()} />;

  return (
    <div className="container-editorial py-16 sm:py-24">
      <h1 className="eyebrow">{t("projects.title")}</h1>

      <ul className="mt-10 divide-y divide-ink/10 border-t border-ink/10">
        {projects.data.map((project) => (
          <li key={project.slug}>
            <Link
              to={localizedPath(`/projects/${project.slug}`)}
              className="group grid grid-cols-1 gap-4 py-10 lg:grid-cols-[1fr_2fr]"
            >
              <div>
                {project.is_featured ? (
                  <p className="eyebrow text-cobalt">{t("projects.featured")}</p>
                ) : null}
                <p className="mt-2 font-serif text-2xl text-ink group-hover:text-cobalt sm:text-3xl">
                  {project.title}
                </p>
              </div>
              <div>
                <p className="max-w-2xl text-ink-soft">{project.summary}</p>
                <ul className="mt-4 flex flex-wrap gap-2">
                  {project.technologies.map((tech) => (
                    <li
                      key={tech}
                      className="rounded-full border border-ink/15 px-3 py-1 text-xs text-ink-faint"
                    >
                      {tech}
                    </li>
                  ))}
                </ul>
              </div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
