# Admin guide

The `/admin` area is the private webmaster interface for this portfolio, being built
incrementally on top of the same backend and frontend (see
[architecture.md](architecture.md)). This document covers what exists today and is
extended as each phase ships — see the "Status" note at the top of each section.

## Status

- ✅ Authentication: email + Argon2id password, optional TOTP two-factor, server-side
  sessions, audit logging, CLI bootstrap/recovery.
- ✅ Speaking (`/admin/speaking`): full draft → preview → publish → schedule →
  unpublish → archive → trash → restore lifecycle, revision history with restore,
  duplicate-appearance detection, an admin-managed tag vocabulary shared across
  content types.
- ✅ Projects (`/admin/projects`): the same lifecycle/revision/tag pattern as
  Speaking, applied to project case studies.
- 🚧 Experience, Education, Skills, Community, Biography, Recognition follow the
  identical, now-proven pattern (see "Extending to a new content type" below) but
  are not yet built. Media library and site administration (homepage, navigation,
  SEO, redirects, settings) are designed but not yet built. This document grows a
  section for each as it lands.

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
- All administrative actions (sign-in/out, 2FA changes, and — from the Speaking
  module onward — every content mutation) are recorded in an audit log, viewable
  from the admin UI once that screen ships. Passwords, session tokens, TOTP secrets,
  and recovery codes are never logged or audited in plaintext.
