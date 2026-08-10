import { Menu, X } from "lucide-react";
import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import { NavLink, useLocation } from "react-router-dom";

import { useLocale } from "@/app/LocaleContext";
import { LanguageSwitcher } from "@/components/LanguageSwitcher";
import { useNavigation } from "@/hooks/usePortfolioQueries";
import type { NavigationItemPublic } from "@/types/api";

// Used only when the navigation API call fails outright (backend down) — a
// visitor should never be stranded with zero navigation. This is not the
// normal content source; the CMS-managed list from useNavigation() is.
const EMERGENCY_FALLBACK_ITEMS: NavigationItemPublic[] = [
  { label: "Home", target: "/", is_external: false, open_in_new_tab: false },
  { label: "Contact", target: "/contact", is_external: false, open_in_new_tab: false },
];

function NavLinkItem({
  item,
  className,
  onClick,
}: {
  item: NavigationItemPublic;
  className: (isActive: boolean) => string;
  onClick?: () => void;
}) {
  const { localizedPath } = useLocale();

  if (item.is_external) {
    return (
      <a
        href={item.target}
        target={item.open_in_new_tab ? "_blank" : undefined}
        rel={item.open_in_new_tab ? "noreferrer noopener" : undefined}
        className={className(false)}
        onClick={onClick}
      >
        {item.label}
      </a>
    );
  }

  return (
    <NavLink
      to={localizedPath(item.target)}
      end={item.target === "/"}
      target={item.open_in_new_tab ? "_blank" : undefined}
      rel={item.open_in_new_tab ? "noreferrer noopener" : undefined}
      className={({ isActive }) => className(isActive)}
      onClick={onClick}
    >
      {item.label}
    </NavLink>
  );
}

export function Nav() {
  const { t } = useTranslation();
  const { localizedPath } = useLocale();
  const location = useLocation();
  const [open, setOpen] = useState(false);
  const navigation = useNavigation();

  useEffect(() => {
    setOpen(false);
  }, [location.pathname]);

  const headerItems = navigation.isError
    ? EMERGENCY_FALLBACK_ITEMS
    : (navigation.data?.header ?? []);

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
          {headerItems.map((item) => (
            <NavLinkItem
              key={`${item.target}-${item.label}`}
              item={item}
              className={(isActive) =>
                `rounded-full px-3.5 py-2 text-sm transition-colors ${
                  isActive ? "font-medium text-ink" : "text-ink-faint hover:text-ink"
                }`
              }
            />
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
            {headerItems.map((item) => (
              <NavLinkItem
                key={`${item.target}-${item.label}`}
                item={item}
                className={(isActive) =>
                  `rounded-xl px-4 py-3 text-base ${
                    isActive ? "bg-ink/5 font-medium text-ink" : "text-ink-soft"
                  }`
                }
                onClick={() => setOpen(false)}
              />
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
