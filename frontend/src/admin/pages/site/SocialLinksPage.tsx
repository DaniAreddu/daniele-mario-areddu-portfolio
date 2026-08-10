import { useState } from "react";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { ConfirmDialog } from "@/admin/components/ui/ConfirmDialog";
import { Input } from "@/admin/components/ui/Input";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminSocialLinkList,
  useCreateSocialLink,
  useDeleteSocialLink,
  useUpdateSocialLink,
} from "@/admin/hooks/useAdminSocialLinks";
import type { SocialLinkAdmin, SocialLinkWritePayload } from "@/admin/types/siteAdmin";

const ALLOWED_ICONS = [
  "github",
  "linkedin",
  "twitter",
  "mastodon",
  "youtube",
  "instagram",
  "rss",
  "mail",
  "globe",
  "sessionize",
];

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

function emptyPayload(): SocialLinkWritePayload {
  return { label: "", url: "", icon: null, enabled: true, sort_order: 0 };
}

function LinkRow({ link }: { link: SocialLinkAdmin }) {
  const [values, setValues] = useState<SocialLinkWritePayload>({
    label: link.label,
    url: link.url,
    icon: link.icon,
    enabled: link.enabled,
    sort_order: link.sort_order,
  });
  const updateLink = useUpdateSocialLink();
  const deleteLink = useDeleteSocialLink();
  const { showToast } = useAdminToast();

  async function handleSave() {
    try {
      await updateLink.mutateAsync({ id: link.id, payload: values });
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
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <Input
          value={values.label}
          onChange={(e) => setValues({ ...values, label: e.target.value })}
          placeholder="Label"
          aria-label="Label"
        />
        <Input
          value={values.url}
          onChange={(e) => setValues({ ...values, url: e.target.value })}
          placeholder="https://..."
          aria-label="URL"
        />
        <Input
          list="icon-options"
          value={values.icon ?? ""}
          onChange={(e) => setValues({ ...values, icon: e.target.value || null })}
          placeholder="icon name"
          aria-label="Icon"
        />
      </div>
      <div className="flex flex-wrap items-center gap-4 text-xs text-ink-soft">
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
          title="Delete this social link?"
          description="It will disappear from the public site immediately."
          confirmLabel="Delete"
          onConfirm={() => void deleteLink.mutateAsync(link.id)}
        />
      </div>
    </li>
  );
}

function NewLinkForm() {
  const [values, setValues] = useState<SocialLinkWritePayload>(emptyPayload());
  const createLink = useCreateSocialLink();
  const { showToast } = useAdminToast();

  async function handleCreate() {
    if (!values.label.trim() || !values.url.trim()) return;
    try {
      await createLink.mutateAsync(values);
      setValues(emptyPayload());
      showToast({ title: "Added" });
    } catch (error) {
      showToast({
        title: "Could not add link",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  return (
    <Card className="space-y-3">
      <h2 className="font-serif text-lg text-ink">New social link</h2>
      <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
        <Input
          value={values.label}
          onChange={(e) => setValues({ ...values, label: e.target.value })}
          placeholder="GitHub"
          aria-label="New label"
        />
        <Input
          value={values.url}
          onChange={(e) => setValues({ ...values, url: e.target.value })}
          placeholder="https://github.com/..."
          aria-label="New URL"
        />
        <Input
          list="icon-options"
          value={values.icon ?? ""}
          onChange={(e) => setValues({ ...values, icon: e.target.value || null })}
          placeholder="github"
          aria-label="New icon"
        />
      </div>
      <Button onClick={() => void handleCreate()} disabled={createLink.isPending}>
        Add
      </Button>
    </Card>
  );
}

export default function SocialLinksPage() {
  const { data: links, isLoading, isError } = useAdminSocialLinkList();

  return (
    <div className="max-w-3xl">
      <datalist id="icon-options">
        {ALLOWED_ICONS.map((icon) => (
          <option key={icon} value={icon} />
        ))}
      </datalist>

      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Site</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Social links</h1>
        <p className="mt-2 text-sm text-ink-soft">
          Shown in the site footer. Icon names must match a known lucide-react icon.
        </p>
      </div>

      <div className="mt-6">
        <NewLinkForm />
      </div>

      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError ? (
          <p className="text-sm text-red-700">Could not load social links.</p>
        ) : links && links.length > 0 ? (
          <ul className="space-y-3">
            {links.map((link) => (
              <LinkRow key={link.id} link={link} />
            ))}
          </ul>
        ) : (
          <div className="rounded-2xl border border-dashed border-ink/15 p-10 text-center">
            <p className="text-ink-soft">No social links yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
