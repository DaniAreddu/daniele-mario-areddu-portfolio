import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { z } from "zod";

import { AdminApiError, adminApiFetch } from "@/admin/api/adminApiClient";
import { useAdminAuth } from "@/admin/auth/AdminAuthContext";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { Input } from "@/admin/components/ui/Input";
import { useAdminToast } from "@/admin/components/ui/Toast";
import type { AdminRecoveryCodes, AdminTotpEnroll } from "@/admin/types";

type ViewState = "idle" | "enrolling" | "recovery-codes";

const confirmSchema = z.object({ code: z.string().length(6, "Enter the 6-digit code.") });
type ConfirmValues = z.infer<typeof confirmSchema>;

const passwordSchema = z.object({ password: z.string().min(1, "Enter your password.") });
type PasswordValues = z.infer<typeof passwordSchema>;

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) return error.message;
  return "Something went wrong. Please try again.";
}

export default function SecurityPage() {
  const { user, refresh } = useAdminAuth();
  const { showToast } = useAdminToast();
  const [view, setView] = useState<ViewState>("idle");
  const [enrollment, setEnrollment] = useState<AdminTotpEnroll | null>(null);
  const [recoveryCodes, setRecoveryCodes] = useState<string[]>([]);
  const [error, setError] = useState<string | null>(null);

  const confirmForm = useForm<ConfirmValues>({
    resolver: zodResolver(confirmSchema),
    defaultValues: { code: "" },
  });
  const disableForm = useForm<PasswordValues>({
    resolver: zodResolver(passwordSchema),
    defaultValues: { password: "" },
  });
  const regenerateForm = useForm<PasswordValues>({
    resolver: zodResolver(passwordSchema),
    defaultValues: { password: "" },
  });

  async function beginEnroll() {
    setError(null);
    try {
      const result = await adminApiFetch<AdminTotpEnroll>("/auth/totp/enroll", {
        method: "POST",
      });
      setEnrollment(result);
      setView("enrolling");
    } catch (enrollError) {
      setError(describeError(enrollError));
    }
  }

  const onConfirm = confirmForm.handleSubmit(async (values) => {
    setError(null);
    try {
      const result = await adminApiFetch<AdminRecoveryCodes>("/auth/totp/confirm", {
        method: "POST",
        body: values,
      });
      setRecoveryCodes(result.codes);
      setView("recovery-codes");
      confirmForm.reset();
      await refresh();
      showToast({ title: "Two-factor authentication enabled" });
    } catch (confirmError) {
      setError(describeError(confirmError));
    }
  });

  const onDisable = disableForm.handleSubmit(async (values) => {
    setError(null);
    try {
      await adminApiFetch("/auth/totp/disable", { method: "POST", body: values });
      disableForm.reset();
      await refresh();
      showToast({ title: "Two-factor authentication disabled" });
    } catch (disableError) {
      setError(describeError(disableError));
    }
  });

  const onRegenerate = regenerateForm.handleSubmit(async (values) => {
    setError(null);
    try {
      const result = await adminApiFetch<AdminRecoveryCodes>("/auth/totp/recovery/regenerate", {
        method: "POST",
        body: values,
      });
      setRecoveryCodes(result.codes);
      setView("recovery-codes");
      regenerateForm.reset();
      showToast({ title: "Recovery codes regenerated" });
    } catch (regenerateError) {
      setError(describeError(regenerateError));
    }
  });

  return (
    <div className="max-w-xl space-y-8">
      <div>
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Security</p>
        <h1 className="mt-2 font-serif text-3xl text-ink">Two-factor authentication</h1>
      </div>

      {error ? (
        <p
          role="alert"
          className="rounded-lg border border-red-300 bg-red-50 p-3 text-sm text-red-800"
        >
          {error}
        </p>
      ) : null}

      {view === "recovery-codes" ? (
        <Card>
          <h2 className="font-serif text-xl text-ink">Save your recovery codes</h2>
          <p className="mt-2 text-sm text-ink-soft">
            Each code can be used once if you lose access to your authenticator app. They will
            not be shown again.
          </p>
          <ul className="mt-4 grid grid-cols-2 gap-2 font-mono text-sm">
            {recoveryCodes.map((code) => (
              <li key={code} className="rounded-lg bg-paper-warm px-3 py-2">
                {code}
              </li>
            ))}
          </ul>
          <Button className="mt-6" onClick={() => setView("idle")}>
            I&rsquo;ve saved these codes
          </Button>
        </Card>
      ) : null}

      {view === "idle" && user?.totp_enabled ? (
        <Card className="space-y-6">
          <p className="text-sm text-ink-soft">
            Two-factor authentication is <strong>enabled</strong> on your account.
          </p>
          <form onSubmit={onRegenerate} className="space-y-3">
            <label htmlFor="regen-password" className="eyebrow">
              Regenerate recovery codes
            </label>
            <Input
              id="regen-password"
              type="password"
              autoComplete="current-password"
              {...regenerateForm.register("password")}
            />
            <Button type="submit" variant="secondary">
              Regenerate codes
            </Button>
          </form>
          <form onSubmit={onDisable} className="space-y-3 border-t border-ink/10 pt-6">
            <label htmlFor="disable-password" className="eyebrow">
              Disable two-factor authentication
            </label>
            <Input
              id="disable-password"
              type="password"
              autoComplete="current-password"
              {...disableForm.register("password")}
            />
            <Button type="submit" variant="danger">
              Disable 2FA
            </Button>
          </form>
        </Card>
      ) : null}

      {view === "idle" && !user?.totp_enabled ? (
        <Card>
          <p className="text-sm text-ink-soft">
            Two-factor authentication is <strong>not enabled</strong>. We recommend turning it
            on.
          </p>
          <Button className="mt-4" onClick={() => void beginEnroll()}>
            Enable two-factor authentication
          </Button>
        </Card>
      ) : null}

      {view === "enrolling" && enrollment ? (
        <Card className="space-y-4">
          <p className="text-sm text-ink-soft">
            Scan this QR code with your authenticator app, or enter the key manually.
          </p>
          <img
            src={enrollment.qr_data_uri}
            alt="Two-factor authentication QR code"
            width={200}
            height={200}
            className="rounded-lg border border-ink/10"
          />
          <p className="break-all rounded-lg bg-paper-warm px-3 py-2 font-mono text-xs">
            {enrollment.secret}
          </p>
          <form onSubmit={onConfirm} className="space-y-3">
            <label htmlFor="confirm-code" className="eyebrow">
              Enter the 6-digit code
            </label>
            <Input
              id="confirm-code"
              inputMode="numeric"
              autoComplete="one-time-code"
              aria-invalid={Boolean(confirmForm.formState.errors.code)}
              {...confirmForm.register("code")}
            />
            {confirmForm.formState.errors.code ? (
              <p role="alert" className="text-sm text-red-700">
                {confirmForm.formState.errors.code.message}
              </p>
            ) : null}
            <Button type="submit">Confirm and enable</Button>
          </form>
        </Card>
      ) : null}
    </div>
  );
}
