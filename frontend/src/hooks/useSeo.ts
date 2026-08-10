import { useEffect } from "react";

import { localizedPathFor, useLocale } from "@/app/LocaleContext";

const SITE_URL = import.meta.env.VITE_SITE_URL ?? "";

function upsertMeta(attr: "name" | "property", key: string, content: string) {
  let tag = document.head.querySelector<HTMLMetaElement>(`meta[${attr}="${key}"]`);
  if (!tag) {
    tag = document.createElement("meta");
    tag.setAttribute(attr, key);
    document.head.appendChild(tag);
  }
  tag.setAttribute("content", content);
}

function upsertLink(rel: string, href: string, hreflang?: string) {
  const selector = hreflang
    ? `link[rel="${rel}"][hreflang="${hreflang}"]`
    : `link[rel="${rel}"]:not([hreflang])`;
  let tag = document.head.querySelector<HTMLLinkElement>(selector);
  if (!tag) {
    tag = document.createElement("link");
    tag.setAttribute("rel", rel);
    if (hreflang) tag.setAttribute("hreflang", hreflang);
    document.head.appendChild(tag);
  }
  tag.setAttribute("href", href);
}

function upsertJsonLd(id: string, data: unknown) {
  let tag = document.head.querySelector<HTMLScriptElement>(`script[data-jsonld="${id}"]`);
  if (!tag) {
    tag = document.createElement("script");
    tag.type = "application/ld+json";
    tag.dataset.jsonld = id;
    document.head.appendChild(tag);
  }
  tag.textContent = JSON.stringify(data);
}

export interface SeoOptions {
  title: string;
  description: string;
  /** Unprefixed, canonical path e.g. "/about" (never "/it/about"). */
  path: string;
  jsonLd?: unknown;
  /** Absolute or site-relative image URL for og:image/twitter:image. Falls
   * back to nothing (no tag) when omitted — callers are not required to
   * provide one. */
  image?: string | null;
  /** Set to false while critical above-the-fold data is still loading, so the
   * prerender script can wait for real content before snapshotting the page. */
  ready?: boolean;
  /** Set for pages that should never be indexed, such as the 404 page. */
  noIndex?: boolean;
}

export function useSeo({
  title,
  description,
  path,
  jsonLd,
  image,
  ready = true,
  noIndex = false,
}: SeoOptions): void {
  const { locale } = useLocale();

  useEffect(() => {
    document.title = title;
    upsertMeta("name", "description", description);
    upsertMeta("property", "og:title", title);
    upsertMeta("property", "og:description", description);
    upsertMeta("property", "og:type", "website");
    upsertMeta("name", "twitter:card", "summary_large_image");
    upsertMeta("name", "twitter:title", title);
    upsertMeta("name", "twitter:description", description);
    if (image) {
      upsertMeta("property", "og:image", image);
      upsertMeta("name", "twitter:image", image);
    }
    upsertMeta("name", "robots", noIndex ? "noindex, nofollow" : "index, follow");

    const canonicalPath = localizedPathFor(path, locale);
    upsertLink("canonical", `${SITE_URL}${canonicalPath}`);
    upsertLink("alternate", `${SITE_URL}${localizedPathFor(path, "en")}`, "en");
    upsertLink("alternate", `${SITE_URL}${localizedPathFor(path, "it")}`, "it");

    if (jsonLd) upsertJsonLd(path, jsonLd);
  }, [title, description, path, locale, jsonLd, image, noIndex]);

  useEffect(() => {
    if (ready) {
      document.body.dataset.prerenderReady = "true";
    }
  }, [ready]);
}
