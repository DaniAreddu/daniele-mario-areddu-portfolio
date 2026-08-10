import { Navigate, Outlet, useLocation } from "react-router-dom";

import { useAdminAuth } from "@/admin/auth/AdminAuthContext";

/**
 * Client-side UX only — real enforcement happens on every backend
 * `/api/v1/admin/*` route via `get_current_admin_user`. This just avoids
 * flashing protected UI before the `/auth/me` check resolves.
 */
export function ProtectedRoute() {
  const { status } = useAdminAuth();
  const location = useLocation();

  if (status === "loading") {
    return (
      <div className="flex min-h-screen items-center justify-center bg-paper-warm">
        <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Loading…</p>
      </div>
    );
  }

  if (status !== "authenticated") {
    return <Navigate to="/admin/login" replace state={{ from: location }} />;
  }

  return <Outlet />;
}
