import { Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { NavLink, useLocation } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { LanguageSwitcher } from "@/components/LanguageSwitcher";

const NAV_ITEMS = [
  { path: "/", key: "nav.home" },
  { path: "/about", key: "nav.about" },
  { path: "/journey", key: "nav.journey" },
  { path: "/projects", key: "nav.projects" },
  { path: "/speaking", key: "nav.speaking" },
  { path: "/community", key: "nav.community" },
  { path: "/contact", key: "nav.contact" },
] as const;

export function Nav() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const location = useLocation();
  const [open, setOpen] = useState(false);

  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  return (
    <header className="sticky top-0 z-50 border-b border-ink/10 bg-paper/90 backdrop-blur">
      <div className="container-editorial flex h-16 items-center justify-between sm:h-20">
        <NavLink
          to={localizedPath("/")}
          end
          className="font-serif text-lg font-semibold tracking-tight text-ink sm:text-xl"
        >
          Daniele Mario Areddu
        </NavLink>

        <nav aria-label="Primary" className="hidden items-center gap-1 lg:flex">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={localizedPath(item.path)}
              end={item.path === "/"}
              className={({ isActive }) =>
                `rounded-full px-3.5 py-2 text-sm transition-colors ${
                  isActive ? "font-medium text-ink" : "text-ink-faint hover:text-ink"
                }`
              }
            >
              {t(item.key)}
            </NavLink>
          ))}
        </nav>

        <div className="hidden items-center gap-4 lg:flex">
          <LanguageSwitcher />
          <NavLink to={localizedPath("/contact")} className="btn-primary">
            {t("nav.inviteToSpeak")}
          </NavLink>
        </div>

        <button
          type="button"
          className="inline-flex items-center justify-center rounded-full border border-ink/15 p-2.5 lg:hidden"
          aria-expanded={open}
          aria-controls="mobile-menu"
          aria-label={open ? t("nav.closeMenu") : t("nav.menu")}
          onClick={() => setOpen((value) => !value)}
        >
          {open ? <X size={20} aria-hidden="true" /> : <Menu size={20} aria-hidden="true" />}
        </button>
      </div>

      {open ? (
        <nav
          id="mobile-menu"
          aria-label="Primary"
          className="border-t border-ink/10 bg-paper lg:hidden"
        >
          <div className="container-editorial flex flex-col gap-1 py-4">
            {NAV_ITEMS.map((item) => (
              <NavLink
                key={item.path}
                to={localizedPath(item.path)}
                end={item.path === "/"}
                className={({ isActive }) =>
                  `rounded-xl px-4 py-3 text-base ${
                    isActive ? "bg-ink/5 font-medium text-ink" : "text-ink-soft"
                  }`
                }
              >
                {t(item.key)}
              </NavLink>
            ))}
            <div className="mt-2 flex items-center justify-between px-4">
              <LanguageSwitcher />
              <NavLink to={localizedPath("/contact")} className="btn-primary">
                {t("nav.inviteToSpeak")}
              </NavLink>
            </div>
          </div>
        </nav>
      ) : null}
    </header>
  );
}
