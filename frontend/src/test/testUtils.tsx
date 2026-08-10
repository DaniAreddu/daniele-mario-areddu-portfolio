import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render } from "@testing-library/react";
import type { ReactElement, ReactNode } from "react";
import { MemoryRouter } from "react-router-dom";

import { LocaleProvider } from "@/app/LocaleContext";
import "@/i18n";

export function createTestQueryClient() {
  return new QueryClient({
    defaultOptions: {
      queries: { retry: false, gcTime: 0 },
      mutations: { retry: false },
    },
  });
}

interface WrapperProps {
  children: ReactNode;
  route?: string;
}

export function AllProviders({ children, route = "/" }: WrapperProps) {
  const client = createTestQueryClient();
  return (
    <QueryClientProvider client={client}>
      <MemoryRouter initialEntries={[route]}>
        <LocaleProvider>{children}</LocaleProvider>
      </MemoryRouter>
    </QueryClientProvider>
  );
}

export function renderWithProviders(ui: ReactElement, route = "/") {
  return render(ui, {
    wrapper: ({ children }) => <AllProviders route={route}>{children}</AllProviders>,
  });
}

export function mockJsonResponse(body: unknown, status = 200): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { "Content-Type": "application/json" },
  });
}
