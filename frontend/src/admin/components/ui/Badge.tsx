import { clsx } from "clsx";
import type { HTMLAttributes } from "react";

interface BadgeProps extends HTMLAttributes<HTMLSpanElement> {
  tone?: "neutral" | "cobalt" | "success" | "warning" | "danger";
}

const TONE_CLASSES: Record<NonNullable<BadgeProps["tone"]>, string> = {
  neutral: "border-ink/15 text-ink-soft",
  cobalt: "border-cobalt/40 text-cobalt",
  success: "border-emerald-400/50 text-emerald-700",
  warning: "border-amber-400/50 text-amber-700",
  danger: "border-red-400/50 text-red-700",
};

export function Badge({ tone = "neutral", className, ...props }: BadgeProps) {
  return (
    <span
      className={clsx(
        "inline-flex items-center rounded-full border px-2 py-0.5 font-mono text-[11px] uppercase tracking-wide",
        TONE_CLASSES[tone],
        className,
      )}
      {...props}
    />
  );
}
