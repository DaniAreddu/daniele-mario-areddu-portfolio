# Production checklist

Items marked **⚠ Daniele must review/decide** are intentionally left open — nothing
here invents a domain, credential, or legal claim on his behalf.

## Configuration

- [ ] ⚠ Set `VITE_SITE_URL` to the real production domain (used for canonical URLs,
      hreflang, sitemap, and JSON-LD).
- [ ] ⚠ Point `SMTP_HOST` / `SMTP_PORT` / `SMTP_USER` / `SMTP_PASSWORD` /
      `SMTP_USE_TLS` / `SMTP_SENDER` at a real transactional email provider — never
      Mailpit.
- [ ] Set strong, unique `POSTGRES_PASSWORD` (do not reuse the development default).
- [ ] Set `CORS_ORIGINS` to the exact production origin(s) only.
- [ ] Set `DOCS_ENABLED=false` if the interactive OpenAPI docs (`/docs`, `/redoc`)
      should not be publicly reachable in production (they are proxied through the
      backend only if `DOCS_ENABLED=true`).
- [ ] ⚠ Decide on and configure TLS termination in front of the Nginx gateway (a
      managed load balancer, or a certbot/TLS-terminating proxy in front of it) — not
      included in this repo since no domain/certificate authority was specified.

## Content

- [ ] ⚠ Review [asset-requirements.md](asset-requirements.md) and supply real
      photographs, the Velletri.dev logo, CV, and speaker kit if desired.
- [ ] ⚠ Review and confirm every event in `backend/app/seed/data.py` — several have
      intentionally incomplete dates/locations (see
      [event-management.md](event-management.md)); fill in real confirmed details as
      they become available.
- [ ] ⚠ Add verified `github_url` / `linkedin_url` / `sessionize_url` to the seed
      `PROFILE` data if Daniele wants those links shown — they render only when set.
- [ ] ⚠ Review [privacy page copy](../frontend/src/pages/PrivacyPage.tsx) against
      applicable regulations (e.g. GDPR) — it is a good-faith plain-language draft,
      not legal advice.

## Database

- [ ] Run `alembic upgrade head` against the production database before first
      deploy.
- [ ] Run the seed once (`python -m app.seed.seed`) — safe to re-run on every deploy,
      since it's idempotent.
- [ ] Confirm automated backups are scheduled (see the backup/restore commands in the
      README) — this repo documents the commands but does not schedule a cron job for
      you, since that depends on the hosting environment.

## Security (see also [security.md](security.md))

- [ ] Confirm `read_only: true` + `tmpfs` mounts in `docker-compose.prod.yml` still
      hold after any Dockerfile changes.
- [ ] Confirm no `.env` file is committed (`git status` should never show one).
- [ ] Run `docker scout` or `trivy` against the built images before deploying, in
      addition to the CI-level `pip-audit` / `npm audit` checks.
- [ ] Confirm the gateway is the only container with a published port.

## Performance

- [ ] Run `npm run build:full` (build + sitemap + prerender) rather than a plain
      `npm run build` for the production frontend image, so crawlers get real content
      (see [seo-strategy.md](seo-strategy.md)).
- [ ] Spot-check Lighthouse scores against the deployed URL once live.

## Post-deploy smoke test

- [ ] `GET /health` and `GET /ready` both return 200.
- [ ] `GET /api/v1/events/geojson` returns a non-empty `FeatureCollection`.
- [ ] Submitting the contact form in production actually delivers an email (test with
      a real address you control, then confirm receipt).
- [ ] Direct navigation to `/it/speaking` and a refresh both work (Nginx history
      fallback).
