import { useTranslation } from "react-i18next";

/** Renders nothing for a completed (past) engagement — badges are reserved
 * for the distinction that actually matters to a visitor: whether something
 * hasn't happened yet. The status is always conveyed as text, never by
 * color alone. */
export function StatusBadge({ status }: { status: string }) {
  const { t } = useTranslation();

  if (status === "upcoming") {
    return (
      <span className="rounded-full border border-cobalt/40 bg-cobalt/10 px-2 py-0.5 font-mono text-[0.65rem] uppercase tracking-wide text-cobalt">
        {t("speaking.upcoming.upcoming")}
      </span>
    );
  }

  if (status === "incoming") {
    return (
      <span className="rounded-full border border-ink/25 bg-ink/5 px-2 py-0.5 font-mono text-[0.65rem] uppercase tracking-wide text-ink-soft">
        {t("speaking.upcoming.incoming")}
      </span>
    );
  }

  return null;
}
