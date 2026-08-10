import { defaultFormValues, formValuesToPayload } from "@/admin/pages/speaking/eventFormSchema";

describe("formValuesToPayload", () => {
  it("sends null (not 0) for optional numeric fields left empty", () => {
    // Regression test: z.coerce.number() turns "" into 0 (Number("") === 0),
    // not NaN, so an empty optional numeric field must be checked BEFORE
    // coercion is attempted — this previously sent talk_id: 0 to the
    // backend, which failed a foreign key constraint on every new draft.
    const values = defaultFormValues();
    const payload = formValuesToPayload(values);

    expect(payload.talk_id).toBeNull();
    expect(payload.month).toBeNull();
    expect(payload.latitude).toBeNull();
    expect(payload.longitude).toBeNull();
  });

  it("preserves real numeric values, including falsy-but-valid ones", () => {
    const values = { ...defaultFormValues(), latitude: 0, longitude: 0, month: 1 };
    const payload = formValuesToPayload(values);

    expect(payload.latitude).toBe(0);
    expect(payload.longitude).toBe(0);
    expect(payload.month).toBe(1);
  });

  it("splits comma-separated tags into a trimmed, non-empty list", () => {
    const values = { ...defaultFormValues(), tags_input: "AI,  Backend ,,Testing" };
    const payload = formValuesToPayload(values);

    expect(payload.tag_labels).toEqual(["AI", "Backend", "Testing"]);
  });

  it("converts blank optional text fields to null rather than empty strings", () => {
    const payload = formValuesToPayload(defaultFormValues());

    expect(payload.city).toBeNull();
    expect(payload.session_title).toBeNull();
    expect(payload.internal_notes).toBeNull();
  });
});
