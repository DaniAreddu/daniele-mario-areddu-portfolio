import type { Page } from "@playwright/test";

/** On narrow viewports the primary nav and language switcher are hidden
 * behind a hamburger menu (see Nav.tsx's `lg:hidden` / `hidden lg:flex`
 * split). Desktop viewports never render that toggle at all, so this is a
 * no-op there. */
export async function openMobileMenuIfPresent(page: Page): Promise<void> {
  const menuButton = page.getByRole("button", { name: /^menu$/i });
  if (await menuButton.isVisible().catch(() => false)) {
    await menuButton.click();
  }
}
