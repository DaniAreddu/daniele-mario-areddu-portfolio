import { expect, test } from "@playwright/test";

import { openMobileMenuIfPresent } from "./helpers";

test.describe("Localization", () => {
  test("switching language navigates to the /it route and translates content", async ({
    page,
  }) => {
    await page.goto("/about");
    await openMobileMenuIfPresent(page);
    await page.getByRole("button", { name: "it" }).click();
    await expect(page).toHaveURL(/\/it\/about$/);
    await expect(page.locator("html")).toHaveAttribute("lang", "it");
  });

  test("language choice persists across a fresh visit to the root URL", async ({ page }) => {
    await page.goto("/about");
    await openMobileMenuIfPresent(page);
    await page.getByRole("button", { name: "it" }).click();
    await expect(page).toHaveURL(/\/it\/about$/);

    await page.goto("/");
    await expect(page).toHaveURL(/\/it$/);
  });

  test("direct link to an explicit English route is respected even with an Italian preference stored", async ({
    page,
  }) => {
    await page.goto("/about");
    await openMobileMenuIfPresent(page);
    await page.getByRole("button", { name: "it" }).click();

    await page.goto("/about");
    await expect(page).toHaveURL(/\/about$/);
    await expect(page.locator("html")).toHaveAttribute("lang", "en");
  });
});
