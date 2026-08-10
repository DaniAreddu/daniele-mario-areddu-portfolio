# Admin guide

The `/admin` area is the private webmaster interface for this portfolio, being built
incrementally on top of the same backend and frontend (see
[architecture.md](architecture.md)). This document covers what exists today and is
extended as each phase ships — see the "Status" note at the top of each section.

## Status

- ✅ Authentication: email + Argon2id password, optional TOTP two-factor, server-side
  sessions, audit logging, CLI bootstrap/recovery.
- ✅ Speaking (`/admin/speaking`) and Projects (`/admin/projects`): full draft →
  preview → publish → schedule → unpublish → archive → trash → restore lifecycle,
  revision history with restore, an admin-managed tag vocabulary shared across
  content types (Speaking also has duplicate-appearance detection).
- ✅ Experience (`/admin/experience`) and Education (`/admin/education`): the same
  lifecycle/revision pattern (Experience also shares the Tag vocabulary).
- ✅ Community (`/admin/community`): activities follow the full lifecycle pattern;
  the community profile (`/admin/community/profile`) is a singleton, always-live,
  no draft state (edited directly, revisions still recorded).
- ✅ Recognition (`/admin/recognition`): certifications/awards/recognition/publications
  in one lifecycle-enabled table, distinguished by a `kind` field.
- ✅ Profile (`/admin/profile`) and Biography (`/admin/biography`): singletons, same
  pattern as the community profile.
- ✅ Skills (`/admin/skills`): categories and skills are plain CRUD with an `enabled`
  switch — no draft/publish lifecycle, since a skill list is a structured settings
  page, not long-form content (see "Extending to a new content type" for when a
  content type should skip the lifecycle machinery entirely).
- ✅ Media library (`/admin/media`): upload (JPEG/PNG/WEBP/GIF, validated by
  decoding — never by trusting the filename or `Content-Type`), automatic
  thumbnail/medium variants, alt text/caption editing, usage-aware delete (warns
  and requires confirmation before deleting a file referenced by other content).
  See "Media library" below.
- ✅ Site administration (`/admin/navigation`, `/admin/social-links`,
  `/admin/redirects`, `/admin/site-settings`, `/admin/seo-settings`,
  `/admin/homepage`): see "Site administration" below.
- ✅ Dashboard (`/admin`), global search (Ctrl/Cmd+K from anywhere in the admin
  area), audit log browser (`/admin/audit-log`), and system health
  (`/admin/system`): see "Dashboard, search, audit log, and system health" below.

## Extending to a new content type

Every content vertical (Speaking, Projects, and whatever comes next) follows the
same shape — read `app/services/event_admin_service.py` and
`app/api/v1/admin_events.py` as the reference implementation:

1. Add `PublishableMixin` and `SoftDeleteMixin` to the model, plus `internal_notes`
   and (if the content has a free-text category/topic list worth normalizing) a
   `<entity>_tag` association table reusing the shared `Tag` model.
2. Write a migration: add the new columns with `server_default='PUBLISHED'` (so
   existing rows stay visible), create the association table, and backfill any
   existing free-text list into `Tag` rows — mirror `0004`/`0005`.
3. Add `visible_now(Model)` to every public repository query; add
   `list_all_admin()`/`get_by_id()`/`get_by_slug_any()`/`create()`/`delete()` for
   admin use.
4. Add `<Entity>AdminCreate`/`<Entity>AdminUpdate` (content fields only — never
   `publication_status`/`deleted_at`, which is what makes the lifecycle endpoints a
   mass-assignment guard, not just a convenience) and `<Entity>AdminOut` schemas.
5. Add the admin service: CRUD + the six lifecycle methods
   (publish/schedule/unpublish/archive/soft_delete/restore_from_trash) built on the
   shared `_admin_common.py` helpers (`create_revision`, `record_audit_event`,
   `merge_revision_snapshot`), plus `list_revisions`/`restore_revision`.
6. Add the admin router under `/api/v1/admin/<entities>`, wire it into
   `app/api/v1/__init__.py`.
7. Update `app/seed/seed.py`'s `_seed_<entity>` to set
   `item.setdefault("publication_status", "PUBLISHED")` so seeded rows stay public.
8. Frontend: a list page (`useAdmin<Entity>List`), a sectioned editor form
   (Zod schema + `react-hook-form`, following `eventFormSchema.ts`'s
   empty-string-vs-zero-coercion pattern for optional numeric fields — see the
   regression test in `eventFormSchema.test.ts` for exactly why the union order
   matters), and a preview page. Add the routes to `AdminApp.tsx` and the nav
   entry to `AdminLayout.tsx`.
9. Write the admin test file mirroring `test_admin_events.py`, **including its
   cleanup fixture** — the test database is shared across the whole suite, so any
   content created by admin tests must delete its own rows (and their
   `Revision`/`AuditEvent` rows) afterward or it will corrupt other tests' counts.

## Media library

