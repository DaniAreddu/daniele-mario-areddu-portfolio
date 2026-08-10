# SEO strategy

## The problem

The mandated stack is React + Vite (explicitly not Next.js), which by default ships a
client-rendered SPA: a crawler that doesn't execute JavaScript sees an near-empty
`<div id="root"></div>`. Modern Googlebot does render JavaScript, but not every crawler
does (many social-preview bots, some search engines, link-unfurling bots), and even
Googlebot's rendering is queued and delayed. Shipping "just" a CSR shell and calling
it done would not meet the brief's requirement for a concrete strategy.

## What's actually implemented

1. **Per-route metadata at runtime.** `frontend/src/hooks/useSeo.ts` imperatively sets
   `<title>`, meta description, Open Graph, Twitter Card, canonical URL, and
   `hreflang` alternates (EN ⇄ IT) for every page, using real page data once loaded
   (e.g. a project's actual title and summary, not a generic template).
2. **JSON-LD structured data.** The home page emits `Person` structured data built
   from the real `/api/v1/profile` response (name, job title, contact email) — never
   invented fields. Per-event JSON-LD is intentionally **not** emitted for events
   with unknown dates/locations, since incomplete structured data is worse than none.
3. **Build-time prerendering.** `frontend/scripts/prerender.mjs` serves the production
   build with `vite preview`, opens each of the ten primary public routes (in both
   languages, twenty pages total) in headless Chromium, waits for the page to signal
   `body[data-prerender-ready="true"]` (set by `useSeo` once a page's critical data
   has loaded — see the `ready` option), and writes the resulting real HTML to
   `dist/<route>/index.html` (or `dist/index.html` for the root). Nginx's static file
   server then serves that pre-rendered HTML on first request; the same JS bundle
   still hydrates afterward, so normal client-side navigation is unaffected for real
   visitors. Run it with `npm run build:full` (build → sitemap → prerender).
   - **Scope**: the ten top-level routes × 2 languages. Project detail pages
     (`/projects/:slug`) are not prerendered in this pass — the script has a comment
     showing exactly how to extend it by fetching the slug list from the API first.
   - **Requirement**: the backend must be reachable during the build (the pages fetch
     their content client-side, same as in production), which is why this is a
     separate, explicit build step rather than bundled into `vite build` — it needs
     a running dependency, unlike a pure bundler step.
4. **Sitemap & robots.txt.** `frontend/scripts/generate-sitemap.mjs` writes
   `dist/sitemap.xml` with `hreflang` alternates for every route/language pair, and
   rewrites `dist/robots.txt` with the sitemap's absolute URL once `VITE_SITE_URL` is
   known (the static `public/robots.txt` only has a placeholder, since the real
   domain isn't known at `public/` copy time).
5. **History fallback.** `frontend/nginx/frontend.conf`'s `try_files $uri $uri/
   /index.html` means direct navigation and refreshes on any route return a real
   page instead of a 404 from Nginx (React Router then renders the right page, or
   the custom 404 page for a truly unknown path).
6. **Semantic HTML & heading hierarchy.** Every page has exactly one `<h1>`; sections
   use `<h2>`; the map's accessible list alternative and filters use proper
   `<fieldset>`/`<label>` semantics (see [../docs/security.md](security.md)'s sibling,
   the accessibility notes in the README).

## What's out of scope here

Full server-side rendering (which would require Next.js or a custom Node SSR server)
was explicitly excluded by the mandated stack. Prerendering a fixed, known set of
routes is the standard, well-established alternative for a React SPA that doesn't use
a meta-framework (the same technique used by tools like `react-snap` or
`vite-plugin-ssg`), and is what's implemented here as an actual, runnable script rather
than a README aspiration.

## Configuring the production domain

Set `VITE_SITE_URL` (frontend build arg / env var) to the real domain before running
`npm run build:full` in production. It is intentionally left empty in
`.env.example` — no domain is invented.
