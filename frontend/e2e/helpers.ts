import { expect, type Locator, type Page } from "@playwright/test";

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

/**
 * Finds the `<li>` row whose form field (matched by its generic, shared
 * aria-label — every row in these admin list pages reuses the same label
 * text, e.g. "Label (English)") currently holds `value`.
 *
 * Playwright has no built-in way to match an element by a live,
 * React-controlled input's current value: `hasText`/`innerText` only see
 * DOM text nodes (an <input>'s value is a property, not text content), and
 * a CSS `[value=...]` attribute selector only sees the value an element was
 * given in markup, not one React set via the DOM property after mount. This
 * reads the actual current value of each candidate field directly instead.
 *
 * Retries internally (via `expect(...).toPass()`) since the row may not
 * have loaded/re-rendered yet right after a create or a page reload.
 */
export async function findRowByFieldValue(
  page: Page,
  fieldAriaLabel: string,
  value: string,
): Promise<Locator> {
  let found: Locator | undefined;
  await expect(async () => {
    const fields = page.locator("li").getByLabel(fieldAriaLabel, { exact: true });
    const count = await fields.count();
    for (let i = 0; i < count; i += 1) {
      if ((await fields.nth(i).inputValue()) === value) {
        found = page.locator("li").nth(i);
        return;
      }
    }
    throw new Error(`No row found with ${fieldAriaLabel} = "${value}"`);
  }).toPass();
  return found as Locator;
}
