import { useState } from "react";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { ConfirmDialog } from "@/admin/components/ui/ConfirmDialog";
import { Input } from "@/admin/components/ui/Input";
import { Select } from "@/admin/components/ui/Select";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminNavigationList,
  useCreateNavigationItem,
  useDeleteNavigationItem,
  useUpdateNavigationItem,
} from "@/admin/hooks/useAdminNavigation";
import type { NavigationItemAdmin, NavigationItemWritePayload } from "@/admin/types/siteAdmin";

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

function emptyPayload(): NavigationItemWritePayload {
  return {
    label_en: "",
    label_it: "",
    target: "/",
    placement: "header",
    is_external: false,
    open_in_new_tab: false,
    enabled: true,
    sort_order: 0,
  };
}

function ItemRow({ item }: { item: NavigationItemAdmin }) {
  const [values, setValues] = useState<NavigationItemWritePayload>({
    label_en: item.label_en,
    label_it: item.label_it,
    target: item.target,
    placement: item.placement,
    is_external: item.is_external,
    open_in_new_tab: item.open_in_new_tab,
    enabled: item.enabled,
    sort_order: item.sort_order,
  });
  const updateItem = useUpdateNavigationItem();
  const deleteItem = useDeleteNavigationItem();
  const { showToast } = useAdminToast();

  async function handleSave() {
    try {
      await updateItem.mutateAsync({ id: item.id, payload: values });
      showToast({ title: "Saved" });
    } catch (error) {
      showToast({
        title: "Could not save",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  return (
    <li className="space-y-3 rounded-lg border border-ink/10 p-4">
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <Input
          value={values.label_en}
          onChange={(e) => setValues({ ...values, label_en: e.target.value })}
          placeholder="Label (English)"
          aria-label="Label (English)"
        />
        <Input
          value={values.label_it}
          onChange={(e) => setValues({ ...values, label_it: e.target.value })}
          placeholder="Label (Italian)"
          aria-label="Label (Italian)"
        />
      </div>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <Input
          value={values.target}
          onChange={(e) => setValues({ ...values, target: e.target.value })}
          placeholder="/path or https://..."
          aria-label="Target"
        />
        <Select
          value={values.placement}
          onChange={(e) =>
            setValues({ ...values, placement: e.target.value as "header" | "footer" })
          }
          aria-label="Placement"
        >
          <option value="header">Header</option>
          <option value="footer">Footer</option>
        </Select>
        <Input
          type="number"
          value={values.sort_order}
          onChange={(e) => setValues({ ...values, sort_order: Number(e.target.value) })}
          aria-label="Sort order"
        />
      </div>
      <div className="flex flex-wrap items-center gap-4 text-xs text-ink-soft">
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-ink/30"
            checked={values.is_external}
            onChange={(e) => setValues({ ...values, is_external: e.target.checked })}
          />
          External link
        </label>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-ink/30"
            checked={values.open_in_new_tab}
            onChange={(e) => setValues({ ...values, open_in_new_tab: e.target.checked })}
          />
          Open in new tab
        </label>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            className="h-4 w-4 rounded border-ink/30"
            checked={values.enabled}
            onChange={(e) => setValues({ ...values, enabled: e.target.checked })}
          />
          Enabled
        </label>
        <Button
          variant="secondary"
          className="px-3 py-1 text-xs"
          onClick={() => void handleSave()}
        >
          Save
        </Button>
        <ConfirmDialog
          trigger={
            <Button variant="danger" className="px-3 py-1 text-xs">
              Delete
            </Button>
          }
          title="Delete this navigation item?"
          description="It will disappear from the public site immediately."
          confirmLabel="Delete"
          onConfirm={() => void deleteItem.mutateAsync(item.id)}
        />
      </div>
    </li>
  );
}

function NewItemForm() {
  const [values, setValues] = useState<NavigationItemWritePayload>(emptyPayload());
  const createItem = useCreateNavigationItem();
  const { showToast } = useAdminToast();

  async function handleCreate() {
    if (!values.label_en.trim() || !values.target.trim()) return;
    try {
      await createItem.mutateAsync(values);
      setValues(emptyPayload());
      showToast({ title: "Added" });
    } catch (error) {
      showToast({
        title: "Could not add item",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  return (
    <Card className="space-y-3">
      <h2 className="font-serif text-lg text-ink">New navigation item</h2>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <Input
          value={values.label_en}
          onChange={(e) => setValues({ ...values, label_en: e.target.value })}
          placeholder="Label (English)"
          aria-label="New label (English)"
        />
        <Input
          value={values.label_it}
          onChange={(e) => setValues({ ...values, label_it: e.target.value })}
          placeholder="Label (Italian)"
          aria-label="New label (Italian)"
        />
      </div>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
        <Input
          value={values.target}
          onChange={(e) => setValues({ ...values, target: e.target.value })}
          placeholder="/about or https://..."
          aria-label="New target"
        />
        <Select
          value={values.placement}
          onChange={(e) =>
            setValues({ ...values, placement: e.target.value as "header" | "footer" })
          }
          aria-label="New placement"
        >
          <option value="header">Header</option>
          <option value="footer">Footer</option>
        </Select>
      </div>
      <Button onClick={() => void handleCreate()} disabled={createItem.isPending}>
        Add
      </Button>
    </Card>
  );
}

export default function NavigationPage() {
  const { data: items, isLoading, isError } = useAdminNavigationList();

  return (
    <div className="max-w-3xl">
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Site</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Navigation</h1>
        <p className="mt-2 text-sm text-ink-soft">
          Header and footer links. Changes take effect immediately, no draft state.
        </p>
      </div>

      <div className="mt-6">
        <NewItemForm />
      </div>

      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError ? (
          <p className="text-sm text-red-700">Could not load navigation items.</p>
        ) : items && items.length > 0 ? (
          <ul className="space-y-3">
            {items.map((item) => (
              <ItemRow key={item.id} item={item} />
            ))}
          </ul>
        ) : (
          <div className="rounded-2xl border border-dashed border-ink/15 p-10 text-center">
            <p className="text-ink-soft">No navigation items yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
