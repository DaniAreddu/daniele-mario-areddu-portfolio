import { expect, test } from "@playwright/test";

// Requires an admin account to already exist — see .github/workflows/frontend.yml's
// `e2e` job, which bootstraps one via `python -m app.cli create-admin` before this
// suite runs. Override E2E_ADMIN_EMAIL/E2E_ADMIN_PASSWORD to point at a different
// account when running locally against a database that already has one.
const ADMIN_EMAIL = process.env.E2E_ADMIN_EMAIL ?? "e2e-admin@example.com";
const ADMIN_PASSWORD = process.env.E2E_ADMIN_PASSWORD ?? "correct-horse-battery-staple-e2e";

test.describe("Admin: full project lifecycle", () => {
  test("login, create a draft, publish it, confirm it's public, then trash and delete it", async ({
    page,
  }) => {
    const slug = `e2e-test-project-${Date.now()}`;
    const title = `E2E Test Project ${Date.now()}`;

    await page.goto("/admin/login");
    await page.getByLabel("Email").fill(ADMIN_EMAIL);
    await page.getByLabel("Password").fill(ADMIN_PASSWORD);
    await page.getByRole("button", { name: "Sign in" }).click();
    await expect(page.getByRole("heading", { name: /welcome back/i })).toBeVisible();

    await page.goto("/admin/projects/new");
    await page.getByLabel("Slug").fill(slug);
    await page.getByLabel("Title (English)").fill(title);
    await page.getByRole("button", { name: "Save draft" }).click();
    await expect(page.getByText("Saved", { exact: true })).toBeVisible();

    // Drafts must never be reachable on the public site.
    const draftCheck = await page.request.get(`/api/v1/projects/${slug}`);
    expect(draftCheck.status()).toBe(404);

    await page.getByRole("button", { name: "Publish" }).click();
    await expect(page.getByText("Published", { exact: true })).toBeVisible();

    const publishedCheck = await page.request.get(`/api/v1/projects/${slug}`);
    expect(publishedCheck.ok()).toBe(true);
    expect((await publishedCheck.json()).title).toBe(title);

    await page.getByRole("button", { name: "Move to trash" }).click();
    await page
      .getByRole("dialog")
      .getByRole("button", { name: "Move to trash", exact: true })
      .click();
    await expect(page.getByRole("button", { name: "Restore from trash" })).toBeVisible();

    const trashedCheck = await page.request.get(`/api/v1/projects/${slug}`);
    expect(trashedCheck.status()).toBe(404);

    await page.getByRole("button", { name: "Delete permanently" }).click();
    await page
      .getByRole("dialog")
      .getByRole("button", { name: "Delete permanently", exact: true })
      .click();
    await expect(page).toHaveURL(/\/admin\/projects$/);
  });

  test("an unauthenticated visitor is redirected away from the admin area", async ({
    page,
  }) => {
    await page.context().clearCookies();
    await page.goto("/admin/projects");
    await expect(page).toHaveURL(/\/admin\/login$/);
  });
});
