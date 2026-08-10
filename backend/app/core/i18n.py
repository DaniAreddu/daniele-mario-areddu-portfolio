"""Locale resolution for the `lang` query parameter / Accept-Language header."""

from __future__ import annotations

from fastapi import Query, Request

from app.core.config import get_settings

Locale = str


def resolve_locale(
    request: Request,
    lang: Locale | None = Query(
        default=None, description="Preferred locale, e.g. 'en' or 'it'."
    ),
) -> Locale:
    settings = get_settings()
    supported = settings.supported_locales

    if lang and lang.lower() in supported:
        return lang.lower()

    accept_language = request.headers.get("accept-language", "")
    for part in accept_language.split(","):
        code = part.split(";")[0].strip().lower()[:2]
        if code in supported:
            return code

    return settings.default_locale
