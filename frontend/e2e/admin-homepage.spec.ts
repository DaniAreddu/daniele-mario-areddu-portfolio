import { expect, test } from "@playwright/test";

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

// Keeps the two tests below from interleaving with each other. They still
// share the homepage singleton with navigation.spec.ts's "home page loads
// with the hero headline" test in a different file — full cross-file
// isolation from that comes from running this suite with a single worker
// (see the `e2e` job in .github/workflows/frontend.yml).
test.describe.configure({ mode: "serial" });

test.describe("Admin: homepage hero content is CMS-driven end to end", () => {
  test("editing the hero headline in /admin/homepage changes the public homepage", async ({
    page,
  }) => {
    const marker = `E2E Homepage Test ${Date.now()}`;

    await login(page);
    await page.goto("/admin/homepage");

    const headlineField = page.getByLabel("Headline (English)", { exact: true });
    // The form mounts with empty react-hook-form defaults and only gets the
    // real fetched values a moment later via a `form.reset()` effect —
    // reading the field before that effect has run would capture "" instead
    // of the actual current headline, and "restoring" it later would blank
    // the site's real content.
    await expect(headlineField).not.toHaveValue("");
    const originalHeadline = await headlineField.inputValue();

    await headlineField.fill(marker);
    await page.getByRole("button", { name: "Save" }).first().click();
    await expect(page.getByText("Saved", { exact: true })).toBeVisible();

    // A fresh navigation (not a client-side route transition) to the public
    // homepage — this is the real integration path, not a mocked check.
    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1 })).toContainText(marker);

    // Restore the original value so the site isn't left with test content.
    await page.goto("/admin/homepage");
    await page.getByLabel("Headline (English)", { exact: true }).fill(originalHeadline);
    await page.getByRole("button", { name: "Save" }).first().click();
    await expect(page.getByText("Saved", { exact: true })).toBeVisible();

    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1 })).toContainText(
      originalHeadline.split("\n")[0],
    );
  });

  test("localization still works after the CMS integration", async ({ page, context }) => {
    await page.goto("/");
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    expect(await page.locator("html").getAttribute("lang")).toBe("en");

    // Fresh storage so the "honor a previously stored language" redirect
    // (see LocaleContext.tsx) doesn't carry over from the check above.
    await context.clearCookies();
    await page.evaluate(() => window.localStorage.clear());

    await page.goto("/it");
    await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
    expect(await page.locator("html").getAttribute("lang")).toBe("it");
  });
});
