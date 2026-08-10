import { ArrowUpRight } from "lucide-react";
import { Fragment } from "react";
import { useTranslation } from "react-i18next";
import { Link } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { ErrorState, LoadingState } from "@/components/AsyncState";
import { Monogram } from "@/components/Monogram";
import { RouteMotif } from "@/components/RouteMotif";
import {
  useBiography,
  useCommunity,
  useEvents,
  useEventStats,
  useHomepage,
  useJourney,
  useProfile,
} from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

// Applied only if the CMS homepage settings haven't set an order yet (a
// brand-new, never-configured singleton) — the admin-configured
// `section_order` is otherwise always authoritative.
const DEFAULT_SECTION_ORDER = ["about", "journey", "speaking", "projects", "community"];

export default function HomePage() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const profile = useProfile();
  const biography = useBiography();
  const journey = useJourney();
  const homepage = useHomepage();
  const community = useCommunity();
  const eventStats = useEventStats();
  const events = useEvents();

  useSeo({
    title: "Daniele Mario Areddu — Backend & AI Developer and International Speaker",
    description:
      "Portfolio of Daniele Mario Areddu, Backend & AI Developer, international technology speaker, Computer Science student, and Founder of Velletri.dev.",
    path: "/",
    ready: (profile.isSuccess && homepage.isSuccess) || profile.isError || homepage.isError,
    jsonLd: profile.data
      ? {
          "@context": "https://schema.org",
          "@type": "Person",
          name: profile.data.full_name,
          jobTitle: profile.data.roles[0],
          email: `mailto:${profile.data.public_email}`,
          address: { "@type": "PostalAddress", addressCountry: "IT" },
          knowsAbout: ["Backend engineering", "Artificial intelligence", "Python", "FastAPI"],
        }
      : undefined,
  });

  if (profile.isLoading || homepage.isLoading) return <LoadingState />;
  if (profile.isError || homepage.isError || !profile.data || !homepage.data) {
    return (
      <ErrorState
        onRetry={() => {
          void profile.refetch();
          void homepage.refetch();
        }}
      />
    );
  }

  const data = profile.data;
  const hero = homepage.data;
  const featuredProjects = hero.features.filter((feature) => feature.entity_type === "project");
  const featuredEvents = hero.features.filter((feature) => feature.entity_type === "event");
  const journeyPreview = journey.data?.slice(0, 4) ?? [];
  const sectionOrder =
    hero.section_order.length > 0 ? hero.section_order : DEFAULT_SECTION_ORDER;
  const isSectionVisible = (key: string) => hero.section_visibility[key] !== false;

  const sortedEvents = [...(events.data ?? [])].sort(
    (a, b) => a.year - b.year || (a.month ?? 99) - (b.month ?? 99),
  );
  const milestoneCities = [
    ...new Set(
      sortedEvents
        .filter((event) => event.is_international_milestone)
        .map((event) => event.city),
    ),
  ].filter((city): city is string => Boolean(city));
  const nextStopCities = [
    ...new Set(
      sortedEvents
        .filter((event) => event.status === "upcoming" || event.status === "incoming")
        .map((event) => event.city),
    ),
  ].filter((city): city is string => Boolean(city));

  const optionalSections: Record<string, JSX.Element | null> = {
    about: (
      <section className="border-t border-ink/10 bg-paper-warm py-20">
        <div className="container-editorial grid grid-cols-1 gap-10 lg:grid-cols-[0.4fr_0.6fr]">
          <p className="eyebrow">{t("home.sectionAbout")}</p>
          <div>
            {biography.data ? (
              <p className="text-balance font-serif text-2xl leading-snug text-ink sm:text-3xl">
                {biography.data.short}
              </p>
            ) : (
              <LoadingState />
            )}
            <Link
              to={localizedPath("/about")}
              className="mt-6 inline-flex items-center gap-1 text-sm font-medium text-ink underline decoration-ink/30 underline-offset-4 hover:decoration-ink"
            >
              {t("home.viewFullBio")} <ArrowUpRight size={14} aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>
    ),
    journey:
      journeyPreview.length > 0 ? (
        <section className="py-20">
          <div className="container-editorial">
            <div className="flex items-baseline justify-between">
              <p className="eyebrow">{t("home.sectionJourney")}</p>
              <Link
                to={localizedPath("/journey")}
                className="text-sm font-medium text-ink-faint hover:text-ink"
              >
                {t("common.followJourney")} →
              </Link>
            </div>
            <ol className="mt-8 grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4">
              {journeyPreview.map((milestone, index) => (
                <li key={index} className="border-t border-ink/15 pt-4">
                  {milestone.year ? (
                    <p className="font-mono text-xs text-cobalt">{milestone.year}</p>
                  ) : null}
                  <p className="mt-1 font-serif text-lg text-ink">{milestone.title}</p>
                  <p className="mt-2 text-sm text-ink-faint">{milestone.text}</p>
                </li>
              ))}
            </ol>
          </div>
        </section>
      ) : null,
    speaking:
      featuredEvents.length > 0 || eventStats.data ? (
        <section className="border-t border-ink/10 bg-ink py-20 text-paper">
          <div className="container-editorial">
            <div className="flex flex-wrap items-baseline justify-between gap-4">
              <p className="eyebrow text-paper/60">{t("home.sectionSpeaking")}</p>
              <Link
                to={localizedPath("/speaking")}
                className="text-sm font-medium text-paper/80 hover:text-paper"
              >
                {t("common.viewSpeakingMap")} →
              </Link>
            </div>

            {eventStats.data ? (
              <div className="mt-6 max-w-2xl">
                <p className="font-serif text-2xl leading-snug sm:text-3xl">
                  {t("home.internationalSpeaker.headline", {
                    count: eventStats.data.total_events,
                  })}
                </p>
                <p className="mt-2 font-mono text-xs uppercase tracking-wide text-paper/50">
                  {data.speaking_regions_label}
                </p>
                {milestoneCities.length > 0 ? (
                  <p className="mt-4 text-sm text-paper/70">{milestoneCities.join(" · ")}</p>
                ) : null}
              </div>
            ) : null}

            {nextStopCities.length > 0 ? (
              <div className="mt-8 border-t border-paper/15 pt-4">
                <p className="eyebrow text-paper/50">{t("speaking.upcoming.title")}</p>
                <p className="mt-2 font-serif text-lg text-paper">
                  {nextStopCities.join(" · ")}
                </p>
              </div>
            ) : null}

            {featuredEvents.length > 0 ? (
              <ul className="mt-10 grid grid-cols-1 gap-8 border-t border-paper/15 pt-8 lg:grid-cols-3">
                {featuredEvents.map((feature) => (
                  <li key={feature.url_path} className="border-t border-paper/15 pt-4">
                    <Link
                      to={localizedPath(feature.url_path)}
                      className="font-serif text-xl leading-snug hover:underline"
                    >
                      {feature.title}
                    </Link>
                    {feature.summary ? (
                      <p className="mt-2 text-sm text-paper/70">{feature.summary}</p>
                    ) : null}
                  </li>
                ))}
              </ul>
            ) : null}
          </div>
        </section>
      ) : null,
    projects:
      featuredProjects.length > 0 ? (
        <section className="py-20">
          <div className="container-editorial">
            <div className="flex items-baseline justify-between">
              <p className="eyebrow">{t("home.sectionProjects")}</p>
              <Link
                to={localizedPath("/projects")}
                className="text-sm font-medium text-ink-faint hover:text-ink"
              >
                {t("home.viewAllProjects")} →
              </Link>
            </div>
            <div className="mt-8 grid grid-cols-1 gap-10 lg:grid-cols-2">
              {featuredProjects.map((feature) => (
                <Link
                  key={feature.url_path}
                  to={localizedPath(feature.url_path)}
                  className="group border-t border-ink/15 pt-5"
                >
                  <p className="font-serif text-2xl text-ink group-hover:text-cobalt">
                    {feature.title}
                  </p>
                  <p className="mt-3 text-ink-soft">{feature.summary}</p>
                  <p className="mt-4 text-sm font-medium text-ink underline decoration-ink/30 underline-offset-4">
                    {t("common.viewProject")}
                  </p>
                </Link>
              ))}
            </div>
          </div>
        </section>
      ) : null,
    community: community.data ? (
      <section className="border-t border-ink/10 bg-paper-warm py-20">
        <div className="container-editorial grid grid-cols-1 gap-10 lg:grid-cols-[0.4fr_0.6fr]">
          <p className="eyebrow">{t("home.sectionCommunity")}</p>
          <div>
            <p className="font-serif text-2xl text-ink sm:text-3xl">{community.data.name}</p>
            <p className="mt-3 max-w-2xl text-ink-soft">{community.data.mission}</p>
            <Link
              to={localizedPath("/community")}
              className="mt-6 inline-flex items-center gap-1 text-sm font-medium text-ink underline decoration-ink/30 underline-offset-4 hover:decoration-ink"
            >
              {t("common.readMore")} <ArrowUpRight size={14} aria-hidden="true" />
            </Link>
          </div>
        </div>
      </section>
    ) : null,
  };

  return (
    <>
      {/* Hero */}
      <section className="container-editorial grid grid-cols-1 gap-12 py-16 sm:py-24 lg:grid-cols-[1.2fr_0.8fr] lg:gap-16">
        <div className="animate-fade-up">
          <p className="eyebrow">{hero.hero_eyebrow}</p>
          <h1 className="mt-5 whitespace-pre-line text-balance font-serif text-4xl leading-[1.05] tracking-tightest text-ink sm:text-6xl lg:text-7xl">
            {hero.hero_headline}
          </h1>
          <p className="mt-6 max-w-xl text-lg text-ink-soft">{hero.hero_subheadline}</p>

          <dl className="mt-6 flex flex-wrap gap-x-6 gap-y-2 font-mono text-xs uppercase tracking-wide text-ink-faint">
            <div className="flex items-center gap-1.5">
              <dt className="sr-only">Base</dt>
              <dd>{t("home.basedIn")}</dd>
            </div>
            <div className="flex items-center gap-1.5">
              <dt className="sr-only">Availability</dt>
              <dd>{t("home.availableFor")}</dd>
            </div>
          </dl>

          <div className="mt-10 flex flex-wrap gap-3">
            {hero.primary_cta_label && hero.primary_cta_url ? (
              <Link to={localizedPath(hero.primary_cta_url)} className="btn-primary">
                {hero.primary_cta_label} <ArrowUpRight size={16} aria-hidden="true" />
              </Link>
            ) : null}
            {hero.secondary_cta_label && hero.secondary_cta_url ? (
              <Link to={localizedPath(hero.secondary_cta_url)} className="btn-secondary">
                {hero.secondary_cta_label}
              </Link>
            ) : null}
          </div>

          <ul className="mt-14 grid max-w-xl grid-cols-3 gap-6 border-t border-ink/10 pt-6">
            <li>
              <p className="font-serif text-2xl text-ink">{data.talks_count_label}</p>
              <p className="mt-1 text-xs text-ink-faint">{t("home.credibilityTalks")}</p>
            </li>
            <li>
              <p className="font-serif text-2xl text-ink">{data.speaking_years_label}</p>
              <p className="mt-1 text-xs text-ink-faint">{t("home.credibilityYears")}</p>
            </li>
            <li>
              <p className="font-serif text-sm leading-tight text-ink">
                {data.speaking_regions_label}
              </p>
              <p className="mt-1 text-xs text-ink-faint">{t("home.credibilityRegions")}</p>
            </li>
          </ul>
        </div>

        <div className="relative flex flex-col gap-4">
          <Monogram />
          <RouteMotif className="h-28 w-full text-ink-faint" />
        </div>
      </section>

      {sectionOrder.map((key) => (
        <Fragment key={key}>{isSectionVisible(key) ? optionalSections[key] : null}</Fragment>
      ))}

      {/* Contact CTA */}
      <section className="py-24">
        <div className="container-editorial text-center">
          <p className="text-balance font-serif text-3xl text-ink sm:text-5xl">
            {t("contact.title")}
          </p>
          <div className="mt-8 flex flex-wrap justify-center gap-3">
            <Link to={localizedPath("/contact")} className="btn-primary">
              {t("common.inviteToSpeak")}
            </Link>
            <Link to={localizedPath("/contact")} className="btn-secondary">
              {t("common.letsCollaborate")}
            </Link>
          </div>
        </div>
      </section>
    </>
  );
}
