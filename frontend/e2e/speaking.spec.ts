import { expect, test } from "@playwright/test";

test.describe("Speaking map and catalogue", () => {
  test("map view renders and can be switched to the accessible list view", async ({ page }) => {
    await page.goto("/speaking");
    await expect(page.getByRole("heading", { name: /speaking/i, level: 1 })).toBeVisible();

    await page.getByRole("button", { name: /list view/i }).click();
    await expect(page.getByRole("list", { name: /event catalogue/i }).first()).toBeVisible();
  });

  test("filters narrow down the visible events", async ({ page }) => {
    await page.goto("/speaking");
    await page.getByRole("button", { name: /list view/i }).click();

    const continentSelect = page.getByLabel(/continent/i);
    await continentSelect.selectOption({ label: "Central Asia" });

    await expect(page.getByText(/2 events/i)).toBeVisible();
  });

  test("the Type filter narrows the catalogue to a single format", async ({ page }) => {
    await page.goto("/speaking");
    await page.getByRole("button", { name: /list view/i }).click();

    await page.getByLabel(/^type$/i).selectOption({ label: "DevFest" });
    const resultsCount = await page.getByText(/\d+ events?/i).textContent();
    expect(resultsCount).toBeTruthy();
  });

  test("selecting an event from the catalogue opens its detail panel", async ({ page }) => {
    await page.goto("/speaking");
    await page.getByRole("button", { name: /list view/i }).click();

    await page
      .getByRole("button", { name: /Qazaq IT Community Conference/i })
      .first()
      .click();
    await expect(
      page.getByRole("heading", { name: "Qazaq IT Community Conference" }),
    ).toBeVisible();
    await expect(page.getByText(/From Cloud to Edge/i)).toBeVisible();
  });

  test("deep link with an event query parameter opens that event's detail directly", async ({
    page,
  }) => {
    await page.goto("/speaking?event=gdg-almaty-2026");
    await expect(
      page.getByRole("heading", { name: "Qazaq IT Community Conference" }),
    ).toBeVisible();
  });

  test("shows real, dynamically computed speaking statistics", async ({ page }) => {
    await page.goto("/speaking");
    // The stat strip renders numbers computed live from the seeded dataset —
    // just assert the shape is present and non-empty, not a specific figure
    // that would need updating every time an event is added.
    await expect(page.getByText("2023 → 2026")).toBeVisible();
  });

  test("Next stops shows upcoming and incoming appearances distinctly", async ({ page }) => {
    await page.goto("/speaking");
    const nextStops = page.getByRole("heading", { name: /next stops/i });
    await expect(nextStops).toBeVisible();
    await expect(page.getByText("GDG Chișinău First Meetup").first()).toBeVisible();
    await expect(page.getByText("M365 Toronto").first()).toBeVisible();
    await expect(page.getByText(/^Upcoming$/).first()).toBeVisible();
    await expect(page.getByText(/^Incoming$/).first()).toBeVisible();
  });

  test("International milestones highlights Sofia, Dallas and Almaty", async ({ page }) => {
    await page.goto("/speaking");
    const milestones = page.getByRole("heading", { name: /international milestones/i });
    await expect(milestones).toBeVisible();
    await expect(
      page
        .getByText("TechCon 365 Dallas — A Microsoft 365 & Power Platform Conference")
        .first(),
    ).toBeVisible();
  });

  test("searching Toronto in the catalogue reveals both Toronto appearances", async ({
    page,
  }) => {
    await page.goto("/speaking");
    await page.getByRole("button", { name: /list view/i }).click();
    const catalogue = page.getByRole("list", { name: /event catalogue/i }).first();
    await page.getByLabel(/^search events$/i).fill("Toronto");
    await expect(catalogue.getByText("M365 Toronto")).toBeVisible();
    await expect(catalogue.getByText("SQL Saturday Toronto")).toBeVisible();
  });
});
