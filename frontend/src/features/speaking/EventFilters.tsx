import { Search, X } from "lucide-react";
import { useTranslation } from "react-i18next";

import type { EventFacets } from "@/types/api";
import type { EventFilterState } from "@/features/speaking/useEventFilterState";

const FORMAT_LABELS: Record<string, string> = {
  conference: "Conference",
  devfest: "DevFest",
  meetup: "Meetup",
  user_group: "User Group",
  lightning_talk: "Lightning Talk",
  community: "Community",
};

export function formatLabel(format: string): string {
  return FORMAT_LABELS[format] ?? format;
}

interface EventFiltersProps {
  facets: EventFacets | undefined;
  state: EventFilterState;
  onChange: (key: keyof EventFilterState, value: string | number | undefined) => void;
  onClear: () => void;
  hasActiveFilters: boolean;
  resultCount: number;
}

export function EventFilters({
  facets,
  state,
  onChange,
  onClear,
  hasActiveFilters,
  resultCount,
}: EventFiltersProps) {
  const { t } = useTranslation();

  return (
    <fieldset className="flex flex-wrap items-end gap-4">
      <legend className="sr-only">{t("speaking.title")}</legend>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-search" className="eyebrow">
          {t("speaking.filters.search")}
        </label>
        <div className="relative">
          <Search
            size={15}
            aria-hidden="true"
            className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 text-ink-faint"
          />
          <input
            id="filter-search"
            type="search"
            value={state.q ?? ""}
            onChange={(event) => onChange("q", event.target.value)}
            placeholder={t("speaking.filters.searchPlaceholder") ?? undefined}
            className="w-56 rounded-full border border-ink/15 bg-paper py-2 pl-9 pr-3 text-sm text-ink placeholder:text-ink-faint/70"
          />
        </div>
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-year" className="eyebrow">
          {t("speaking.filters.year")}
        </label>
        <select
          id="filter-year"
          value={state.year ?? ""}
          onChange={(event) => onChange("year", event.target.value || undefined)}
          className="rounded-full border border-ink/15 bg-paper px-3 py-2 text-sm text-ink"
        >
          <option value="">{t("speaking.filters.allYears")}</option>
          {facets?.years.map((year) => (
            <option key={year} value={year}>
              {year}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-continent" className="eyebrow">
          {t("speaking.filters.continent")}
        </label>
        <select
          id="filter-continent"
          value={state.continent ?? ""}
          onChange={(event) => onChange("continent", event.target.value || undefined)}
          className="rounded-full border border-ink/15 bg-paper px-3 py-2 text-sm text-ink"
        >
          <option value="">{t("speaking.filters.allContinents")}</option>
          {facets?.continents.map((continent) => (
            <option key={continent} value={continent}>
              {continent}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-country" className="eyebrow">
          {t("speaking.filters.country")}
        </label>
        <select
          id="filter-country"
          value={state.country ?? ""}
          onChange={(event) => onChange("country", event.target.value || undefined)}
          className="rounded-full border border-ink/15 bg-paper px-3 py-2 text-sm text-ink"
        >
          <option value="">{t("speaking.filters.allCountries")}</option>
          {facets?.countries.map((country) => (
            <option key={country} value={country}>
              {country}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-topic" className="eyebrow">
          {t("speaking.filters.topic")}
        </label>
        <select
          id="filter-topic"
          value={state.topic ?? ""}
          onChange={(event) => onChange("topic", event.target.value || undefined)}
          className="rounded-full border border-ink/15 bg-paper px-3 py-2 text-sm text-ink"
        >
          <option value="">{t("speaking.filters.allTopics")}</option>
          {facets?.topics.map((topic) => (
            <option key={topic} value={topic}>
              {topic}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-1.5">
        <label htmlFor="filter-format" className="eyebrow">
          {t("speaking.filters.format")}
        </label>
        <select
          id="filter-format"
          value={state.format ?? ""}
          onChange={(event) => onChange("format", event.target.value || undefined)}
          className="rounded-full border border-ink/15 bg-paper px-3 py-2 text-sm text-ink"
        >
          <option value="">{t("speaking.filters.allFormats")}</option>
          {facets?.formats.map((format) => (
            <option key={format} value={format}>
              {formatLabel(format)}
            </option>
          ))}
        </select>
      </div>

      {hasActiveFilters ? (
        <button
          type="button"
          onClick={onClear}
          className="inline-flex items-center gap-1 rounded-full px-3 py-2 text-sm text-ink-faint hover:text-ink"
        >
          <X size={14} aria-hidden="true" /> {t("speaking.filters.clear")}
        </button>
      ) : null}

      <p
        className="ml-auto self-center font-mono text-xs uppercase tracking-wide text-ink-faint"
        aria-live="polite"
      >
        {t("speaking.filters.resultsCount", { count: resultCount })}
      </p>
    </fieldset>
  );
}
