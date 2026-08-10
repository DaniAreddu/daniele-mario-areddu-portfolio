import { Check, Copy } from "lucide-react";
import { useState } from "react";

export function CopyButton({ text, label }: { text: string; label: string }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 2000);
    } catch {
      // Clipboard API may be unavailable (e.g. insecure context); fail silently.
    }
  };

  return (
    <button type="button" onClick={handleCopy} className="btn-secondary" aria-live="polite">
      {copied ? <Check size={16} aria-hidden="true" /> : <Copy size={16} aria-hidden="true" />}
      {label}
    </button>
  );
}
