# Daniele Mario Areddu — Portfolio

A production-oriented personal portfolio for **Daniele Mario Areddu** — Backend & AI
Developer at Global Technologies Italia, international conference speaker, Computer
Science student at the University of Calabria, and founder of
[Velletri.dev](https://velletri.dev). Built as a bilingual (EN/IT), editorial-tech
monorepo: a React/TypeScript frontend backed by a real FastAPI/PostgreSQL API — no
portfolio content is hardcoded into components.

## 1. Project overview & product goals

Within 30 seconds a visitor should understand who Daniele is, what he builds, which
technologies he works with, his education and professional journey, where he has
spoken, which projects he has worked on, what drives him personally, and how to invite
him to speak or collaborate. The design language is warm charcoal + ivory with a single
cobalt-blue accent, editorial serif headings, and restrained cartographic motifs — see
[docs/asset-requirements.md](docs/asset-requirements.md) for the full visual system.

## 2. Feature list

- Bilingual site (English default, Italian under `/it`) with a typed i18n layer
- Hero, About, Journey (editorial timeline), Experience, Projects + case studies,
  Speaking (interactive MapLibre map with multi-event location grouping, a
  year-by-year international expansion timeline, dynamically computed stats,
  curated "Next stops" and "International milestones" showcases, filters, and an
  accessible list fallback), Community (Velletri.dev), Passions, Contact, Privacy,
  custom 404
- Real FastAPI backend serving every piece of portfolio content, with localized
  responses, filtering/search on events, and a GeoJSON endpoint for the map
- Contact form (React Hook Form + Zod) with honeypot + rate limiting, delivering to
  Mailpit in development and configurable SMTP in production
- SEO: per-route metadata, canonical/hreflang links, JSON-LD, sitemap, and a concrete
  prerendering step (see [docs/seo-strategy.md](docs/seo-strategy.md))
- Automated tests at every layer: backend pytest, frontend Vitest + Testing Library +
  axe, and Playwright end-to-end tests
- Dockerized development and production stacks behind a single Nginx gateway

## 3. Technology stack

**Frontend** — React 18, TypeScript, Vite, React Router, Tailwind CSS, Motion
(Framer Motion), TanStack Query, React Hook Form, Zod, Lucide, MapLibre GL JS,
i18next, Vitest, React Testing Library, Playwright, ESLint, Prettier.

**Backend** — Python 3.12, FastAPI, Pydantic v2, Pydantic Settings, SQLAlchemy 2
(async), asyncpg, Alembic, PostgreSQL, Ruff, mypy, pytest, pytest-asyncio, HTTPX,
`uv` for dependency management.

**Infrastructure** — Docker, Docker Compose, multi-stage non-root Dockerfiles, Nginx
(single public gateway), Mailpit (dev email), GitHub Actions.

## 4. Architecture summary

```
Browser → Nginx gateway (:8080) → / → frontend (static SPA, internal)
                                 → /api → backend (FastAPI, internal)
Backend → PostgreSQL
Backend → SMTP (Mailpit in dev, real provider in prod)
```

The gateway is the **only** publicly exposed service. See
[docs/architecture.md](docs/architecture.md) for a full diagram and
[docs/data-model.md](docs/data-model.md) for the database schema.

## 5. Prerequisites

- Docker Desktop (or Docker Engine + Compose plugin) — for the full stack
- Node.js 20+ and npm — for frontend-only local development
- Python 3.12 and [uv](https://docs.astral.sh/uv/) — for backend-only local development
- `make` (optional) — Windows users without `make` can run the underlying
  `docker compose` commands directly; each Makefile target's command is shown below

## 6. Quick start (Docker)

```bash
cp .env.example .env
docker compose up --build
```

This starts PostgreSQL, the FastAPI backend (with live reload), the Vite dev server,
Mailpit, and the Nginx gateway. Once healthy:

- App: http://localhost:8080
- API docs (Swagger UI): http://localhost:8000/docs (or via the gateway at
  `http://localhost:8080/api/v1/...` for the endpoints themselves)
- Mailpit web UI: http://localhost:8025

Then, in a second terminal, apply migrations and seed content:

```bash
make migrate && make seed
# Windows without make:
docker compose exec backend uv run alembic upgrade head
docker compose exec backend uv run python -m app.seed.seed
```

## 7. Local frontend development (without Docker)

```bash
cd frontend
npm install
cp .env.example .env   # adjust VITE_API_PROXY_TARGET if the backend isn't on :8000
npm run dev
```

## 8. Local backend development (without Docker)

```bash
cd backend
uv sync
cp .env.example .env   # point DATABASE_URL at a local Postgres, or see the SQLite note below
uv run alembic upgrade head
uv run python -m app.seed.seed
uv run uvicorn app.main:app --reload
```

For a quick spin without installing PostgreSQL, override `DATABASE_URL` with a SQLite
URL, e.g. `sqlite+aiosqlite:///./dev.db` — this is exactly what the automated test
suite does (see `backend/tests/conftest.py`). Production and the Docker Compose setup
use PostgreSQL.

## 9. Database migrations

```bash
make migrate
# or: docker compose exec backend uv run alembic upgrade head
```

To create a new migration after changing a model:

```bash
docker compose exec backend uv run alembic revision --autogenerate -m "describe the change"
```

Always review autogenerated migrations before applying them.

## 10. Database seed

```bash
make seed
# or: docker compose exec backend uv run python -m app.seed.seed
```

The seed is **idempotent** — safe to re-run. Rows are matched by their natural key
(slug, or a singleton lookup for profile/biography/community profile) and updated in
place rather than duplicated. See [docs/event-management.md](docs/event-management.md)
for how to add a new speaking event.

## 11. Tests

```bash
make test
# Backend only:  docker compose exec backend uv run pytest
# Frontend only: docker compose exec frontend npm run test
```

End-to-end tests (require the dev stack running, or start their own dev server):

```bash
cd frontend
npx playwright install --with-deps chromium   # first time only
npm run e2e
```

## 12. Linting & type checking

```bash
make lint
make typecheck
```

## 13. Production builds

```bash
docker compose -f docker-compose.prod.yml build
```

Or locally per service:

```bash
cd backend && uv sync --frozen
cd frontend && npm run build         # bundle only
cd frontend && npm run build:full    # bundle + sitemap.xml + prerendered routes
```

## 14. Environment variables

See [`.env.example`](.env.example) (Compose-level), [`backend/.env.example`](backend/.env.example),
and [`frontend/.env.example`](frontend/.env.example) for the full, documented list.
Key ones:

| Variable                        | Where    | Purpose                                                                  |
| ------------------------------- | -------- | ------------------------------------------------------------------------ |
| `DATABASE_URL`                  | backend  | Async SQLAlchemy connection string                                       |
| `CORS_ORIGINS`                  | backend  | Allowed frontend origins                                                 |
| `CONTACT_RECIPIENT_EMAIL`       | backend  | Where contact form notifications are sent                                |
| `SMTP_HOST` / `SMTP_PORT` / ... | backend  | Mailpit in dev, real SMTP in prod                                        |
| `CONTACT_RATE_LIMIT_PER_HOUR`   | backend  | App-level abuse protection                                               |
| `VITE_API_BASE_URL`             | frontend | API base path the browser calls                                          |
| `VITE_MAP_STYLE_URL`            | frontend | MapLibre style URL (no API key required by default)                      |
| `VITE_SITE_URL`                 | frontend | Canonical domain for SEO tags — **must be set before production launch** |

No secrets are committed. `.env` is gitignored everywhere; only `.env.example` files
are tracked.

## 15. Mailpit (development email)

All contact-form emails in development are sent to Mailpit, a local SMTP test server —
never to a real inbox. View them at http://localhost:8025. See
[docs/contact-flow.md](docs/contact-flow.md) for the full flow, including what happens
if delivery fails (the API is honest about it — it never claims a false success).

## 16. SMTP configuration (production)

Set `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD`, `SMTP_USE_TLS`, and
`SMTP_SENDER` to a real transactional email provider's credentials. Do not point
production at Mailpit.

## 17. Nginx behavior

A single Nginx **gateway** container is the only publicly exposed service. It
reverse-proxies `/` to the frontend and `/api/` to the backend, applies security
headers and a CSP, rate-limits the contact endpoint beyond the app-level limit, and
gzips responses. The frontend's own internal Nginx (production image only) serves the
static build with immutable caching for hashed assets, no caching for HTML, and a
SPA history-fallback so direct navigation and refreshes on any route work correctly.
See [nginx/gateway.conf](nginx/gateway.conf) and
[frontend/nginx/frontend.conf](frontend/nginx/frontend.conf).

## 18. Project structure

```
backend/
  app/
    api/          FastAPI routers (v1) + dependency wiring
    core/         settings, logging, error envelopes, i18n locale resolution
    db/           SQLAlchemy base + async session
    models/       SQLAlchemy ORM models
    schemas/      Pydantic request/response schemas
    repositories/ data access (one per resource)
    services/     business logic + locale selection
    seed/         structured seed content + idempotent seed script
  alembic/        migrations
  tests/          pytest suite
frontend/
  src/
    app/          router, App shell, locale context
    pages/        one component per route
    features/     speaking (map/timeline/filters) and contact (form)
    components/   shared UI primitives (nav, footer, async states, ...)
    hooks/        TanStack Query hooks, SEO hook, reduced-motion hook
    services/     typed API client
    i18n/         UI-string dictionaries (EN/IT) — page content itself comes from the API
    types/        API response types
  e2e/            Playwright specs
  scripts/        sitemap + prerender build scripts
nginx/            public gateway image
docs/             architecture, data model, SEO, security, and operational guides
```

## 19. Deployment guidance

This repo ships a Docker Compose production configuration
(`docker-compose.prod.yml`), suitable for a single VM or any Docker-capable host. It
does not include a specific cloud provider's deployment automation — CI builds and
validates the images but does not deploy them anywhere (see
`.github/workflows/`). Before deploying:

1. Set `VITE_SITE_URL` to the real production domain.
2. Point `SMTP_*` at a real provider.
3. Put TLS termination in front of the gateway (e.g. a managed load balancer, or add
   a TLS-terminating reverse proxy / certbot sidecar — not included here since no
   domain was provided).
4. Review [docs/production-checklist.md](docs/production-checklist.md).

## 20. PostgreSQL backup

```bash
make db-backup
# or: docker compose exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup.sql
```

## 21. PostgreSQL restore

```bash
make db-restore
# or: cat backup.sql | docker compose exec -T db psql -U $POSTGRES_USER $POSTGRES_DB
```

## 22. Adding an event

Edit `backend/app/seed/data.py` (`EVENTS` list) — never invent dates, locations,
session titles, or URLs; leave genuinely unknown fields as `None`. Re-run
`make seed`. Full walkthrough: [docs/event-management.md](docs/event-management.md).

## 23. Updating biography content

Edit the `PROFILE` / `BIOGRAPHY` dictionaries in `backend/app/seed/data.py` (both
`_en` and `_it` fields), then `make seed`. Content is never hardcoded in React
components.

## 24. Adding a project

Add an entry to the `PROJECTS` list in `backend/app/seed/data.py` following the
existing shape (problem/challenge/approach/architecture/outcome/lessons in both
languages), then `make seed`.

## 25. Adding photographs

No headshot, speaker photo, or logo exists in this repository yet. Elegant
typographic/cartographic placeholders (`Monogram`, `RouteMotif`) are used instead —
see [docs/asset-requirements.md](docs/asset-requirements.md) for exact filenames,
dimensions, and where each future asset would be wired in.

## 26. Configuring social links

`Profile.github_url` / `linkedin_url` / `sessionize_url` in the seed data are `null`
by default and the corresponding UI elements stay hidden until a verified URL is set —
no username or URL is ever guessed.

## 27. Troubleshooting

- **`docker compose up` fails to reach the database** — wait for the `db` healthcheck;
  `depends_on: condition: service_healthy` should handle this, but first-run image
  pulls can be slow.
- **Contact form always shows "email could not be delivered"** — check Mailpit is
  running and `SMTP_HOST=mailpit` (the service name, not `localhost`, from inside
  Docker).
- **Map doesn't load** — check `VITE_MAP_STYLE_URL` is reachable; the UI falls back to
  an accessible list automatically if it isn't.
- **Windows + Docker Desktop**: ensure the WSL2 backend is running before
  `docker compose up`; `docker compose exec` commands work identically in PowerShell,
  `cmd`, and WSL.

## 28. Known content gaps

Tracked transparently rather than invented:

- No headshot, speaker photo, Velletri.dev logo, CV, speaker kit, slides, or
  recordings exist yet — see [docs/asset-requirements.md](docs/asset-requirements.md).
- GitHub/LinkedIn/Sessionize links are unset (`null`) until Daniele provides verified
  URLs.
- Several 2025–2026 events have a known year but not an exact date or, in a few cases,
  an exact city — these fields are `null` by design (see
  [docs/event-management.md](docs/event-management.md) for the full list).
- The production domain (`VITE_SITE_URL`) is not set — no domain is invented.
- `docs/privacy` page content is a good-faith plain-language draft, not legal advice;
  it should be reviewed against applicable regulations before launch.
