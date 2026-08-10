import { expect, test } from "@playwright/test";

import { findRowByFieldValue } from "./helpers";

// Requires an admin account to already exist — see .github/workflows/frontend.yml's
// `e2e` job, which bootstraps one via `python -m app.cli create-admin` before this
// suite runs. Override E2E_ADMIN_EMAIL/E2E_ADMIN_PASSWORD to point at a different
// account when running locally against a database that already has one.
const ADMIN_EMAIL = process.env.E2E_ADMIN_EMAIL ?? "e2e-admin@example.com";
const ADMIN_PASSWORD = process.env.E2E_ADMIN_PASSWORD ?? "correct-horse-battery-staple-e2e";

test.describe("Admin: footer social links are CMS-driven end to end", () => {
  test("adding a social link in /admin/social-links appears in the public footer, removing it disappears", async ({
    page,
  }) => {
    const label = `E2E Social ${Date.now()}`;

    await page.goto("/admin/login");
    await page.getByLabel("Email").fill(ADMIN_EMAIL);
    await page.getByLabel("Password").fill(ADMIN_PASSWORD);
    await page.getByRole("button", { name: "Sign in" }).click();
    await expect(page.getByRole("heading", { name: /welcome back/i })).toBeVisible();

    await page.goto("/admin/social-links");
    await page.getByLabel("New label").fill(label);
    await page.getByLabel("New URL").fill("https://example.com/e2e-social-test");
    await page.getByLabel("New icon").fill("globe");
    await page.getByRole("button", { name: "Add" }).click();
    await expect(page.getByText("Added", { exact: true })).toBeVisible();

    await page.goto("/");
    const footerLink = page.locator("footer").getByRole("link", { name: label });
    await expect(footerLink).toBeVisible();
    await expect(footerLink).toHaveAttribute("href", "https://example.com/e2e-social-test");

    // Clean up.
    await page.goto("/admin/social-links");
    const row = await findRowByFieldValue(page, "Label", label);
    await row.getByRole("button", { name: "Delete", exact: true }).click();
    await page.getByRole("dialog").getByRole("button", { name: "Delete", exact: true }).click();
    await expect(async () => {
      const fields = page.locator("li").getByLabel("Label", { exact: true });
      const count = await fields.count();
      for (let i = 0; i < count; i += 1) {
        expect(await fields.nth(i).inputValue()).not.toBe(label);
      }
    }).toPass();

    await page.goto("/");
    await expect(page.locator("footer").getByRole("link", { name: label })).toHaveCount(0);
  });
});
