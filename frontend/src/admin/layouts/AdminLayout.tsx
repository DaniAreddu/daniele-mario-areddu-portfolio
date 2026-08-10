import { clsx } from "clsx";
import { NavLink, Outlet } from "react-router-dom";

import { useAdminAuth } from "@/admin/auth/AdminAuthContext";
import { CommandPalette } from "@/admin/components/CommandPalette";

// This list grows across later phases (Speaking, Projects, Media, Site
// administration, ...). With only a couple of entries today a simple
// always-visible row works on mobile; once it grows, this should become a
// real collapsible/hamburger nav rather than wrapping indefinitely.
const NAV_ITEMS = [
  { to: "/admin", label: "Dashboard", end: true },
  { to: "/admin/speaking", label: "Speaking", end: false },
  { to: "/admin/projects", label: "Projects", end: false },
  { to: "/admin/experience", label: "Experience", end: false },
  { to: "/admin/education", label: "Education", end: false },
  { to: "/admin/skills", label: "Skills", end: false },
  { to: "/admin/community", label: "Community", end: false },
  { to: "/admin/recognition", label: "Recognition", end: false },
  { to: "/admin/profile", label: "Profile", end: false },
  { to: "/admin/biography", label: "Biography", end: false },
  { to: "/admin/media", label: "Media", end: false },
  { to: "/admin/homepage", label: "Homepage", end: false },
  { to: "/admin/navigation", label: "Navigation", end: false },
  { to: "/admin/social-links", label: "Social links", end: false },
  { to: "/admin/redirects", label: "Redirects", end: false },
  { to: "/admin/site-settings", label: "Site settings", end: false },
  { to: "/admin/seo-settings", label: "SEO settings", end: false },
  { to: "/admin/audit-log", label: "Audit log", end: false },
  { to: "/admin/system", label: "System", end: false },
  { to: "/admin/security", label: "Security", end: false },
] as const;

function navLinkClassName(isActive: boolean) {
  return clsx(
    "rounded-lg px-3 py-2 text-sm transition-colors",
    isActive ? "bg-ink text-paper" : "text-ink-soft hover:bg-paper-warm hover:text-ink",
  );
}

export function AdminLayout() {
  const { user, logout } = useAdminAuth();

  return (
    <div className="flex min-h-screen bg-paper-warm font-sans text-ink">
      <CommandPalette />
      <aside className="hidden w-60 shrink-0 flex-col border-r border-ink/10 bg-paper p-6 lg:flex">
        <p className="font-serif text-lg text-ink">Webmaster</p>
        <p className="mt-1 text-xs text-ink-faint">Press Ctrl/Cmd+K to search</p>
        <nav aria-label="Admin navigation" className="mt-8 flex flex-col gap-1">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.end}
              className={({ isActive }) => navLinkClassName(isActive)}
            >
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="mt-auto space-y-3 border-t border-ink/10 pt-6 text-xs">
          <a
            href="/"
            target="_blank"
            rel="noreferrer"
            className="block text-ink-faint hover:text-cobalt"
          >
            View site ↗
          </a>
          {user ? <p className="truncate text-ink-faint">{user.email}</p> : null}
          <button
            type="button"
            onClick={() => void logout()}
            className="text-ink-faint hover:text-cobalt"
          >
            Sign out
          </button>
        </div>
      </aside>

      <div className="flex-1">
        <header className="border-b border-ink/10 bg-paper px-4 py-4 lg:hidden">
          <div className="flex items-center justify-between">
            <p className="font-serif text-lg text-ink">Webmaster</p>
            <button
              type="button"
              onClick={() => void logout()}
              className="text-xs text-ink-faint hover:text-cobalt"
            >
              Sign out
            </button>
          </div>
          <nav
            aria-label="Admin navigation"
            className="mt-3 flex flex-wrap gap-1 border-t border-ink/10 pt-3"
          >
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.end}
                className={({ isActive }) => navLinkClassName(isActive)}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </header>

        <main id="admin-main-content" className="mx-auto max-w-5xl px-6 py-10">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