Upload images from `/admin/media`. Validation is intentionally never based on the
client-supplied filename or `Content-Type` header — the backend decodes every
upload with Pillow and rejects anything that isn't a real JPEG/PNG/WEBP/GIF (this
also catches disguised files and most decompression-bomb attempts, since Pillow's
default `MAX_IMAGE_PIXELS` guard is left on). Two smaller variants (`thumbnail`,
`medium`) are generated automatically as WEBP; the original is stored unmodified.

Every stored file gets a server-generated key (`uuid4().hex` plus an extension) —
**never** derived from the original filename — which is what makes the public
`GET /api/v1/media/{key}` route safe to leave unauthenticated: the key itself is
the access control (unguessable, no path-traversal surface since it never contains
user input), and the original filename is kept purely as display metadata. Files
live outside PostgreSQL in a dedicated Docker volume (`media-data`), never as
database blobs.

Deleting a file checks whether any other content still references its URL (project
cover images, event images, experience/education logos) and requires an explicit
"delete anyway" confirmation if so, rather than silently breaking a live page.

## Site administration

These screens replace hand-editing source code for the handful of settings/content
sections needed to stand up the public site end to end:

- **Navigation** (`/admin/navigation`) — header and footer links in one list,
  distinguished by a `placement` field. Each item has separate English/Italian
  labels (`label_en`/`label_it`, matching the bilingual-column convention used
  everywhere else) and a `target` that must be an internal path (starting with
  `/`) unless `is_external` is checked, in which case it must be a full
  `http(s)://` URL — enforced server-side, not just in the form.
- **Social links** (`/admin/social-links`) — shown in the site footer. The `icon`
  field is checked against a small fixed allow-list (`github`, `linkedin`,
  `twitter`, `mastodon`, `youtube`, `instagram`, `rss`, `mail`, `globe`,
  `sessionize`) that matches the frontend's icon lookup table — an unrecognized
  name is rejected at write time rather than silently rendering nothing.
- **Redirects** (`/admin/redirects`) — both the source and destination path must be
  internal (start with `/`); there is no way to configure a redirect to an
  external domain, which removes open-redirect risk by construction rather than
  by allow-listing hosts. Creating or editing a redirect is also checked against
  every existing redirect for a loop (including indirect chains up to 20 hops) and
  against duplicate source paths, both rejected before they reach the database.
- **Site settings** (`/admin/site-settings`) — a singleton: site name, default
  timezone/language, a maintenance-mode flag, and the boolean switches that decide
  whether the speaking map, statistics, "now" section, projects, and community
  sections appear on the public site at all.
- **SEO settings** (`/admin/seo-settings`) — a singleton: default page title
  template, default meta description, default Open Graph image, Twitter card
  type, default `robots` directive, and canonical base URL. These are global
  fallbacks; the frontend's `useSeo` hook still lets any individual page set its
  own title/description/image, which take precedence.
- **Homepage** (`/admin/homepage`) — a singleton for the hero copy (eyebrow,
  headline, subheadline, both languages), the two call-to-action buttons, and
  which page sections are visible; plus a **featured items** list that pins
  specific published projects or speaking appearances to the homepage by id
  (validated to exist, and resolved against each entity's normal public
  visibility rules — an item that's later unpublished or trashed simply
  disappears from the homepage response rather than leaking draft content or
  erroring).

All six are plain create/update/delete operations with audit logging but no
draft/publish lifecycle — see "Extending to a new content type" above for when a
content type should skip the six-lifecycle-endpoint pattern entirely (a nav link
or a redirect has no meaningful "draft" state distinct from "not created yet").

## Dashboard, search, audit log, and system health

- **Dashboard** (`/admin`) — real, computed-on-demand counts (never cached or
  hardcoded) of published/draft/scheduled/archived/trashed items per content
  type, plus upcoming speaking appearances, total media files, and a recent
  activity feed pulled from the audit log.
- **Global search** — press **Ctrl+K** (or **Cmd+K** on macOS) anywhere in the
  admin area to open a command palette that searches across every content type,
  media filenames, navigation items, and social links by a simple substring
  match. Results link straight to each item's editor. This is an admin-only,
  authenticated endpoint — it can (deliberately) surface drafts, since finding
  your own unpublished work is the point.
- **Audit log** (`/admin/audit-log`) — every administrative mutation (not just
  content — logins, 2FA changes, everything), filterable by content type, newest
  first. Also lists the most recent revisions (point-in-time content snapshots)
  across every content type.
- **System health** (`/admin/system`) — a quick operational glance: database
  connectivity, whether the database's applied Alembic migration matches the
  code's expected migration head, and whether the media storage backend is
  writable. Deliberately never renders a connection string, key, or other secret
  value — only booleans and short status labels.

## Creating the first administrator

There is no sign-up page and no default admin account. Create the first (or an
additional) administrator from the backend container:

```bash
docker compose exec backend uv run python -m app.cli create-admin
# or, without Docker: uv run python -m app.cli create-admin (from backend/)
```

