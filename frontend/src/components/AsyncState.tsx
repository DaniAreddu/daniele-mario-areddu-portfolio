import { useTranslation } from "react-i18next";

export function LoadingState({ label }: { label?: string }) {
  const { t } = useTranslation();
  return (
    <div role="status" aria-live="polite" className="py-16 text-center">
      <span className="eyebrow">{label ?? t("common.loading")}</span>
    </div>
  );
}

export function ErrorState({ onRetry }: { onRetry?: () => void }) {
  const { t } = useTranslation();
  return (
    <div
      role="alert"
      className="rounded-2xl border border-ink/10 bg-paper-warm px-6 py-10 text-center"
    >
      <p className="text-ink-soft">{t("common.loadingError")}</p>
      {onRetry ? (
        <button type="button" onClick={onRetry} className="btn-secondary mt-4">
          {t("common.retry")}
        </button>
      ) : null}
    </div>
  );
}
