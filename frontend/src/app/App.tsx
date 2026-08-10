import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";

import { AppRouter } from "@/app/router";
import { LocaleProvider } from "@/app/LocaleContext";
import "@/i18n";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
      staleTime: 60_000,
    },
  },
});

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <LocaleProvider>
          <AppRouter />
        </LocaleProvider>
      </BrowserRouter>
    </QueryClientProvider>
  );
}
