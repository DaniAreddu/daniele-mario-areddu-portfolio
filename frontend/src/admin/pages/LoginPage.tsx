import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";

import { AdminApiError } from "@/admin/api/adminApiClient";
import { useAdminAuth } from "@/admin/auth/AdminAuthContext";
import { Button } from "@/admin/components/ui/Button";
import { Card } from "@/admin/components/ui/Card";
import { Input } from "@/admin/components/ui/Input";

const credentialsSchema = z.object({
  email: z.string().email("Enter a valid email address."),
  password: z.string().min(1, "Enter your password."),
});
type CredentialsValues = z.infer<typeof credentialsSchema>;

const totpSchema = z.object({
  code: z.string().min(6, "Enter your 6-digit code or a recovery code."),
});
type TotpValues = z.infer<typeof totpSchema>;

function describeError(error: unknown): string {
  if (error instanceof AdminApiError) {
    if (error.status === 429) {
      return "Too many attempts. Please wait a few minutes and try again.";
    }
    return error.message;
  }
  return "Something went wrong. Please try again.";
}

export default function LoginPage() {
  const { login, verifyTotp, status } = useAdminAuth();
  const navigate = useNavigate();
  const [error, setError] = useState<string | null>(null);
  const showTotpStep = status === "mfa-required";

  const credentialsForm = useForm<CredentialsValues>({
    resolver: zodResolver(credentialsSchema),
    defaultValues: { email: "", password: "" },
  });
  const totpForm = useForm<TotpValues>({
    resolver: zodResolver(totpSchema),
    defaultValues: { code: "" },
  });

  const onSubmitCredentials = credentialsForm.handleSubmit(async (values) => {
    setError(null);
    try {
      const result = await login(values.email, values.password);
      if (result.status === "authenticated") navigate("/admin", { replace: true });
    } catch (submitError) {
      setError(describeError(submitError));
    }
  });

  const onSubmitTotp = totpForm.handleSubmit(async (values) => {
    setError(null);
    try {
      await verifyTotp(values.code);
      navigate("/admin", { replace: true });
    } catch (submitError) {
      setError(describeError(submitError));
    }
  });

  return (
    <div className="flex min-h-screen items-center justify-center bg-paper-warm px-4">
      <Card className="w-full max-w-sm">
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">
          Areddu Portfolio
        </p>
        <h1 className="mt-2 font-serif text-2xl text-ink">
          {showTotpStep ? "Enter your authentication code" : "Sign in"}
        </h1>

        {error ? (
          <p
            role="alert"
            className="mt-4 rounded-lg border border-red-300 bg-red-50 p-3 text-sm text-red-800"
          >
            {error}
          </p>
        ) : null}

        {showTotpStep ? (
          <form onSubmit={onSubmitTotp} noValidate className="mt-6 space-y-4">
            <div>
              <label htmlFor="code" className="eyebrow">
                6-digit code or recovery code
              </label>
              <Input
                id="code"
                inputMode="text"
                autoComplete="one-time-code"
                aria-invalid={Boolean(totpForm.formState.errors.code)}
                aria-describedby={totpForm.formState.errors.code ? "code-error" : undefined}
                className="mt-2"
                {...totpForm.register("code")}
              />
              {totpForm.formState.errors.code ? (
                <p id="code-error" role="alert" className="mt-1 text-sm text-red-700">
                  {totpForm.formState.errors.code.message}
                </p>
              ) : null}
            </div>
            <Button type="submit" className="w-full" disabled={totpForm.formState.isSubmitting}>
              Verify
            </Button>
          </form>
        ) : (
          <form onSubmit={onSubmitCredentials} noValidate className="mt-6 space-y-4">
            <div>
              <label htmlFor="email" className="eyebrow">
                Email
              </label>
              <Input
                id="email"
                type="email"
                autoComplete="email"
                aria-invalid={Boolean(credentialsForm.formState.errors.email)}
                aria-describedby={
                  credentialsForm.formState.errors.email ? "email-error" : undefined
                }
                className="mt-2"
                {...credentialsForm.register("email")}
              />
              {credentialsForm.formState.errors.email ? (
                <p id="email-error" role="alert" className="mt-1 text-sm text-red-700">
                  {credentialsForm.formState.errors.email.message}
                </p>
              ) : null}
            </div>
            <div>
              <label htmlFor="password" className="eyebrow">
                Password
              </label>
              <Input
                id="password"
                type="password"
                autoComplete="current-password"
                aria-invalid={Boolean(credentialsForm.formState.errors.password)}
                aria-describedby={
                  credentialsForm.formState.errors.password ? "password-error" : undefined
                }
                className="mt-2"
                {...credentialsForm.register("password")}
              />
              {credentialsForm.formState.errors.password ? (
                <p id="password-error" role="alert" className="mt-1 text-sm text-red-700">
                  {credentialsForm.formState.errors.password.message}
                </p>
              ) : null}
            </div>
            <Button
              type="submit"
              className="w-full"
              disabled={credentialsForm.formState.isSubmitting}
            >
              Sign in
            </Button>
          </form>
        )}
      </Card>
    </div>
  );
}
