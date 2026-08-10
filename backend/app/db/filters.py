"""Shared query predicates for content using the publication/soft-delete
mixins in app.db.base.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TypeVar

from sqlalchemy import ColumnElement, and_, or_

from app.db.base import PublishableMixin, SoftDeleteMixin

ModelT = TypeVar("ModelT", bound=PublishableMixin)


def visible_now(model: type[ModelT]) -> ColumnElement[bool]:
    """True for rows that should appear in a public endpoint right now:
    published, not soft-deleted, and within any configured publish/unpublish
    window. Apply this to every public repository query for a model mixing
    in ``PublishableMixin`` — never filter publication status in Python,
    since that would require loading hidden rows into memory at all.
    """
    now = datetime.now(UTC)
    conditions = [
        model.publication_status == "PUBLISHED",
        or_(model.publish_at.is_(None), model.publish_at <= now),
        or_(model.unpublish_at.is_(None), model.unpublish_at > now),
    ]
    if issubclass(model, SoftDeleteMixin):
        conditions.append(model.deleted_at.is_(None))
    return and_(*conditions)
