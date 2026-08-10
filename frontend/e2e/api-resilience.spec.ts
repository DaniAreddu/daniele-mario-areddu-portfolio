import { expect, test } from "@playwright/test";

test.describe("API failure handling", () => {
  test("a failed profile request shows a retry state instead of a blank page", async ({
    page,
  }) => {
    await page.route("**/api/v1/profile*", (route) =>
      route.fulfill({
        status: 500,
        contentType: "application/json",
        body: JSON.stringify({ error: { code: "internal_error", message: "boom" } }),
      }),
    );

    await page.goto("/");
    await expect(page.getByRole("alert")).toBeVisible();
    await expect(page.getByRole("button", { name: /retry/i })).toBeVisible();
  });
});
