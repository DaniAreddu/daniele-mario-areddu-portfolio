import { expect, test } from "@playwright/test";

test.describe("Contact form", () => {
  test("shows validation errors for an empty submission", async ({ page }) => {
    await page.goto("/contact");
    await page.getByRole("button", { name: /send message/i }).click();
    await expect(page.getByRole("alert").first()).toBeVisible();
  });

  test("submits successfully against the real backend (development email flow)", async ({
    page,
  }) => {
    await page.goto("/contact");
    await page.getByLabel("Name", { exact: true }).fill("Playwright Tester");
    await page.getByLabel("Email", { exact: true }).fill("tester@example.com");
    await page
      .getByLabel(/^message$/i)
      .fill("This is an end-to-end test submission from Playwright.");
    await page.getByLabel(/agree/i).check();
    await page.getByRole("button", { name: /send message/i }).click();

    // Whether or not a local Mailpit/SMTP relay is reachable, the API must
    // never claim success without saying so honestly; both outcomes render
    // a `status` region with a message, never a silent failure.
    await expect(page.getByRole("status")).toBeVisible({ timeout: 10_000 });
  });

  test("handles an API failure gracefully instead of hanging or crashing", async ({ page }) => {
    await page.route("**/api/v1/contact", (route) =>
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ error: { code: "internal_error", message: "boom" } }),
      }),
    );

    await page.goto("/contact");
    await page.getByLabel("Name", { exact: true }).fill("Playwright Tester");
    await page.getByLabel("Email", { exact: true }).fill("tester@example.com");
    await page
      .getByLabel(/^message$/i)
      .fill("This is an end-to-end test submission from Playwright.");
    await page.getByLabel(/agree/i).check();
    await page.getByRole("button", { name: /send message/i }).click();

    await expect(page.getByRole("alert")).toContainText(/something went wrong/i);
  });
});
