import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { ErrorState, LoadingState } from "@/components/AsyncState";
import { CopyButton } from "@/components/CopyButton";
import {
  useBiography,
  useEducation,
  useExperiences,
  useSkills,
} from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

export default function AboutPage() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const biography = useBiography();
  const education = useEducation();
  const experiences = useExperiences();
  const skills = useSkills();

  useSeo({
    title: "About — Daniele Mario Areddu",
    description:
      "Backend engineering, applied AI, international speaking and community building — the full biography of Daniele Mario Areddu.",
    path: "/about",
    ready: biography.isSuccess || biography.isError,
  });

  if (biography.isLoading) return <LoadingState />;
  if (biography.isError || !biography.data)
    return <ErrorState onRetry={() => biography.refetch()} />;

  return (
    <div className="container-editorial py-16 sm:py-24">
      <h1 className="eyebrow">{t("about.title")}</h1>
      <div className="mt-6 max-w-3xl space-y-6 font-serif text-xl leading-relaxed text-ink sm:text-2xl">
        {biography.data.long.split("\n\n").map((paragraph, index) => (
          <p key={index}>{paragraph}</p>
        ))}
      </div>

      {/* Education */}
      <section className="mt-20 border-t border-ink/10 pt-10">
        <h2 className="eyebrow">{t("about.educationTitle")}</h2>
        {education.data ? (
          <ul className="mt-6 space-y-8">
            {education.data.map((item) => (
              <li
                key={item.institution}
                className="grid grid-cols-1 gap-2 sm:grid-cols-[8rem_1fr]"
              >
                <p className="font-mono text-sm text-ink-faint">
                  {item.start_year ?? ""}
                  {item.start_year ? "–" : ""}
                  {item.is_ongoing ? t("common.present") : (item.end_year ?? "")}
                </p>
                <div>
                  <p className="font-serif text-xl text-ink">{item.institution}</p>
                  <p className="text-ink-soft">{item.degree}</p>
                  {item.description ? (
                    <p className="mt-1 text-sm text-ink-faint">{item.description}</p>
                  ) : null}
                </div>
              </li>
            ))}
          </ul>
        ) : (
          <LoadingState />
        )}
      </section>

      {/* Experience summary */}
      <section className="mt-16 border-t border-ink/10 pt-10">
        <div className="flex items-baseline justify-between">
          <h2 className="eyebrow">{t("about.experienceTitle")}</h2>
          <Link
            to={localizedPath("/experience")}
            className="text-sm font-medium text-ink-faint hover:text-ink"
          >
            {t("common.readMore")} →
          </Link>
        </div>
        {experiences.data?.[0] ? (
          <div className="mt-6">
            <p className="font-serif text-xl text-ink">{experiences.data[0].role}</p>
            <p className="text-ink-soft">{experiences.data[0].organization}</p>
            <p className="mt-3 max-w-2xl text-ink-faint">{experiences.data[0].summary}</p>
          </div>
        ) : null}
      </section>

      {/* Skills */}
      <section className="mt-16 border-t border-ink/10 pt-10">
        <h2 className="eyebrow">{t("about.skillsTitle")}</h2>
        {skills.data ? (
          <div className="mt-6 grid grid-cols-1 gap-10 sm:grid-cols-2">
            {skills.data.map((category) => (
              <div key={category.slug}>
                <p className="font-serif text-lg text-ink">{category.name}</p>
                <ul className="mt-3 flex flex-wrap gap-2">
                  {category.skills.map((skill) => (
                    <li
                      key={skill.name}
                      title={skill.context ?? undefined}
                      className="rounded-full border border-ink/15 px-3 py-1 text-sm text-ink-soft"
                    >
                      {skill.name}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        ) : (
          <LoadingState />
        )}
      </section>

      {/* Speaker bio */}
      <section className="mt-16 border-t border-ink/10 pt-10">
        <h2 className="eyebrow">{t("about.speakerBioTitle")}</h2>
        <p className="mt-6 max-w-2xl text-ink-soft">{biography.data.speaker_bio}</p>
        <div className="mt-6">
          <CopyButton text={biography.data.speaker_bio} label={t("about.copyBio")} />
        </div>
      </section>

      {/* Speaker kit (hidden/unavailable until real assets exist) */}
      <section className="mt-16 border-t border-ink/10 pt-10">
        <h2 className="eyebrow">{t("about.speakerKitTitle")}</h2>
        <p className="mt-4 max-w-xl text-sm text-ink-faint">
          {t("about.speakerKitUnavailable")}
        </p>
      </section>
    </div>
  );
}
