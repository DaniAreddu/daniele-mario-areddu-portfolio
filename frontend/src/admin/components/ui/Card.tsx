import { clsx } from "clsx";
import type { HTMLAttributes } from "react";

export function Card({ className, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={clsx("rounded-2xl border border-ink/10 bg-paper p-6 shadow-sm", className)}
      {...props}
    />
  );
}
