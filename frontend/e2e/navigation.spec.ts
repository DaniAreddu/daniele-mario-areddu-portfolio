import { expect, test } from "@playwright/test";

import { openMobileMenuIfPresent } from "./helpers";

test.describe("Global navigation", () => {
  test("home page loads with the hero headline", async ({ page }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1 })).toContainText(
      /Building intelligent systems/i,
    );
  });

  test("primary navigation links move between pages", async ({ page }) => {
    await page.goto("/");
    await openMobileMenuIfPresent(page);
    await page
      .getByRole("navigation", { name: "Primary" })
      .getByRole("link", { name: "About" })
      .click();
    await expect(page).toHaveURL(/\/about$/);
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  });

  test("direct navigation to a nested route works without going through the app", async ({
    page,
  }) => {
    await page.goto("/projects");
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    await page.reload();
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  });

  test("custom 404 page renders for an unknown route", async ({ page }) => {
    await page.goto("/this-page-does-not-exist");
    await expect(page.getByText("404")).toBeVisible();
    await page.getByRole("link", { name: /back to home/i }).click();
    await expect(page).toHaveURL(/\/$/);
  });

  test("skip link moves focus to main content", async ({ page }) => {
    await page.goto("/");
    await page.keyboard.press("Tab");
    await expect(page.getByRole("link", { name: /skip to content/i })).toBeFocused();
  });
});
