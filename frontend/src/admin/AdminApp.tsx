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
const ExperienceListPage = lazy(() => import("@/admin/pages/experience/ExperienceListPage"));
const ExperienceEditorPage = lazy(
  () => import("@/admin/pages/experience/ExperienceEditorPage"),
);
const ExperiencePreviewPage = lazy(
  () => import("@/admin/pages/experience/ExperiencePreviewPage"),
);
const EducationListPage = lazy(() => import("@/admin/pages/education/EducationListPage"));
const EducationEditorPage = lazy(() => import("@/admin/pages/education/EducationEditorPage"));
const EducationPreviewPage = lazy(() => import("@/admin/pages/education/EducationPreviewPage"));
const SkillsPage = lazy(() => import("@/admin/pages/skills/SkillsPage"));
const ActivityListPage = lazy(() => import("@/admin/pages/community/ActivityListPage"));
const ActivityEditorPage = lazy(() => import("@/admin/pages/community/ActivityEditorPage"));
const ActivityPreviewPage = lazy(() => import("@/admin/pages/community/ActivityPreviewPage"));
const CommunityProfilePage = lazy(() => import("@/admin/pages/community/CommunityProfilePage"));
const RecognitionListPage = lazy(() => import("@/admin/pages/recognition/RecognitionListPage"));
const RecognitionEditorPage = lazy(
  () => import("@/admin/pages/recognition/RecognitionEditorPage"),
);
const RecognitionPreviewPage = lazy(
  () => import("@/admin/pages/recognition/RecognitionPreviewPage"),
);
const ProfilePage = lazy(() => import("@/admin/pages/profile/ProfilePage"));
const BiographyPage = lazy(() => import("@/admin/pages/profile/BiographyPage"));
const MediaPage = lazy(() => import("@/admin/pages/media/MediaPage"));
const SiteSettingsPage = lazy(() => import("@/admin/pages/site/SiteSettingsPage"));
const SeoSettingsPage = lazy(() => import("@/admin/pages/site/SeoSettingsPage"));
const NavigationPage = lazy(() => import("@/admin/pages/site/NavigationPage"));
const SocialLinksPage = lazy(() => import("@/admin/pages/site/SocialLinksPage"));
const RedirectsPage = lazy(() => import("@/admin/pages/site/RedirectsPage"));
const HomepageAdminPage = lazy(() => import("@/admin/pages/site/HomepageAdminPage"));
const AuditLogPage = lazy(() => import("@/admin/pages/AuditLogPage"));
const SystemHealthPage = lazy(() => import("@/admin/pages/SystemHealthPage"));

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
                  <Route path="experience" element={<ExperienceListPage />} />
                  <Route path="experience/new" element={<ExperienceEditorPage />} />
                  <Route path="experience/:id" element={<ExperienceEditorPage />} />
                  <Route path="experience/:id/preview" element={<ExperiencePreviewPage />} />
                  <Route path="education" element={<EducationListPage />} />
                  <Route path="education/new" element={<EducationEditorPage />} />
                  <Route path="education/:id" element={<EducationEditorPage />} />
                  <Route path="education/:id/preview" element={<EducationPreviewPage />} />
                  <Route path="skills" element={<SkillsPage />} />
                  <Route path="community" element={<ActivityListPage />} />
                  <Route path="community/profile" element={<CommunityProfilePage />} />
                  <Route path="community/new" element={<ActivityEditorPage />} />
                  <Route path="community/:id" element={<ActivityEditorPage />} />
                  <Route path="community/:id/preview" element={<ActivityPreviewPage />} />
                  <Route path="recognition" element={<RecognitionListPage />} />
                  <Route path="recognition/new" element={<RecognitionEditorPage />} />
                  <Route path="recognition/:id" element={<RecognitionEditorPage />} />
                  <Route path="recognition/:id/preview" element={<RecognitionPreviewPage />} />
                  <Route path="profile" element={<ProfilePage />} />
                  <Route path="biography" element={<BiographyPage />} />
                  <Route path="media" element={<MediaPage />} />
                  <Route path="site-settings" element={<SiteSettingsPage />} />
                  <Route path="seo-settings" element={<SeoSettingsPage />} />
                  <Route path="navigation" element={<NavigationPage />} />
                  <Route path="social-links" element={<SocialLinksPage />} />
                  <Route path="redirects" element={<RedirectsPage />} />
                  <Route path="homepage" element={<HomepageAdminPage />} />
                  <Route path="audit-log" element={<AuditLogPage />} />
                  <Route path="system" element={<SystemHealthPage />} />
                </Route>
              </Route>
            </Routes>
          </Suspense>
        </AdminToastProvider>
      </AdminAuthProvider>
    </AdminErrorBoundary>
  );
}
