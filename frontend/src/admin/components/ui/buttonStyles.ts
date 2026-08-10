import { clsx } from "clsx";

export type ButtonVariant = "primary" | "secondary" | "danger";

export function buttonClassName(variant: ButtonVariant = "primary", className?: string) {
  return clsx(
    "inline-flex items-center justify-center gap-2 rounded-lg px-4 py-2 text-sm font-medium transition-colors",
    "disabled:cursor-not-allowed disabled:opacity-50",
    "focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-cobalt",
    variant === "primary" && "bg-ink text-paper hover:bg-cobalt",
    variant === "secondary" &&
      "border border-ink/15 bg-transparent text-ink hover:bg-paper-warm",
    variant === "danger" && "bg-red-600 text-white hover:bg-red-700",
    className,
  );
}
