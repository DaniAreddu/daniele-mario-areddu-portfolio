import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import { AdminToastProvider } from "@/admin/components/ui/Toast";
import SpeakingEditorPage from "@/admin/pages/speaking/SpeakingEditorPage";
import { mockJsonResponse } from "@/test/testUtils";

function renderEditor() {
  const client = new QueryClient({ defaultOptions: { queries: { retry: false } } });
  return render(
    <QueryClientProvider client={client}>
      <AdminToastProvider>
        <MemoryRouter initialEntries={["/admin/speaking/new"]}>
          <Routes>
            <Route path="/admin/speaking/new" element={<SpeakingEditorPage />} />
          </Routes>
        </MemoryRouter>
      </AdminToastProvider>
    </QueryClientProvider>,
  );
}

describe("SpeakingEditorPage — new appearance", () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    globalThis.fetch = vi.fn(async () => mockJsonResponse([])) as unknown as typeof fetch;
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("renders a coordinate preview without crashing once latitude/longitude are entered", async () => {
    // Regression test: react-hook-form's watch() returns number inputs as
    // strings, and the map-preview helper previously called .toFixed()
    // directly on that string, crashing the whole form (with no error
    // boundary at the time, the crash silently wiped all in-progress input).
    const user = userEvent.setup();
    renderEditor();

    await screen.findByRole("heading", { name: /new appearance/i });

    await user.type(screen.getByLabelText("Latitude"), "41.9028");
    await user.type(screen.getByLabelText("Longitude"), "12.4964");

    expect(await screen.findByText("41.9028, 12.4964")).toBeInTheDocument();
    // The event name field, filled earlier in the flow, must not have been
    // wiped by an unrelated crash/remount.
    await user.type(screen.getByLabelText("Event name"), "Regression Check");
    expect(screen.getByLabelText("Event name")).toHaveValue("Regression Check");
  });
});
