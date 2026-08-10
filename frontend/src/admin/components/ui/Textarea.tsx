import { clsx } from "clsx";
import { forwardRef, type TextareaHTMLAttributes } from "react";

export const Textarea = forwardRef<
  HTMLTextAreaElement,
  TextareaHTMLAttributes<HTMLTextAreaElement>
>(function Textarea({ className, ...props }, ref) {
  return (
    <textarea
      ref={ref}
      className={clsx(
        "w-full rounded-lg border border-ink/15 bg-paper px-3 py-2 text-sm text-ink",
        "placeholder:text-ink-faint",
        "focus:border-cobalt focus:outline-none focus:ring-1 focus:ring-cobalt",
        className,
      )}
      {...props}
    />
  );
});
