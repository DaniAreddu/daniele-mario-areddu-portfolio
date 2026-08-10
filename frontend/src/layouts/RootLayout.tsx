import { Suspense } from "react";
import { useTranslation } from "react-i18next";
import { Outlet, useLocation } from "react-router-dom";

import { LoadingState } from "@/components/AsyncState";
import { Footer } from "@/components/Footer";
import { Nav } from "@/components/Nav";

export function RootLayout() {
  const { t } = useTranslation();
  const location = useLocation();

  return (
    <div className="flex min-h-screen flex-col">
      <a href="#main-content" className="skip-link">
        {t("nav.skipToContent")}
      </a>
      <Nav />
      {/* The Suspense boundary lives here, around the routed page only, so
          the nav/skip-link/footer chrome stays mounted across route changes
          instead of being replaced by the loading fallback every time a lazy
          page chunk suspends. */}
      <main id="main-content" tabIndex={-1} className="flex-1" key={location.pathname}>
        <Suspense fallback={<LoadingState />}>
          <Outlet />
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}
