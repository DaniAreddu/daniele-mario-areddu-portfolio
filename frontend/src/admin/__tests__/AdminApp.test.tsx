import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter, Route, Routes } from "react-router-dom";

import AdminApp from "@/admin/AdminApp";
import { mockJsonResponse } from "@/test/testUtils";

type Handler = () => Response | Promise<Response>;

function mockAdminFetch(handlers: Record<string, Handler>) {
  globalThis.fetch = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
    const url = typeof input === "string" ? input : input.toString();
    const path = url
      .replace(window.location.origin, "")
      .split("?")[0]
      .replace("/api/v1/admin", "");
    const method = (init?.method ?? "GET").toUpperCase();
    const key = `${method} ${path}`;
    const handler = handlers[key];
    if (!handler) {
      return mockJsonResponse({ error: { code: "not_found", message: "Not found" } }, 404);
    }
    return handler();
  }) as unknown as typeof fetch;
}

const SAMPLE_USER = { id: 1, email: "daniele@areddu.it", role: "OWNER", totp_enabled: false };

function renderAdminApp(route: string) {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false }, mutations: { retry: false } },
  });
  return render(
    <QueryClientProvider client={queryClient}>
      <MemoryRouter initialEntries={[route]}>
        <Routes>
          <Route path="admin/*" element={<AdminApp />} />
        </Routes>
      </MemoryRouter>
    </QueryClientProvider>,
  );
}

describe("AdminApp", () => {
  const originalFetch = globalThis.fetch;

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it("redirects an unauthenticated visitor from /admin to the login page", async () => {
    mockAdminFetch({
      "GET /auth/me": () => mockJsonResponse({ error: { code: "unauthorized" } }, 401),
    });

    renderAdminApp("/admin");

    expect(await screen.findByRole("heading", { name: /sign in/i })).toBeInTheDocument();
  });

  it("shows validation errors for an empty submission", async () => {
    mockAdminFetch({
      "GET /auth/me": () => mockJsonResponse({ error: { code: "unauthorized" } }, 401),
    });
    const user = userEvent.setup();

    renderAdminApp("/admin/login");
    await screen.findByRole("heading", { name: /sign in/i });

    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByText(/enter a valid email address/i)).toBeInTheDocument();
  });

  it("logs in and reaches the dashboard when no second factor is required", async () => {
    let meCallCount = 0;
    mockAdminFetch({
      "GET /auth/me": () => {
        meCallCount += 1;
        return meCallCount === 1
          ? mockJsonResponse({ error: { code: "unauthorized" } }, 401)
          : mockJsonResponse(SAMPLE_USER);
      },
      "POST /auth/login": () => mockJsonResponse({ status: "authenticated" }),
    });
    const user = userEvent.setup();

    renderAdminApp("/admin/login");
    await screen.findByRole("heading", { name: /sign in/i });

    await user.type(screen.getByLabelText(/email/i), "daniele@areddu.it");
    await user.type(screen.getByLabelText(/password/i), "correct-horse-battery-staple");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(await screen.findByRole("heading", { name: /welcome back/i })).toHaveTextContent(
      "daniele@areddu.it",
    );
  });

  it("requires a second factor when the account has TOTP enabled", async () => {
    let meCallCount = 0;
    mockAdminFetch({
      "GET /auth/me": () => {
        meCallCount += 1;
        return meCallCount === 1
          ? mockJsonResponse({ error: { code: "unauthorized" } }, 401)
          : mockJsonResponse({ ...SAMPLE_USER, totp_enabled: true });
      },
      "POST /auth/login": () => mockJsonResponse({ status: "mfa_required" }),
      "POST /auth/totp/verify": () => mockJsonResponse({ status: "authenticated" }),
    });
    const user = userEvent.setup();

    renderAdminApp("/admin/login");
    await screen.findByRole("heading", { name: /sign in/i });

    await user.type(screen.getByLabelText(/email/i), "daniele@areddu.it");
    await user.type(screen.getByLabelText(/password/i), "correct-horse-battery-staple");
    await user.click(screen.getByRole("button", { name: /sign in/i }));

    expect(
      await screen.findByRole("heading", { name: /enter your authentication code/i }),
    ).toBeInTheDocument();

    await user.type(screen.getByLabelText(/6-digit code/i), "123456");
    await user.click(screen.getByRole("button", { name: /verify/i }));

    await waitFor(() => expect(screen.getByText(/welcome back/i)).toBeInTheDocument());
  });
});
