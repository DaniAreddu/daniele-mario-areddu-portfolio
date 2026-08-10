# Event management guide

Speaking events are now primarily managed through the admin UI at
`/admin/speaking` (see [admin-guide.md](admin-guide.md)) — draft, preview,
publish, schedule, and revision history are all handled there without touching
source code. `backend/app/seed/data.py` remains the origin of the initial
dataset and is still the right tool for bulk/scripted changes or re-seeding a
fresh environment; this document describes the conventions that apply either
way (the admin UI enforces the same field constraints). As of this writing the
seeded dataset covers 32 appearances from 2023 to 2026 across 10 countries and 3
continents (Europe, North America, Central Asia) — see `GET /api/v1/events/stats`
for the live, computed figures.

## Adding a new event via the seed file

1. Open `backend/app/seed/data.py` and find the `EVENTS` list.
2. Add a new entry using the `_event(...)` helper:

   ```python
   _event(
       "your-event-slug-2027", "Your Event Name",
       year=2027, month=4, city="Turin", country="Italy", continent="Europe",
       start_date=date(2027, 4, 10), format="conference",
   ),
   ```

3. **Only** set `city` to a value in `CITY_COORDINATES` if you also want it plotted
   on the map — coordinates are looked up from that fixed dictionary and are never
   geocoded automatically. If the city isn't in the dictionary yet, add its
   `[lat, lon]` there first, from a source you trust (never guessed).
4. Prefer `month=` over a guessed `start_date` when only the month is confirmed
   (e.g. "September 2026") — the model has a dedicated nullable `month` column for
   exactly this. Passing `start_date` automatically fills `month` too. Leave
   `start_date`/`month`, `city`, `country`, `continent`, `venue`, `event_url`,
   `slides_url`, `recording_url` as `None`/omitted for anything not yet confirmed.
   The API and frontend both handle `None` gracefully (fields are simply omitted
   from the UI — never a visible "TBD").
5. Set `status=` explicitly for anything that hasn't happened yet:
   `"upcoming"` or `"incoming"` (both render as a distinct badge — see
   `frontend/src/features/speaking/StatusBadge.tsx`). The default, `"completed"`,
   is for past engagements. Status is **never** inferred from today's date; it is
   always set by hand based on what is actually known.
6. If the event has a known, reusable talk title, add it to `TALKS` first and pass
   its slug as `talk_slug=` to `_event(...)`. Do **not** invent a session title for
   an event where only the event name is confirmed.
7. Set `is_international_milestone=True` **only** for the small, curated set of
   appearances that mark a genuine first step into a new country or region (see
   "International milestones" below) — this is deliberately not automatic.
8. Run the seed:

   ```bash
   make seed
   # or: docker compose exec backend uv run python -m app.seed.seed
   ```

   The seed matches existing rows by `slug` and updates them in place — safe to
   re-run, and safe to edit an existing event's fields and re-seed.

## Avoiding duplicate records

Before adding an event, search `EVENTS` for existing entries at the same city/year —
two names can refer to the same appearance. Two real examples handled this way in the
current dataset:

- **"Nerdearla Madrid" vs. "Nerdearla España 2025"** — the same appearance, described
  two different ways. Kept as a single row (`nerdearla-madrid-2025`), with
  `event_name` updated to the more complete/official "Nerdearla España 2025". The slug
  was **not** renamed to match, specifically to avoid ever having two rows for one
  appearance.
- **"GDG Almaty" vs. "Qazaq IT Community Conference"** — the original seed only had a
  generic GDG-branded name for an Almaty appearance; a later, more complete brief
  identified it as the official "Qazaq IT Community Conference" (same city, same date,
  same talk). Rather than adding a second Almaty row, the existing `gdg-almaty-2026`
  row's `event_name` and `event_url` were updated in place.

If you're ever unsure whether two descriptions refer to the same appearance, prefer
updating the existing row over adding a new one — a slug is an internal identifier,
not user-facing, so it never needs to match the current display name.

## International milestones

`is_international_milestone` drives the "International milestones" showcase on the
Speaking page — a deliberately small, curated set distinct from `is_featured` (which
highlights notable *session content*, not geography). As of this writing:

Tirana (Power Platform User Group Albania), Bucharest (OmniOpenCon), Dallas
(TechCon 365), Madrid (Nerdearla España), Sofia (AgentCamp), New York (AI Community
Conference), Bishkek (GDG Bishkek), Almaty (Qazaq IT Community Conference).

Not every international event gets this treatment — only ones that represent a real
first step into a country/region. Keep this list short; the hierarchy is the point.

## Fields that must stay nullable

`start_date`, `month`, `end_date`, `city`, `country`, `continent`, `latitude`,
`longitude`, `venue`, `event_url`, `slides_url`, `recording_url`, `image`, and
`session_title` are all nullable on the `Event` model because several real events in
this portfolio have genuinely incomplete public information. Current examples (as of
this writing):

- **Confirmed year and month, no exact day**: most 2025–2026 events (e.g. DevFest
  Ponferrada, OmniOpenCon, GDG Chișinău First Meetup, M365 Toronto, SQL Saturday
  Toronto, Data Saturday Sofia).
- **Confirmed year only, no month/day**: BSides NOVA.
- **Nothing beyond the name/year confirmed, no known city**: SQL Start! and
  1nn0vAI both had this gap in an earlier draft of the dataset and were later
  confirmed (Ancona and Pordenone respectively) — a reminder that "currently
  unknown" fields should be revisited as more information becomes available, not
  left stale forever.

Never fill these in with a plausible-looking guess — leave them `None`/omitted and let
the UI omit them.

## Verifying the map/GeoJSON/stats after a change

```bash
curl "http://localhost:8000/api/v1/events/geojson" | python -m json.tool
curl "http://localhost:8000/api/v1/events/stats" | python -m json.tool
```

Only events with both `latitude` and `longitude` set appear in the `FeatureCollection`
— confirmed by `backend/tests/test_events_and_geojson.py`. The stats endpoint recomputes
every figure (total appearances, countries, cities, continents, first/last year,
international count, upcoming count, GDG/DevFest count) live from the seeded rows —
nothing in `EventStatsOut` is a hardcoded number, so it can never silently drift from
what's actually in `EVENTS`.

## Country → continent grouping

Continents are set explicitly per event, not derived from country automatically.
Kazakhstan and Kyrgyzstan are grouped as `"Central Asia"`, not `"Asia"` or `"Europe"` —
this is a presentation choice specific to this portfolio's speaking-expansion story
(see `docs/data-model.md`), so keep it consistent when adding future Central Asian
events.
