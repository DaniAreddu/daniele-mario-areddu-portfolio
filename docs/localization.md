# Localization strategy

## Routing

English is the default locale at unprefixed routes (`/`, `/about`, `/speaking`, ...).
Italian lives under a `/it` prefix (`/it`, `/it/about`, `/it/speaking`, ...). Both are
real, directly linkable, bookmarkable, and shareable routes — there is no
client-side-only language state that a URL can't capture.

This decision (over query-string or cookie-only locale switching) was made because it:

- gives every page a distinct, crawlable URL per language (see
  [seo-strategy.md](seo-strategy.md) for the resulting hreflang tags),
- works correctly with the Nginx static/prerendering setup (each locale's HTML can be
  pre-rendered independently), and
- matches how most large bilingual sites (and search engines) expect localized content
  to be organized.

Implementation: `frontend/src/app/LocaleContext.tsx` derives the active locale purely
from `location.pathname` (`/it` or `/it/...` → `it`, anything else → `en`) — there is
no separate router configuration to keep in sync. `frontend/src/app/router.tsx`
defines each route's element **once** and renders it under both the unprefixed and
`/it`-prefixed route trees, so no page's JSX/markup is duplicated per language.

## Persisting the choice

`LanguageSwitcher` writes the chosen locale to `localStorage` on every switch. A guard
in `LocaleContext` checks that value once, only when landing on the **bare** `/` root
(never on a specific deep link), and redirects to `/it` if Italian was last chosen.
Direct links to an explicit route in a specific language (e.g. someone sharing
`/about`) always render in that language, regardless of any stored preference — a
stored preference should never override an explicit URL.

## UI strings vs. content

Two separate localization mechanisms exist on purpose:

1. **UI chrome** (nav labels, buttons, form labels, aria-labels, validation
   messages) — `react-i18next`, with dictionaries in
   `frontend/src/i18n/locales/{en,it}.json`. These never change without a code
   change, so they're checked into the frontend.
2. **Portfolio content** (biography, project case studies, event descriptions,
   passions, community text) — stored per-locale in the database (`_en` / `_it`
   columns; see [data-model.md](data-model.md)) and served by the API based on the
   `lang` query parameter or `Accept-Language` header
   (`app/core/i18n.py::resolve_locale`). This is what "translate all significant
   content, not only navigation labels" means in practice: content editing (see
   [event-management.md](event-management.md)) always happens in one place —
   `backend/app/seed/data.py` — not scattered across React components.

## API locale resolution

`GET /api/v1/...?lang=it` takes precedence; if omitted, the `Accept-Language` header
is parsed and matched against the two supported locales; otherwise the API defaults to
English. Every localized endpoint's tests assert both paths (see
`backend/tests/test_profile_and_biography.py`).

## Dates

Dates are formatted client-side with `Intl.DateTimeFormat` (via
`toLocaleDateString`) using the active locale (`it-IT` / `en-US`), not hardcoded
strings — see `ExperiencePage.tsx` and `CommunityPage.tsx`.
