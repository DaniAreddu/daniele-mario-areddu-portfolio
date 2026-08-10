import { render, screen } from "@testing-library/react";
import { configureAxe, toHaveNoViolations } from "jest-axe";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import AdminApp from "@/admin/AdminApp";
import { mockJsonResponse } from "@/test/testUtils";

expect.extend(toHaveNoViolations);
const axe = configureAxe();

describe("admin accessibility", () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    globalThis.fetch = vi.fn(async () =>
      mockJsonResponse({ error: { code: "unauthorized" } }, 401),
    ) as unknown as typeof fetch;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("Login page has no detectable axe violations", async () => {
    const { container } = render(
      <MemoryRouter initialEntries={["/admin/login"]}>
        <Routes>
          <Route path="admin/*" element={<AdminApp />} />
        </Routes>
      </MemoryRouter>,
    );
    await screen.findByRole("heading", { name: /sign in/i });

    expect(await axe(container)).toHaveNoViolations();
  });
});
