import { screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { Route, Routes } from "react-router-dom";

import { LanguageSwitcher } from "@/components/LanguageSwitcher";
import { LOCALE_STORAGE_KEY } from "@/i18n";
import { renderWithProviders } from "@/test/testUtils";

function renderSwitcherAt(route: string) {
  return renderWithProviders(
    <Routes>
      <Route path="/about" element={<LanguageSwitcher />} />
      <Route path="/it/about" element={<p>Pagina it attiva</p>} />
    </Routes>,
    route,
  );
}

describe("LanguageSwitcher", () => {
  beforeEach(() => {
    window.localStorage.clear();
  });

  it("marks the active locale with aria-current", () => {
    renderSwitcherAt("/about");
    expect(screen.getByRole("button", { name: "en" })).toHaveAttribute("aria-current", "true");
    expect(screen.getByRole("button", { name: "it" })).not.toHaveAttribute("aria-current");
  });

  it("persists the chosen locale to localStorage when switched", async () => {
    const user = userEvent.setup();
    renderSwitcherAt("/about");

    await user.click(screen.getByRole("button", { name: "it" }));

    expect(window.localStorage.getItem(LOCALE_STORAGE_KEY)).toBe("it");
  });

  it("navigates to the /it-prefixed equivalent path", async () => {
    const user = userEvent.setup();
    renderSwitcherAt("/about");

    await user.click(screen.getByRole("button", { name: "it" }));

    expect(await screen.findByText("Pagina it attiva")).toBeInTheDocument();
  });
});
