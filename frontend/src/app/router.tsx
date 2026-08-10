import { lazy } from "react";
import { Route, Routes } from "react-router-dom";

import { RootLayout } from "@/layouts/RootLayout";

// The private webmaster area — not bilingual, not wrapped in the public
// Nav/Footer chrome, and deliberately excluded from
// scripts/generate-sitemap.mjs and scripts/prerender.mjs.
const AdminApp = lazy(() => import("@/admin/AdminApp"));

const HomePage = lazy(() => import("@/pages/HomePage"));
const AboutPage = lazy(() => import("@/pages/AboutPage"));
const JourneyPage = lazy(() => import("@/pages/JourneyPage"));
const ExperiencePage = lazy(() => import("@/pages/ExperiencePage"));
const ProjectsPage = lazy(() => import("@/pages/ProjectsPage"));
const ProjectDetailPage = lazy(() => import("@/pages/ProjectDetailPage"));
const SpeakingPage = lazy(() => import("@/pages/SpeakingPage"));
const CommunityPage = lazy(() => import("@/pages/CommunityPage"));
const PassionsPage = lazy(() => import("@/pages/PassionsPage"));
const ContactPage = lazy(() => import("@/pages/ContactPage"));
const PrivacyPage = lazy(() => import("@/pages/PrivacyPage"));
const NotFoundPage = lazy(() => import("@/pages/NotFoundPage"));

const ROUTE_DEFS = [
  { path: "", Component: HomePage },
  { path: "about", Component: AboutPage },
  { path: "journey", Component: JourneyPage },
  { path: "experience", Component: ExperiencePage },
  { path: "projects", Component: ProjectsPage },
  { path: "projects/:slug", Component: ProjectDetailPage },
  { path: "speaking", Component: SpeakingPage },
  { path: "community", Component: CommunityPage },
  { path: "passions", Component: PassionsPage },
  { path: "contact", Component: ContactPage },
  { path: "privacy", Component: PrivacyPage },
] as const;

function renderRouteDefs() {
  return ROUTE_DEFS.map(({ path, Component }) =>
    path === "" ? (
      <Route key="home" index element={<Component />} />
    ) : (
      <Route key={path} path={path} element={<Component />} />
    ),
  );
}

export function AppRouter() {
  return (
    <Routes>
      <Route path="admin/*" element={<AdminApp />} />
      <Route element={<RootLayout />}>
        {renderRouteDefs()}
        <Route path="it">{renderRouteDefs()}</Route>
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  );
}
