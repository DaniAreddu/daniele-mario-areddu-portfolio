#!/usr/bin/env node
/** Generates dist/sitemap.xml from the same static route list used by the
 * prerender script, with EN/IT alternates. Run after `npm run build`. */
import { writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = dirname(fileURLToPath(import.meta.url));
const DIST = join(__dirname, "..", "dist");

const SITE_URL = process.env.VITE_SITE_URL || "https://example.invalid";
if (!process.env.VITE_SITE_URL) {
  console.warn(
    "VITE_SITE_URL is not set — sitemap.xml will use a placeholder domain. " +
      "Set VITE_SITE_URL before a production build.",
  );
}

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

function urlEntry(route) {
  const en = `${SITE_URL}${route === "/" ? "" : route}`;
  const it = `${SITE_URL}${route === "/" ? "/it" : `/it${route}`}`;
  return `  <url>
    <loc>${en}</loc>
    <xhtml:link rel="alternate" hreflang="en" href="${en}" />
    <xhtml:link rel="alternate" hreflang="it" href="${it}" />
  </url>
  <url>
    <loc>${it}</loc>
    <xhtml:link rel="alternate" hreflang="en" href="${en}" />
    <xhtml:link rel="alternate" hreflang="it" href="${it}" />
  </url>`;
}

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
${ROUTES.map(urlEntry).join("\n")}
</urlset>
`;

writeFileSync(join(DIST, "sitemap.xml"), xml, "utf-8");
console.log(`Wrote sitemap.xml with ${ROUTES.length * 2} URLs.`);

// robots.txt must reference the sitemap by absolute URL; public/robots.txt
// (copied verbatim into dist by Vite) only has a relative placeholder, so it
// is rewritten here once the real site URL is known.
writeFileSync(
  join(DIST, "robots.txt"),
  `User-agent: *\nAllow: /\nDisallow: /admin\n\nSitemap: ${SITE_URL}/sitemap.xml\n`,
  "utf-8",
);
