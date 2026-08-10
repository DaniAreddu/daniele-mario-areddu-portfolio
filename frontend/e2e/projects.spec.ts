import { expect, test } from "@playwright/test";

test.describe("Projects", () => {
  test("opening a project from the list shows its case study", async ({ page }) => {
    await page.goto("/projects");
    await page.getByRole("link", { name: /Municipal Data Reconciliation Platform/i }).click();
    await expect(page).toHaveURL(/\/projects\/municipal-data-reconciliation-platform$/);
    await expect(page.getByRole("heading", { level: 1 })).toContainText(
      "Municipal Data Reconciliation Platform",
    );
    await expect(page.getByRole("heading", { name: /confidentiality/i })).toBeVisible();
  });

  test("an unknown project slug redirects back to the projects list", async ({ page }) => {
    await page.goto("/projects/does-not-exist");
    await expect(page).toHaveURL(/\/projects$/);
  });
});
