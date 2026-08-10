"""Small helper to pick the right localized attribute off a model instance."""

from __future__ import annotations

from typing import Any


def pick(obj: Any, field: str, locale: str) -> Any:
    """Return obj.<field>_<locale>, falling back to the English variant."""
    value = getattr(obj, f"{field}_{locale}", None)
    if value is None or value == "":
        value = getattr(obj, f"{field}_en")
    return value
