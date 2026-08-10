#!/usr/bin/env node
/**
 * Concrete prerendering step for a subset of important public routes.
 *
 * React + Vite ship no server-side rendering here (Next.js is explicitly out
 * of scope), so crawlers hitting a bare client-rendered SPA would see an
 * empty shell. This script serves the real production build with
 * `vite preview`, opens each route in headless Chromium (via Playwright,
 * already a project dependency for e2e tests), waits for the page's data to
 * actually load, and writes the resulting HTML into `dist/<route>/index.html`
 * (or `dist/index.html` for the root). Nginx's static file server (see
 * nginx/frontend.conf) then serves that pre-rendered HTML to first requests,
 * while the same JS bundle still hydrates and takes over normal client-side
 * navigation for real visitors.
 *
 * Scope: the routes listed in ROUTES below, in both languages. Per-project
 * slugs are not prerendered in this pass; see the note at the bottom of this
 * file for how to extend it.
 *
 * Requires: the backend API reachable at VITE_API_PROXY_TARGET (default
 * http://localhost:8000), because pages fetch their content client-side on
 * first load, and this script waits for that fetch to resolve before
 * snapshotting the page.
 */
import { chromium } from "@playwright/test";
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, "..");
const DIST = join(ROOT, "dist");
const PREVIEW_PORT = 4173;
const BASE_URL = `http://localhost:${PREVIEW_PORT}`;

const ROUTES = [
  "/",
  "/about",
  "/journey",
  "/experience",
  "/projects",
  "/speaking",
  "/community",
  "/passions",
  "/contact",
  "/privacy",
];

const ALL_ROUTES = [
  ...ROUTES,
  ...ROUTES.map((route) => (route === "/" ? "/it" : `/it${route}`)),
];

function outputPathFor(route) {
  if (route === "/") return join(DIST, "index.html");
  return join(DIST, route.replace(/^\//, ""), "index.html");
}

async function waitForServer(url, attempts = 30) {
  for (let i = 0; i < attempts; i += 1) {
    try {
      const response = await fetch(url);
      if (response.ok) return;
    } catch {
      // Not up yet.
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  throw new Error(`Preview server at ${url} never became ready.`);
}

async function main() {
  if (!existsSync(DIST)) {
    console.error("dist/ not found — run `npm run build` before prerendering.");
    process.exitCode = 1;
    return;
  }

  const preview = spawn(
    "npx",
    ["vite", "preview", "--port", String(PREVIEW_PORT), "--strictPort"],
    { cwd: ROOT, stdio: "inherit", shell: true },
  );

  try {
    await waitForServer(BASE_URL);

    const browser = await chromium.launch();
    const page = await browser.newPage();

    for (const route of ALL_ROUTES) {
      const url = `${BASE_URL}${route}`;
      console.log(`Prerendering ${route}...`);
      await page.goto(url, { waitUntil: "networkidle" });
      try {
        await page.waitForSelector('body[data-prerender-ready="true"]', { timeout: 8000 });
      } catch {
        console.warn(`  ⚠ ${route} did not signal readiness in time; snapshotting anyway.`);
      }
      const html = await page.content();
      const outputPath = outputPathFor(route);
      mkdirSync(dirname(outputPath), { recursive: true });
      writeFileSync(outputPath, html, "utf-8");
    }

    await browser.close();
    console.log(`Prerendered ${ALL_ROUTES.length} routes into dist/.`);
  } finally {
    preview.kill();
  }
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

// To extend this to per-project case studies, fetch the project slug list
// from `${VITE_API_PROXY_TARGET}/api/v1/projects` before building ALL_ROUTES
// and add "/projects/<slug>" (and its "/it" counterpart) for each one.
