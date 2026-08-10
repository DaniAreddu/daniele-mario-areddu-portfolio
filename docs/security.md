# Security considerations

## Transport & edge

- The Nginx **gateway** is the only container with a published port; the frontend,
  backend, database, and Mailpit are reachable only over the internal Docker network
  (`docker-compose.prod.yml` publishes no ports for them at all).
- The gateway sets `X-Content-Type-Options`, `X-Frame-Options: DENY`,
  `Referrer-Policy`, `Permissions-Policy`, and a `Content-Security-Policy` on every
  response (`nginx/gateway.conf`). The CSP allows only `'self'` plus the two external
  origins actually used: the MapLibre tile host and Google Fonts.
- TLS termination is intentionally not baked into this repo (see
  [production-checklist.md](production-checklist.md)) — no domain or certificate
  authority was provided to configure it against.
- Trusted-proxy handling: the gateway is the network edge, so `$remote_addr` is the
  real client IP; `nginx/gateway.conf` documents exactly what to change
  (`set_real_ip_from`) if another load balancer/CDN is ever placed in front of it.
  On the backend side, `app/core/client_ip.py::get_client_ip` reads the real
  visitor IP from `X-Forwarded-For` (set by the gateway's `proxy-common.conf`)
  rather than the raw socket peer — since every request reaches the API through
  the gateway, `request.client.host` alone would always resolve to the gateway
  container's own address, collapsing every distinct visitor into one IP for
  rate-limiting purposes. This was caught during Docker-based end-to-end
  verification, where it manifested as legitimate contact submissions being
  rate-limited after a handful of unrelated requests.

## Application

- **CORS** is configurable via `CORS_ORIGINS` and defaults to the local dev origins
  only — must be tightened to the real production origin (see the checklist).
- **Input validation** is enforced twice: Zod on the frontend (fast feedback) and
  Pydantic on the backend (the actual trust boundary — the frontend's validation is a
  UX nicety, not a security control).
- **Rate limiting** is layered: Nginx (`limit_req`, edge-level, IP-based) and an
  application-level check in `ContactService` (hashed-IP, per-hour). See
  [contact-flow.md](contact-flow.md).
- **Honeypot** protects the contact form from unsophisticated bots without a CAPTCHA
  (which would hurt UX for legitimate speaking invitations).
- **Consistent error envelopes** (`app/core/errors.py`) never leak stack traces,
  internal paths, or exception details to the client — unhandled exceptions are
  logged server-side and returned as a generic `internal_error`.
- **`TrustedHostMiddleware`** guards against Host-header attacks; tighten
  `TRUSTED_HOSTS` from `*` to the real production host(s) in production.

## Data

- Contact submissions are **never exposed via any public read endpoint** — there is
  no `GET` route for `ContactSubmission` at all, by design.
- Source IPs on contact submissions are stored as a SHA-256 hash, not plaintext,
  sufficient for rate-limiting logic without retaining a directly identifiable IP
  address.
- Logs never contain the contact message body, name, or email address (see
  `ContactService.submit`'s `logger.info` call) — only the request type and delivery
  outcome.
- No secrets are committed: `.env` is gitignored at the root and in both `backend/`
  and `frontend/`; only `.env.example` files (no real credentials) are tracked.

## Containers

- All three custom images (backend, frontend, gateway) run as a **non-root** `app`
  user.
- Production containers run with `read_only: true` root filesystems plus narrow
  `tmpfs` mounts only where a process genuinely needs to write at runtime (Nginx's
  PID file and cache directories; the gateway's templated config directory — see the
  comment in `docker-compose.prod.yml`).
- Multi-stage Dockerfiles mean no build tools, dev dependencies, or source `.git`
  history end up in the production image layers.

## Dependency hygiene

- `backend/uv.lock` and `frontend/package-lock.json` are committed for reproducible
  installs.
- CI runs `pip-audit` (backend) and `npm audit` (frontend) — see
  `.github/workflows/backend.yml` / `frontend.yml`. Both are currently
  `continue-on-error` so a new advisory doesn't block every PR, but findings should
  be triaged, not ignored.

## Known limitations to review before launch

- No automated dependency-update bot (e.g. Dependabot/Renovate) is configured —
  worth adding.
- No Web Application Firewall in front of the gateway — evaluate based on the actual
  hosting provider's offerings.
- The privacy page is a plain-language draft, not legal advice — see the production
  checklist.
