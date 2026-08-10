# Asset requirements

No headshot, speaker photograph, logo, CV, speaker kit, slides, or recordings exist in
this repository. Nothing here uses stock photography or a generated face — elegant
typographic/cartographic placeholders stand in until real assets are supplied.

## Current placeholders and where they live

| Placeholder | Component | Purpose |
|---|---|---|
| Monogram ("DA" on charcoal) | `frontend/src/components/Monogram.tsx` | Stands in for the hero portrait |
| Route/coordinate motif (SVG) | `frontend/src/components/RouteMotif.tsx` | Decorative cartographic detail near the hero |
| Text-only favicon | `frontend/public/favicon.svg` | Browser tab icon |

## Recommended assets, once available

All paths are suggestions under `frontend/src/assets/` (co-located with the components
that would use them) or `frontend/public/` (for files referenced by absolute URL,
like OG images and the favicon).

| Asset | Suggested filename | Dimensions | Format | Used in |
|---|---|---|---|---|
| Main headshot | `assets/portrait-main.jpg` | 1200×1500 (4:5) | JPEG/WebP, <300KB | Replaces `Monogram` in the hero |
| Stage/speaking photograph | `assets/portrait-stage.jpg` | 1600×1067 (3:2) | JPEG/WebP | Speaking page hero or About page |
| Speaker portrait (square) | `assets/portrait-square.jpg` | 800×800 (1:1) | JPEG/WebP | Social preview / speaker-kit card |
| Velletri.dev logo | `assets/velletri-dev-logo.svg` | vector, ~200×200 viewBox | SVG (preferred) or PNG @2x | Community page |
| CV | `public/cv-daniele-areddu.pdf` | — | PDF | About page "Download CV" (currently hidden — see below) |
| Speaker kit | `public/speaker-kit.pdf` or `.zip` | — | PDF/ZIP | About page's "Speaker kit" section (currently shows an "in preparation" note) |
| Talk slides (per event) | `assets/slides/<event-slug>.pdf` | — | PDF | Linked from `Event.slides_url` once uploaded somewhere and the URL is added to seed data |
| Social preview / OG image | `public/og-image.png` | 1200×630 | PNG/JPEG | `useSeo`'s `og:image` meta tag (not yet set — see below) |

## Compression guidance

- Photographs: export at 80–85% JPEG quality or WebP equivalent; target under 300KB
  for hero-sized images, under 150KB for smaller ones.
- Logos/icons: prefer SVG; optimize with SVGO before committing.
- Never commit uncompressed originals to the repository — keep those outside version
  control and commit only the optimized, web-ready export.

## How to wire a real photograph in without restructuring

`Monogram` and the hero section (`frontend/src/pages/HomePage.tsx`) were deliberately
built with the same aspect ratio and rounded-corner treatment a real portrait would
use. To replace it:

1. Add the optimized image to `frontend/src/assets/`.
2. Replace `<Monogram />` in `HomePage.tsx` with an `<img>` (with descriptive `alt`
   text) or a small `Portrait` component wrapping it — same container classes.
3. No layout or routing changes are needed elsewhere.

## Social preview image

`useSeo` does not currently set `og:image` / `twitter:image` because no portrait or
designed social-card image exists yet, and a code-generated preview using only
typography (matching the Monogram treatment) was out of scope for this pass. Once
`public/og-image.png` exists, add `upsertMeta("property", "og:image", ...)` /
`twitter:image` calls to `frontend/src/hooks/useSeo.ts`.

## Speaker kit & CV

The About page's "Speaker kit" section renders a plain notice
(`about.speakerKitUnavailable`) instead of a broken download link, per the brief's
instruction to hide download actions that cannot work rather than fake them. Once a
real PDF/ZIP exists at a stable URL, replace that notice with a real `<a href>` download
link.
