"""Generic publish/schedule/unpublish/archive/trash/restore/permanent-delete
+ revision-listing machinery, shared by every content type built on
PublishableMixin + SoftDeleteMixin.

Extracted only now, after the identical hand-written logic proved itself
twice (Event, Project) — see docs/admin-guide.md's "extending to a new
content type" note. Event/ProjectAdminService are deliberately left as they
are (already correct and tested); this mixin is for the content types built
after the pattern was proven, so the DRY-up never risks the two verticals
that were manually verified end-to-end in a browser.

A concrete service still owns `create`/`update`/`restore_revision` (field
shapes and tag handling differ too much per entity to generalize usefully)
but delegates every lifecycle transition to this mixin.
"""

from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime
from typing import Any, Generic, TypeVar

from app.core.errors import AppError, NotFoundError
from app.models.admin_user import AdminUser
from app.models.revision import Revision
from app.services._admin_common import record_audit_event

# Deliberately untyped (Any) for the entity itself — a Protocol bound here
# added ceremony without benefit, since every concrete service already
# knows its own concrete entity type in its own method signatures (e.g.
# `apply: Callable[[Education], None]` inside EducationAdminService). OutT
# is the generic parameter that actually matters: it keeps each service's
# public methods (`publish`, `archive`, ...) returning its own precise
# `<Entity>AdminOut` type rather than a shared base.
OutT = TypeVar("OutT")


class LifecycleAdminMixin(Generic[OutT]):
    """Mixed into a concrete admin service that defines ``self.repository``
    (with async ``get_by_id``/``delete``, plus a ``session`` attribute),
    ``self.revision_repository``, an ``entity_type`` class attribute, and a
    ``_to_out(entity) -> OutT`` mapper.
    """

    entity_type: str
    repository: Any
    revision_repository: Any

    def _to_out(self, entity: Any) -> OutT:  # pragma: no cover - overridden
        raise NotImplementedError

    def _refresh_attrs(self) -> list[str]:
        """Relationship/derived attribute names to refresh after a commit,
        beyond the always-required ``updated_at`` (expired by the DB-side
        ``onupdate`` regardless of ``expire_on_commit``). Override to add
        e.g. ``["tags"]``.
        """
        return []

    async def _get_or_404(self, entity_id: int) -> Any:
        entity = await self.repository.get_by_id(entity_id)
        if entity is None:
            raise NotFoundError(f"{self.entity_type.capitalize()} not found.")
        return entity

    async def _commit_and_refresh(self, entity: Any) -> None:
        await self.repository.session.commit()
        await self.repository.session.refresh(
            entity, attribute_names=[*self._refresh_attrs(), "updated_at"]
        )

    async def _transition(
        self,
        entity_id: int,
        actor: AdminUser,
        action: str,
        summary: str,
        apply: Callable[[Any], None],
    ) -> OutT:
        entity = await self._get_or_404(entity_id)
        apply(entity)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action=f"{self.entity_type}.{action}",
            entity_type=self.entity_type,
            entity_id=entity.id,
            summary=summary,
        )
        await self._commit_and_refresh(entity)
        return self._to_out(entity)

    async def publish(self, entity_id: int, actor: AdminUser) -> OutT:
        def apply(entity: Any) -> None:
            entity.publication_status = "PUBLISHED"
            entity.publish_at = None
            entity.unpublish_at = None
            if entity.published_at is None:
                entity.published_at = datetime.now(UTC)

        return await self._transition(entity_id, actor, "publish", "Published", apply)

    async def schedule(self, entity_id: int, publish_at: datetime, actor: AdminUser) -> OutT:
        def apply(entity: Any) -> None:
            entity.publication_status = "SCHEDULED"
            entity.publish_at = publish_at

        return await self._transition(
            entity_id, actor, "schedule", f"Scheduled for {publish_at.isoformat()}", apply
        )

    async def unpublish(self, entity_id: int, actor: AdminUser) -> OutT:
        def apply(entity: Any) -> None:
            entity.publication_status = "DRAFT"
            entity.publish_at = None
            entity.unpublish_at = None

        return await self._transition(entity_id, actor, "unpublish", "Unpublished", apply)

    async def archive(self, entity_id: int, actor: AdminUser) -> OutT:
        def apply(entity: Any) -> None:
            entity.publication_status = "ARCHIVED"

        return await self._transition(entity_id, actor, "archive", "Archived", apply)

    async def soft_delete(self, entity_id: int, actor: AdminUser) -> OutT:
        def apply(entity: Any) -> None:
            entity.deleted_at = datetime.now(UTC)

        return await self._transition(entity_id, actor, "trash", "Moved to trash", apply)

    async def restore_from_trash(self, entity_id: int, actor: AdminUser) -> OutT:
        def apply(entity: Any) -> None:
            entity.deleted_at = None

        return await self._transition(
            entity_id, actor, "restore_from_trash", "Restored from trash", apply
        )

    async def permanent_delete(self, entity_id: int, actor: AdminUser) -> None:
        entity = await self._get_or_404(entity_id)
        if entity.deleted_at is None:
            raise AppError(
                f"Move the {self.entity_type} to trash before deleting it permanently.",
                code="not_trashed",
            )
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action=f"{self.entity_type}.delete_permanently",
            entity_type=self.entity_type,
            entity_id=entity.id,
            summary=f"Permanently deleted {self.entity_type} #{entity.id}",
        )
        await self.repository.delete(entity)
        await self.repository.session.commit()

    async def list_revisions(self, entity_id: int) -> list[Revision]:
        await self._get_or_404(entity_id)
        result: list[Revision] = await self.revision_repository.list_for_entity(
            self.entity_type, entity_id
        )
        return result

    async def _get_revision_or_404(self, entity_id: int, revision_id: int) -> Revision:
        revision: Revision | None = await self.revision_repository.get(revision_id)
        if (
            revision is None
            or revision.entity_type != self.entity_type
            or revision.entity_id != entity_id
        ):
            raise NotFoundError("Revision not found.")
        return revision
