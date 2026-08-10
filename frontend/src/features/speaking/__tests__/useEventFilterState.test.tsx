import { act, renderHook } from "@testing-library/react";
import type { ReactNode } from "react";
import { MemoryRouter } from "react-router-dom";

import { useEventFilterState } from "@/features/speaking/useEventFilterState";

function wrapper({ children }: { children: ReactNode }) {
  return <MemoryRouter initialEntries={["/speaking?year=2025"]}>{children}</MemoryRouter>;
}

describe("useEventFilterState", () => {
  it("reads initial filter state from the URL", () => {
    const { result } = renderHook(() => useEventFilterState(), { wrapper });
    expect(result.current.state.year).toBe(2025);
    expect(result.current.hasActiveFilters).toBe(true);
  });

  it("sets and clears a filter", () => {
    const { result } = renderHook(() => useEventFilterState(), { wrapper });

    act(() => result.current.setFilter("continent", "Asia"));
    expect(result.current.state.continent).toBe("Asia");

    act(() => result.current.setFilter("continent", undefined));
    expect(result.current.state.continent).toBeUndefined();
  });

  it("selects an event without disturbing other filters", () => {
    const { result } = renderHook(() => useEventFilterState(), { wrapper });

    act(() => result.current.selectEvent("gdg-almaty-2026"));
    expect(result.current.state.event).toBe("gdg-almaty-2026");
    expect(result.current.state.year).toBe(2025);
  });

  it("clearFilters removes filters but keeps the event selection untouched", () => {
    const { result } = renderHook(() => useEventFilterState(), { wrapper });

    act(() => result.current.selectEvent("gdg-almaty-2026"));
    act(() => result.current.clearFilters());

    expect(result.current.state.year).toBeUndefined();
    expect(result.current.hasActiveFilters).toBe(false);
    expect(result.current.state.event).toBe("gdg-almaty-2026");
  });
});
