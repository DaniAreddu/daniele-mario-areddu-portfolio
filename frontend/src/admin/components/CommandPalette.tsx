import { Command } from "cmdk";
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAdminSearch } from "@/admin/hooks/useAdminDashboard";

export function CommandPalette() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const navigate = useNavigate();
  const { data: results, isFetching } = useAdminSearch(query);

  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if ((event.metaKey || event.ctrlKey) && event.key === "k") {
        event.preventDefault();
        setOpen((current) => !current);
      }
    }
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, []);

  function goTo(path: string) {
    setOpen(false);
    setQuery("");
    navigate(path);
  }

  return (
    <Command.Dialog
      open={open}
      onOpenChange={setOpen}
      label="Global search"
      className="fixed left-1/2 top-24 z-50 w-full max-w-lg -translate-x-1/2 overflow-hidden rounded-2xl border border-ink/10 bg-paper shadow-xl"
    >
      <Command.Input
        value={query}
        onValueChange={setQuery}
        placeholder="Search content… (Ctrl/Cmd+K)"
        className="w-full border-b border-ink/10 bg-transparent px-4 py-3 text-sm text-ink outline-none placeholder:text-ink-faint"
      />
      <Command.List className="max-h-80 overflow-y-auto p-2">
        {isFetching ? (
          <p className="px-3 py-4 text-sm text-ink-faint">Searching…</p>
        ) : (
          <Command.Empty className="px-3 py-4 text-sm text-ink-faint">
            {query.trim().length < 2 ? "Type at least 2 characters." : "No results."}
          </Command.Empty>
        )}
        {(results ?? []).map((result) => (
          <Command.Item
            key={`${result.entity_type}-${result.entity_id}`}
            value={`${result.entity_type}-${result.entity_id}-${result.title}`}
            onSelect={() => goTo(result.admin_path)}
            className="cursor-pointer rounded-lg px-3 py-2 text-sm text-ink data-[selected=true]:bg-paper-warm"
          >
            <span className="font-mono text-xs uppercase tracking-wide text-ink-faint">
              {result.entity_type.replace(/_/g, " ")}
            </span>
            <span className="ml-2">{result.title}</span>
          </Command.Item>
        ))}
      </Command.List>
    </Command.Dialog>
  );
}
