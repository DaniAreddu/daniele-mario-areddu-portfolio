import { clsx } from "clsx";
import { forwardRef, type InputHTMLAttributes } from "react";

export const Input = forwardRef<HTMLInputElement, InputHTMLAttributes<HTMLInputElement>>(
  function Input({ className, ...props }, ref) {
    return (
      <input
        ref={ref}
        className={clsx(
          "w-full rounded-lg border border-ink/15 bg-paper px-3 py-2 text-sm text-ink",
          "placeholder:text-ink-faint",
          "focus:border-cobalt focus:outline-none focus:ring-1 focus:ring-cobalt",
          "aria-[invalid=true]:border-red-400",
          className,
        )}
        {...props}
      />
    );
  },
);
