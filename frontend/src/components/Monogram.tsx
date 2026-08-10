/** Sophisticated typographic placeholder used in place of a portrait, which
 * does not yet exist in the asset library. Designed to be swapped for a real
 * photograph later without touching layout (see docs/asset-requirements.md). */
export function Monogram({ className }: { className?: string }) {
  return (
    <div
      className={`flex aspect-[4/5] items-center justify-center overflow-hidden rounded-[2rem] border border-ink/10 bg-ink ${className ?? ""}`}
      role="img"
      aria-label="Monogram of Daniele Mario Areddu"
    >
      <span className="font-serif text-[7rem] leading-none tracking-tightest text-paper sm:text-[9rem]">
        DA
      </span>
    </div>
  );
}