You'll be prompted for an email and a password (minimum 12 characters, entered
twice to confirm). The account is created with role `OWNER`. Sign in at
`https://<your-domain>/admin` — always through the Nginx gateway, never by
connecting to the backend or the Vite dev server directly (see "Local development"
below for why that matters).

## Signing in

Sign-in is a two-step flow whenever two-factor authentication is enabled on the
account:

1. Email + password.
2. If TOTP is enabled, a 6-digit authenticator code (or a one-time recovery code).

Failed attempts are rate-limited both at the application level (per email + IP, a
generic "invalid email or password" error regardless of which factor was wrong) and
at the Nginx gateway (a dedicated, stricter rate-limit zone on the
login/2FA-verification endpoints). Sessions are server-side rows, identified by an
`HttpOnly`, `Secure` (in production), `SameSite=Strict` cookie — the raw session
token is never stored anywhere, only its hash, and it is never accessible to
JavaScript or persisted in `localStorage`.

## Enabling two-factor authentication

From **Security** in the admin sidebar:

1. **Enable two-factor authentication** — generates a QR code (scan with any
   TOTP-compatible authenticator app: Google Authenticator, 1Password, Authy, etc.)
   and shows the secret as text for manual entry.
2. Enter the 6-digit code your app produces to confirm enrollment.
3. You'll be shown **10 recovery codes once** — save them somewhere safe (a password
   manager). Each can be used exactly once in place of a TOTP code if you lose access
   to your authenticator app. They are never shown again; regenerating produces a
   fresh set and invalidates the old ones.

TOTP secrets are encrypted at rest (Fernet, `ADMIN_TOTP_ENCRYPTION_KEY`) — see
"Environment variables" below. Recovery codes are hashed individually, the same way
session tokens are; a leaked database backup cannot be used to derive working codes.

## Recovering access

**Forgot your password?** From the backend container:

```bash
docker compose exec backend uv run python -m app.cli reset-password
```

Prompts for the account's email and a new password, then revokes every active
session for that account (so a lost/stolen session cookie stops working
immediately).

**Lost your authenticator device and have no recovery codes?** Add `--disable-totp`
to the same command:

```bash
docker compose exec backend uv run python -m app.cli reset-password --disable-totp
```

This resets the password **and** disables two-factor authentication on the account,
so you can sign back in with just the new password and re-enroll TOTP afterward.
There is no email-based password reset — for a single-operator portfolio, this
CLI-based recovery (which requires shell access to the running backend, i.e. the
same trust level as deploying the app at all) is the appropriate mechanism rather
than standing up outbound-email infrastructure just for this.

## Disabling two-factor authentication

From **Security**, enter your current password under "Disable two-factor
authentication." This immediately clears the stored (encrypted) secret and all
recovery codes.

## Environment variables

| Variable | Purpose | Notes |
|---|---|---|
| `ADMIN_TOTP_ENCRYPTION_KEY` | Encrypts TOTP secrets at rest (Fernet) | The repository ships a published dev-only default — **generate a real one** for any non-dev deployment: `python -c "from cryptography.fernet import Fernet as F; print(F.generate_key().decode())"`. Rotating this key invalidates every enrolled account's TOTP secret (they'd need to re-enroll). |
| `ADMIN_SESSION_TTL_HOURS` | How long an authenticated session lasts | Default 12 hours. |
| `ADMIN_LOGIN_RATE_LIMIT_PER_HOUR` | App-level login throttling | Default 10 failed attempts/hour per email+IP. |

None of these are ever returned by any API response — secrets stay in environment
variables, never in a settings table served to the frontend.

## Local development note

The dev Docker Compose stack exposes the Vite dev server on `:5173` and the backend
directly on `:8080` (via the gateway) — **always develop against the gateway
(`http://localhost:8080/admin`)**, not `:5173` or `:8000` directly. Those ports are
genuinely cross-origin from the API's perspective, and the session cookie's
`SameSite=Strict` attribute will silently fail to be sent there — login will appear
to succeed but the next request won't carry the cookie. This is intentional (the
gateway making frontend and backend same-origin is what makes `SameSite=Strict`
possible at all) and documented here rather than "fixed" by loosening the cookie
policy.

## Security model summary

- Passwords: Argon2id.
- Sessions: opaque random tokens, SHA-256-hashed before storage, revocable, expiring.
- Two-factor: TOTP (RFC 6238) with encrypted-at-rest secrets and single-use hashed
  recovery codes; login only completes after both factors pass (a
  password-verified-but-not-yet-2FA-verified session grants nothing).
- CSRF: `SameSite=Strict` cookie plus a required custom header on every mutating
  request — sufficient for a same-origin SPA with no third-party embeds, without the
  added complexity of a double-submit token.
- Authorization is enforced server-side on every `/api/v1/admin/*` route
  (`get_current_admin_user`) — the admin UI hiding a button is never the actual
  security boundary.
- All administrative actions (sign-in/out, 2FA changes, and every content
  mutation) are recorded in an audit log, viewable and filterable from
  `/admin/audit-log`. Passwords, session tokens, TOTP secrets, and recovery codes
  are never logged or audited in plaintext.
