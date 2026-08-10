import { clsx } from "clsx";
import { forwardRef, type SelectHTMLAttributes } from "react";

export const Select = forwardRef<HTMLSelectElement, SelectHTMLAttributes<HTMLSelectElement>>(
  function Select({ className, ...props }, ref) {
    return (
      <select
        ref={ref}
        className={clsx(
          "w-full rounded-lg border border-ink/15 bg-paper px-3 py-2 text-sm text-ink",
          "focus:border-cobalt focus:outline-none focus:ring-1 focus:ring-cobalt",
          className,
        )}
        {...props}
      />
    );
  },
);
