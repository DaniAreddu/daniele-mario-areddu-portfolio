import { lazy, Suspense } from "react";
import { Route, Routes } from "react-router-dom";

import { AdminAuthProvider } from "@/admin/auth/AdminAuthContext";
import { ProtectedRoute } from "@/admin/auth/ProtectedRoute";
import { AdminErrorBoundary } from "@/admin/components/AdminErrorBoundary";
import { AdminToastProvider } from "@/admin/components/ui/Toast";
import { AdminLayout } from "@/admin/layouts/AdminLayout";

const LoginPage = lazy(() => import("@/admin/pages/LoginPage"));
const DashboardPage = lazy(() => import("@/admin/pages/DashboardPage"));
const SecurityPage = lazy(() => import("@/admin/pages/SecurityPage"));
const SpeakingListPage = lazy(() => import("@/admin/pages/speaking/SpeakingListPage"));
const SpeakingEditorPage = lazy(() => import("@/admin/pages/speaking/SpeakingEditorPage"));
const SpeakingPreviewPage = lazy(() => import("@/admin/pages/speaking/SpeakingPreviewPage"));
const ProjectsListPage = lazy(() => import("@/admin/pages/projects/ProjectsListPage"));
const ProjectsEditorPage = lazy(() => import("@/admin/pages/projects/ProjectsEditorPage"));
const ProjectsPreviewPage = lazy(() => import("@/admin/pages/projects/ProjectsPreviewPage"));

function AdminLoadingFallback() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-paper-warm">
      <p className="font-mono text-xs uppercase tracking-wide text-ink-faint">Loading…</p>
    </div>
  );
}

/**
 * The entire private webmaster area, mounted at `/admin/*` outside the
 * public site's bilingual RootLayout (see src/app/router.tsx) — it isn't
 * localized, doesn't get the public Nav/Footer, and is lazy-loaded so it
 * never inflates the public bundle. Excluded from
 * scripts/generate-sitemap.mjs and scripts/prerender.mjs on purpose.
 */
export default function AdminApp() {
  return (
    <AdminErrorBoundary>
      <AdminAuthProvider>
        <AdminToastProvider>
          <Suspense fallback={<AdminLoadingFallback />}>
            <Routes>
              <Route path="login" element={<LoginPage />} />
              <Route element={<ProtectedRoute />}>
                <Route element={<AdminLayout />}>
                  <Route index element={<DashboardPage />} />
                  <Route path="security" element={<SecurityPage />} />
                  <Route path="speaking" element={<SpeakingListPage />} />
                  <Route path="speaking/new" element={<SpeakingEditorPage />} />
                  <Route path="speaking/:id" element={<SpeakingEditorPage />} />
                  <Route path="speaking/:id/preview" element={<SpeakingPreviewPage />} />
                  <Route path="projects" element={<ProjectsListPage />} />
                  <Route path="projects/new" element={<ProjectsEditorPage />} />
                  <Route path="projects/:id" element={<ProjectsEditorPage />} />
                  <Route path="projects/:id/preview" element={<ProjectsPreviewPage />} />
                </Route>
              </Route>
            </Routes>
          </Suspense>
        </AdminToastProvider>
      </AdminAuthProvider>
    </AdminErrorBoundary>
  );
}
