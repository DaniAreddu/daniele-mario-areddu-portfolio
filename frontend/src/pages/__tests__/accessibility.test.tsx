import { configureAxe, toHaveNoViolations } from "jest-axe";
import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import ContactPage from "@/pages/ContactPage";
import HomePage from "@/pages/HomePage";
import SpeakingPage from "@/pages/SpeakingPage";
import { installFetchMock } from "@/test/mockApi";
import { renderWithProviders } from "@/test/testUtils";

expect.extend(toHaveNoViolations);

// The map's third-party tile layer and canvas are excluded: MapLibre isn't
// mounted in these tests (Home/Contact don't render it), and its canvas-based
// UI is verified separately by hand per docs/production-checklist.md.
const axe = configureAxe({});

describe("accessibility", () => {
  beforeEach(() => {
    installFetchMock();
  });

  it("Home page has no detectable axe violations", async () => {
    const { container } = renderWithProviders(<HomePage />, "/");
    await waitFor(() => expect(container.querySelector("h1")).toBeInTheDocument());
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("Contact page (with form) has no detectable axe violations", async () => {
    const { container } = renderWithProviders(<ContactPage />, "/contact");
    await waitFor(() => expect(container.querySelector("form")).toBeInTheDocument());
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  it("Speaking page (list view, stats, upcoming, milestones) has no detectable axe violations", async () => {
    const user = userEvent.setup();
    const { container } = renderWithProviders(<SpeakingPage />, "/speaking");
    await waitFor(() => expect(container.querySelector("h1")).toBeInTheDocument());
    // Switch to the accessible list view rather than mounting the real
    // MapLibre/WebGL map, which jsdom cannot render.
    await user.click(screen.getByRole("button", { name: /list view/i }));
    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });
});
