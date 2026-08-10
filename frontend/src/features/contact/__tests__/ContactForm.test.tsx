import { screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";

import { ContactForm } from "@/features/contact/ContactForm";
import { renderWithProviders, mockJsonResponse } from "@/test/testUtils";

describe("ContactForm", () => {
  const originalFetch = globalThis.fetch;

  afterEach(() => {
    globalThis.fetch = originalFetch;
    vi.restoreAllMocks();
  });

  it("shows validation errors when required fields are missing", async () => {
    const user = userEvent.setup();
    renderWithProviders(<ContactForm />);

    await user.click(screen.getByRole("button", { name: /send message/i }));

    expect(await screen.findAllByRole("alert")).not.toHaveLength(0);
  });

  it("submits successfully and shows a success message when email is delivered", async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValue(
        mockJsonResponse({ received: true, email_delivered: true }, 201),
      ) as unknown as typeof fetch;

    const user = userEvent.setup();
    renderWithProviders(<ContactForm />);

    await user.type(screen.getByLabelText(/^name$/i), "Jane Organizer");
    await user.type(screen.getByLabelText(/^email$/i), "jane@example.com");
    await user.type(
      screen.getByLabelText(/^message$/i),
      "We would love to invite Daniele to speak at our conference.",
    );
    await user.click(screen.getByLabelText(/agree/i));
    await user.click(screen.getByRole("button", { name: /send message/i }));

    expect(await screen.findByText(/message sent/i)).toBeInTheDocument();
    expect(globalThis.fetch).toHaveBeenCalledTimes(1);
  });

  it("shows the undelivered-email notice when the API accepts but cannot send email", async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValue(
        mockJsonResponse({ received: true, email_delivered: false }, 201),
      ) as unknown as typeof fetch;

    const user = userEvent.setup();
    renderWithProviders(<ContactForm />);

    await user.type(screen.getByLabelText(/^name$/i), "Jane Organizer");
    await user.type(screen.getByLabelText(/^email$/i), "jane@example.com");
    await user.type(
      screen.getByLabelText(/^message$/i),
      "A message long enough to pass validation.",
    );
    await user.click(screen.getByLabelText(/agree/i));
    await user.click(screen.getByRole("button", { name: /send message/i }));

    await waitFor(() => {
      expect(screen.getByRole("status")).toHaveTextContent(
        /email notification could not be delivered/i,
      );
    });
  });

  it("shows a rate-limit specific message on 429 responses", async () => {
    globalThis.fetch = vi
      .fn()
      .mockResolvedValue(
        mockJsonResponse(
          { error: { code: "rate_limited", message: "Too many requests." } },
          429,
        ),
      ) as unknown as typeof fetch;

    const user = userEvent.setup();
    renderWithProviders(<ContactForm />);

    await user.type(screen.getByLabelText(/^name$/i), "Jane Organizer");
    await user.type(screen.getByLabelText(/^email$/i), "jane@example.com");
    await user.type(
      screen.getByLabelText(/^message$/i),
      "A message long enough to pass validation.",
    );
    await user.click(screen.getByLabelText(/agree/i));
    await user.click(screen.getByRole("button", { name: /send message/i }));

    expect(await screen.findByText(/too many messages/i)).toBeInTheDocument();
  });
});
