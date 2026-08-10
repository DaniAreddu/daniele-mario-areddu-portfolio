import { useRef, useState } from "react";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { ConfirmDialog } from "@/admin/components/ui/ConfirmDialog";
import { Input } from "@/admin/components/ui/Input";
import { useAdminToast } from "@/admin/components/ui/Toast";
import {
  useAdminMediaList,
  useDeleteMedia,
  useUpdateMedia,
  useUploadMedia,
} from "@/admin/hooks/useAdminMedia";
import type { MediaAsset } from "@/admin/types/media";

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function UploadCard() {
  const inputRef = useRef<HTMLInputElement>(null);
  const upload = useUploadMedia();
  const { showToast } = useAdminToast();

  async function handleFiles(files: FileList | null) {
    if (!files || files.length === 0) return;
    for (const file of Array.from(files)) {
      try {
        await upload.mutateAsync(file);
      } catch (error) {
        showToast({
          title: `Could not upload '${file.name}'`,
          description: describeError(error),
          variant: "error",
        });
      }
    }
    if (inputRef.current) inputRef.current.value = "";
  }

  return (
    <Card className="flex flex-col items-center justify-center gap-3 border-dashed p-10 text-center">
      <p className="text-sm text-ink-soft">
        Upload JPEG, PNG, WEBP, or GIF images. Files are validated server-side.
      </p>
      <input
        ref={inputRef}
        type="file"
        accept="image/jpeg,image/png,image/webp,image/gif"
        multiple
        onChange={(event) => void handleFiles(event.target.files)}
        className="hidden"
        id="media-upload-input"
      />
      <Button onClick={() => inputRef.current?.click()} disabled={upload.isPending}>
        {upload.isPending ? "Uploading…" : "Upload files"}
      </Button>
    </Card>
  );
}

function MediaCard({ asset }: { asset: MediaAsset }) {
  const [altText, setAltText] = useState(asset.alt_text ?? "");
  const [caption, setCaption] = useState(asset.caption ?? "");
  const [usageWarning, setUsageWarning] = useState<string | null>(null);
  const updateMedia = useUpdateMedia();
  const deleteMedia = useDeleteMedia();
  const { showToast } = useAdminToast();

  async function handleSaveMetadata() {
    try {
      await updateMedia.mutateAsync({
        id: asset.id,
        altText: altText || null,
        caption: caption || null,
      });
      showToast({ title: "Saved" });
    } catch (error) {
      showToast({
        title: "Could not save",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  async function handleDelete(force: boolean) {
    try {
      await deleteMedia.mutateAsync({ id: asset.id, force });
      showToast({ title: "Deleted" });
    } catch (error) {
      if (error instanceof AdminApiError && error.code === "media_in_use") {
        setUsageWarning(error.message);
        return;
      }
      showToast({
        title: "Could not delete",
        description: describeError(error),
        variant: "error",
      });
    }
  }

  async function copyUrl() {
    await navigator.clipboard.writeText(new URL(asset.url, window.location.origin).toString());
    showToast({ title: "URL copied" });
  }

  const thumbnail = asset.variants.thumbnail ?? asset.url;

  return (
    <Card className="space-y-3">
      <img
        src={thumbnail}
        alt={asset.alt_text ?? ""}
        className="h-40 w-full rounded-lg border border-ink/10 object-cover"
      />
      <div>
        <p className="truncate text-sm font-medium text-ink" title={asset.original_filename}>
          {asset.original_filename}
        </p>
        <p className="font-mono text-xs text-ink-faint">
          {asset.width}×{asset.height} · {formatBytes(asset.size_bytes)}
        </p>
      </div>
      <Input
        value={altText}
        onChange={(event) => setAltText(event.target.value)}
        placeholder="Alt text (required for accessibility)"
        aria-label="Alt text"
      />
      <Input
        value={caption}
        onChange={(event) => setCaption(event.target.value)}
        placeholder="Caption (optional)"
        aria-label="Caption"
      />
      {usageWarning ? (
        <p role="alert" className="text-xs text-amber-700">
          {usageWarning}
        </p>
      ) : null}
      <div className="flex flex-wrap items-center gap-2">
        <Button
          variant="secondary"
          className="px-3 py-1 text-xs"
          onClick={() => void handleSaveMetadata()}
        >
          Save
        </Button>
        <Button
          variant="secondary"
          className="px-3 py-1 text-xs"
          onClick={() => void copyUrl()}
        >
          Copy URL
        </Button>
        {usageWarning ? (
          <ConfirmDialog
            trigger={
              <Button variant="danger" className="px-3 py-1 text-xs">
                Delete anyway
              </Button>
            }
            title="Delete this file anyway?"
            description={usageWarning}
            confirmLabel="Delete anyway"
            onConfirm={() => void handleDelete(true)}
          />
        ) : (
          <Button
            variant="danger"
            className="px-3 py-1 text-xs"
            onClick={() => void handleDelete(false)}
          >
            Delete
          </Button>
        )}
      </div>
    </Card>
  );
}

export default function MediaPage() {
  const { data: assets, isLoading, isError } = useAdminMediaList();

  return (
    <div>
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Media</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Media library</h1>
        <p className="mt-2 text-sm text-ink-soft">
          Uploaded files are stored outside the database. Deleting a file that's referenced by
          published content warns before proceeding.
        </p>
      </div>

      <div className="mt-6">
        <UploadCard />
      </div>

      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-ink-faint">Loading…</p>
        ) : isError ? (
          <p className="text-sm text-red-700">Could not load media.</p>
        ) : assets && assets.length > 0 ? (
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {assets.map((asset) => (
              <MediaCard key={asset.id} asset={asset} />
            ))}
          </div>
        ) : (
          <div className="rounded-2xl border border-dashed border-ink/15 p-10 text-center">
            <p className="text-ink-soft">No media uploaded yet.</p>
          </div>
        )}
      </div>
    </div>
  );
}
