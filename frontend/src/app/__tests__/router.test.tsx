import { screen } from "@testing-library/react";

import { AppRouter } from "@/app/router";
import { installFetchMock } from "@/test/mockApi";
import { renderWithProviders } from "@/test/testUtils";

describe("AppRouter", () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    installFetchMock();
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("renders the home page at the root route", async () => {
    renderWithProviders(<AppRouter />, "/");
    expect(await screen.findByText(/Building intelligent systems/i)).toBeInTheDocument();
  });

  it("renders the Italian home page under /it and sets html lang", async () => {
    renderWithProviders(<AppRouter />, "/it");
    await screen.findByText(/Building intelligent systems/i);
    expect(document.documentElement.lang).toBe("it");
  });

  it("renders a custom 404 page for unknown routes", async () => {
    renderWithProviders(<AppRouter />, "/this-route-does-not-exist");
    expect(await screen.findByText(/404/)).toBeInTheDocument();
  });

  it("supports direct navigation to a nested route", async () => {
    renderWithProviders(<AppRouter />, "/about");
    expect(await screen.findByRole("heading", { level: 1 })).toBeInTheDocument();
  });
});
