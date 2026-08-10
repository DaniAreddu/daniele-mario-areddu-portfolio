import { useTranslation } from "react-i18next";

import { ErrorState, LoadingState } from "@/components/AsyncState";
import { useCommunity } from "@/hooks/usePortfolioQueries";
import { useSeo } from "@/hooks/useSeo";

function formatDate(iso: string, locale: string): string {
  return new Date(iso).toLocaleDateString(locale === "it" ? "it-IT" : "en-US", {
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}

export default function CommunityPage() {
  const { t, i18n } = useTranslation();
  const community = useCommunity();

  useSeo({
    title: "Community — Velletri.dev",
    description:
      "Velletri.dev is a developer community founded by Daniele Mario Areddu, connecting local talent with the international tech ecosystem.",
    path: "/community",
    ready: community.isSuccess || community.isError,
  });

  if (community.isLoading) return <LoadingState />;
  if (community.isError || !community.data)
    return <ErrorState onRetry={() => community.refetch()} />;

  const data = community.data;

  return (
    <div className="container-editorial py-16 sm:py-24">
      <p className="eyebrow">{t("community.title")}</p>
      <h1 className="mt-4 text-balance font-serif text-4xl leading-tight text-ink sm:text-5xl">
        {data.name}
      </h1>
      <p className="mt-2 text-lg text-ink-soft">
        {data.role} · {t("common.present")} {data.founded_year}
      </p>

      <div className="mt-10 grid grid-cols-1 gap-10 lg:grid-cols-2">
        <div>
          <h2 className="eyebrow">Mission</h2>
          <p className="mt-3 text-ink-soft">{data.mission}</p>
        </div>
        <div>
          <h2 className="eyebrow">Vision</h2>
          <p className="mt-3 text-ink-soft">{data.vision}</p>
        </div>
      </div>

      <div className="mt-10 max-w-3xl border-t border-ink/10 pt-8">
        <p className="font-serif text-xl leading-relaxed text-ink">{data.description}</p>
      </div>

      {data.activities.length > 0 ? (
        <section className="mt-16 border-t border-ink/10 pt-10">
          <h2 className="eyebrow">{t("community.activitiesTitle")}</h2>
          <ul className="mt-6 space-y-6">
            {data.activities.map((activity) => (
              <li
                key={activity.slug}
                className="grid grid-cols-1 gap-2 sm:grid-cols-[10rem_1fr]"
              >
                <p className="font-mono text-xs text-ink-faint">
                  {activity.activity_date
                    ? formatDate(activity.activity_date, i18n.language)
                    : ""}
                </p>
                <div>
                  <p className="font-serif text-lg text-ink">{activity.title}</p>
                  <p className="mt-1 text-sm text-ink-soft">{activity.description}</p>
                </div>
              </li>
            ))}
          </ul>
        </section>
      ) : null}

      <section className="mt-16 rounded-2xl border border-ink/10 bg-paper-warm p-8">
        <h2 className="font-serif text-xl text-ink">{t("community.collaborateTitle")}</h2>
        <p className="mt-3 max-w-2xl text-ink-soft">{data.collaboration}</p>
        {data.website_url ? (
          <a
            href={data.website_url}
            target="_blank"
            rel="noreferrer noopener"
            className="btn-secondary mt-5 inline-flex"
          >
            velletri.dev
          </a>
        ) : null}
      </section>
    </div>
  );
}
