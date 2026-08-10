import { expect, test } from "@playwright/test";

import { findRowByFieldValue } from "./helpers";

// Requires an admin account to already exist — see .github/workflows/frontend.yml's
// `e2e` job, which bootstraps one via `python -m app.cli create-admin` before this
// suite runs. Override E2E_ADMIN_EMAIL/E2E_ADMIN_PASSWORD to point at a different
// account when running locally against a database that already has one.
const ADMIN_EMAIL = process.env.E2E_ADMIN_EMAIL ?? "e2e-admin@example.com";
const ADMIN_PASSWORD = process.env.E2E_ADMIN_PASSWORD ?? "correct-horse-battery-staple-e2e";

async function login(page: import("@playwright/test").Page) {
  await page.goto("/admin/login");
  await page.getByLabel("Email").fill(ADMIN_EMAIL);
  await page.getByLabel("Password").fill(ADMIN_PASSWORD);
  await page.getByRole("button", { name: "Sign in" }).click();
  await expect(page.getByRole("heading", { name: /welcome back/i })).toBeVisible();
}

test.describe("Admin: navigation is CMS-driven end to end", () => {
  test("creating, reordering, disabling, and deleting a nav item propagates to the public site", async ({
    page,
  }) => {
    const label = `E2E Nav ${Date.now()}`;

    await login(page);
    await page.goto("/admin/navigation");

    // Create.
    await page.getByLabel("New label (English)").fill(label);
    await page.getByLabel("New target").fill("/contact");
    await page.getByRole("button", { name: "Add" }).click();
    await expect(page.getByText("Added", { exact: true })).toBeVisible();
    await findRowByFieldValue(page, "Label (English)", label);

    // Public site shows the new item (default sort_order puts it last).
    await page.goto("/");
    await expect(page.getByRole("navigation", { name: "Primary" }).first()).toContainText(
      label,
    );

    // Reorder: push it to the very front with a very low sort order. Each
    // step below re-locates the row rather than reusing one Locator, since a
    // `.nth(index)`-based row identity isn't stable across a reorder.
    await page.goto("/admin/navigation");
    let row = await findRowByFieldValue(page, "Label (English)", label);
    await row.getByLabel("Sort order").fill("-1");
    await row.getByRole("button", { name: "Save", exact: true }).click();
    await expect(page.getByText("Saved", { exact: true })).toBeVisible();

    await page.goto("/");
    const headerLinks = page
      .getByRole("navigation", { name: "Primary" })
      .first()
      .getByRole("link");
    await expect(headerLinks.first()).toHaveText(label);

    // Disable: the item must disappear from the public site.
    await page.goto("/admin/navigation");
    row = await findRowByFieldValue(page, "Label (English)", label);
    await row.getByLabel("Enabled").uncheck();
    await row.getByRole("button", { name: "Save", exact: true }).click();
    await expect(page.getByText("Saved", { exact: true })).toBeVisible();

    await page.goto("/");
    await expect(page.getByRole("navigation", { name: "Primary" }).first()).not.toContainText(
      label,
    );

    // Clean up.
    await page.goto("/admin/navigation");
    row = await findRowByFieldValue(page, "Label (English)", label);
    await row.getByRole("button", { name: "Delete", exact: true }).click();
    await page.getByRole("dialog").getByRole("button", { name: "Delete", exact: true }).click();
    await expect(async () => {
      const fields = page.locator("li").getByLabel("Label (English)", { exact: true });
      const count = await fields.count();
      for (let i = 0; i < count; i += 1) {
        expect(await fields.nth(i).inputValue()).not.toBe(label);
      }
    }).toPass();
  });
});
