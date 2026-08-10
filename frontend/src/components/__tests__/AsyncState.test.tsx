import { fireEvent, render, screen } from "@testing-library/react";
import { I18nextProvider } from "react-i18next";

import i18n from "@/i18n";
import { ErrorState, LoadingState } from "@/components/AsyncState";

function withI18n(ui: React.ReactElement) {
  return <I18nextProvider i18n={i18n}>{ui}</I18nextProvider>;
}

describe("LoadingState", () => {
  it("announces loading status for assistive technology", () => {
    render(withI18n(<LoadingState />));
    expect(screen.getByRole("status")).toHaveTextContent(/loading/i);
  });
});

describe("ErrorState", () => {
  it("shows a retry button and calls the handler on click", () => {
    const onRetry = vi.fn();
    render(withI18n(<ErrorState onRetry={onRetry} />));
    expect(screen.getByRole("alert")).toBeInTheDocument();
    fireEvent.click(screen.getByRole("button", { name: /retry/i }));
    expect(onRetry).toHaveBeenCalledTimes(1);
  });

  it("omits the retry button when no handler is given", () => {
    render(withI18n(<ErrorState />));
    expect(screen.queryByRole("button")).not.toBeInTheDocument();
  });
});
