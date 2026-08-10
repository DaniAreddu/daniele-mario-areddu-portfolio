"""Admin CRUD, publication lifecycle, and revision history for speaking
events — the first content vertical, and the template every later content
type's admin service follows (see docs/admin-guide.md).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from app.core.errors import AppError, NotFoundError
from app.models.admin_user import AdminUser
from app.models.event import Event
from app.models.revision import Revision
from app.models.tag import Tag
from app.repositories.event_repository import EventRepository
from app.repositories.revision_repository import RevisionRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.event import EventOut
from app.schemas.event_admin import (
    DuplicateCandidateOut,
    EventAdminCreate,
    EventAdminOut,
    EventAdminUpdate,
    EventListItemOut,
    RevisionDiffOut,
    RevisionOut,
)
from app.services._admin_common import (
    create_revision,
    merge_revision_snapshot,
    record_audit_event,
    snapshot_entity,
)
from app.services.event_service import to_event_out

_UPDATE_FIELDS = set(EventAdminUpdate.model_fields.keys()) - {"tag_labels"}


def _slugify_tag(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def _to_admin_out(event: Event) -> EventAdminOut:
    return EventAdminOut(
        id=event.id,
        slug=event.slug,
        event_name=event.event_name,
        talk_id=event.talk_id,
        session_title=event.session_title,
        short_description_en=event.short_description_en,
        short_description_it=event.short_description_it,
        full_description_en=event.full_description_en,
        full_description_it=event.full_description_it,
        start_date=event.start_date,
        end_date=event.end_date,
        year=event.year,
        month=event.month,
        city=event.city,
        country=event.country,
        continent=event.continent,
        latitude=event.latitude,
        longitude=event.longitude,
        venue=event.venue,
        format=event.format,
        language=event.language,
        event_url=event.event_url,
        slides_url=event.slides_url,
        recording_url=event.recording_url,
        image=event.image,
        status=event.status,
        sessions_count=event.sessions_count,
        is_featured=event.is_featured,
        is_international_milestone=event.is_international_milestone,
        internal_notes=event.internal_notes,
        tags=sorted(tag.label for tag in event.tags),
        publication_status=event.publication_status,
        publish_at=event.publish_at,
        unpublish_at=event.unpublish_at,
        published_at=event.published_at,
        deleted_at=event.deleted_at,
        created_at=event.created_at,
        updated_at=event.updated_at,
    )


def _to_list_item(event: Event) -> EventListItemOut:
    return EventListItemOut(
        id=event.id,
        slug=event.slug,
        event_name=event.event_name,
        city=event.city,
        country=event.country,
        year=event.year,
        month=event.month,
        status=event.status,
        publication_status=event.publication_status,
        is_featured=event.is_featured,
        is_international_milestone=event.is_international_milestone,
        deleted_at=event.deleted_at,
    )


class EventAdminService:
    def __init__(
        self,
        repository: EventRepository,
        tag_repository: TagRepository,
        revision_repository: RevisionRepository,
    ) -> None:
        self.repository = repository
        self.tag_repository = tag_repository
        self.revision_repository = revision_repository

    async def list_all(self, *, include_trashed: bool = False) -> list[EventListItemOut]:
        events = await self.repository.list_all_admin(include_trashed=include_trashed)
        return [_to_list_item(event) for event in events]

    async def get(self, event_id: int) -> EventAdminOut:
        event = await self._get_or_404(event_id)
        return _to_admin_out(event)

    async def preview(self, event_id: int, locale: str) -> EventOut:
        """Renders through the exact public schema/shape regardless of
        publication status, so admins preview drafts as the public site will
        eventually show them rather than via a second bespoke preview UI.
        """
        event = await self._get_or_404(event_id)
        return to_event_out(event, locale)

    async def _get_or_404(self, event_id: int) -> Event:
        event = await self.repository.get_by_id(event_id)
        if event is None:
            raise NotFoundError("Event not found.")
        return event

    async def check_duplicates(
        self, event_name: str, city: str | None, year: int
    ) -> list[DuplicateCandidateOut]:
        matches = await self.repository.find_similar(event_name, city, year)
        return [
            DuplicateCandidateOut(
                slug=event.slug, event_name=event.event_name, city=event.city, year=event.year
            )
            for event in matches
        ]

    async def _resolve_tags(self, labels: list[str]) -> list[Tag]:
        tags: list[Tag] = []
        seen_slugs: set[str] = set()
        for raw_label in labels:
            label = raw_label.strip()
            if not label:
                continue
            slug = _slugify_tag(label)
            if not slug or slug in seen_slugs:
                continue
            seen_slugs.add(slug)
            tag = await self.tag_repository.get_by_slug(slug)
            if tag is None:
                tag = await self.tag_repository.create(Tag(slug=slug, label=label))
            tags.append(tag)
        return tags

    async def create(self, payload: EventAdminCreate, actor: AdminUser) -> EventAdminOut:
        if await self.repository.get_by_slug_any(payload.slug) is not None:
            raise AppError("An event with this slug already exists.", code="slug_conflict")

        data = payload.model_dump(exclude={"tag_labels"})
        event = Event(**data)
        event.tags = await self._resolve_tags(payload.tag_labels)

        try:
            await self.repository.create(event)
            await record_audit_event(
                self.repository.session,
                actor_id=actor.id,
                action="event.create",
                entity_type="event",
                entity_id=event.id,
                summary=f"Created '{event.event_name}'",
            )
            await self.repository.session.commit()
        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise AppError(
                "Could not save the event: check that referenced values (e.g. talk) are valid.",
                code="invalid_reference",
            ) from exc

        # `updated_at` has a DB-side `onupdate`, so SQLAlchemy expires it
        # after any UPDATE regardless of `expire_on_commit` — it must be
        # explicitly included here or accessing it next would attempt an
        # implicit (sync) lazy-load and crash under the async driver.
        await self.repository.session.refresh(
            event, attribute_names=["tags", "talk", "updated_at"]
        )
        return _to_admin_out(event)

    async def update(
        self, event_id: int, payload: EventAdminUpdate, actor: AdminUser
    ) -> EventAdminOut:
        event = await self._get_or_404(event_id)
        await create_revision(
            self.repository.session,
            entity=event,
            entity_type="event",
            entity_id=event.id,
            actor_id=actor.id,
        )

        for field, value in payload.model_dump(exclude={"tag_labels"}).items():
            setattr(event, field, value)
        event.tags = await self._resolve_tags(payload.tag_labels)

        try:
            await record_audit_event(
                self.repository.session,
                actor_id=actor.id,
                action="event.update",
                entity_type="event",
                entity_id=event.id,
                summary=f"Updated '{event.event_name}'",
            )
            await self.repository.session.commit()
        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise AppError(
                "Could not save the event: check that referenced values (e.g. talk) are valid.",
                code="invalid_reference",
            ) from exc

        # `updated_at` has a DB-side `onupdate`, so SQLAlchemy expires it
        # after any UPDATE regardless of `expire_on_commit` — it must be
        # explicitly included here or accessing it next would attempt an
        # implicit (sync) lazy-load and crash under the async driver.
        await self.repository.session.refresh(
            event, attribute_names=["tags", "talk", "updated_at"]
        )
        return _to_admin_out(event)

    async def _transition(
        self,
        event_id: int,
        actor: AdminUser,
        action: str,
        summary: str,
        apply: Callable[[Event], None],
    ) -> EventAdminOut:
        event = await self._get_or_404(event_id)
        apply(event)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action=action,
            entity_type="event",
            entity_id=event.id,
            summary=summary,
        )
        await self.repository.session.commit()
        # `updated_at` has a DB-side `onupdate`, so SQLAlchemy expires it
        # after any UPDATE regardless of `expire_on_commit` — it must be
        # explicitly included here or accessing it next would attempt an
        # implicit (sync) lazy-load and crash under the async driver.
        await self.repository.session.refresh(
            event, attribute_names=["tags", "talk", "updated_at"]
        )
        return _to_admin_out(event)

    async def publish(self, event_id: int, actor: AdminUser) -> EventAdminOut:
        def apply(event: Event) -> None:
            event.publication_status = "PUBLISHED"
            event.publish_at = None
            event.unpublish_at = None
            if event.published_at is None:
                event.published_at = datetime.now(UTC)

        return await self._transition(event_id, actor, "event.publish", "Published", apply)

    async def schedule(
        self, event_id: int, publish_at: datetime, actor: AdminUser
    ) -> EventAdminOut:
        def apply(event: Event) -> None:
            event.publication_status = "SCHEDULED"
            event.publish_at = publish_at

        return await self._transition(
            event_id, actor, "event.schedule", f"Scheduled for {publish_at.isoformat()}", apply
        )

    async def unpublish(self, event_id: int, actor: AdminUser) -> EventAdminOut:
        def apply(event: Event) -> None:
            event.publication_status = "DRAFT"
            event.publish_at = None
            event.unpublish_at = None

        return await self._transition(event_id, actor, "event.unpublish", "Unpublished", apply)

    async def archive(self, event_id: int, actor: AdminUser) -> EventAdminOut:
        def apply(event: Event) -> None:
            event.publication_status = "ARCHIVED"

        return await self._transition(event_id, actor, "event.archive", "Archived", apply)

    async def soft_delete(self, event_id: int, actor: AdminUser) -> EventAdminOut:
        def apply(event: Event) -> None:
            event.deleted_at = datetime.now(UTC)

        return await self._transition(
            event_id, actor, "event.trash", "Moved to trash", apply
        )

    async def restore_from_trash(self, event_id: int, actor: AdminUser) -> EventAdminOut:
        def apply(event: Event) -> None:
            event.deleted_at = None

        return await self._transition(
            event_id, actor, "event.restore_from_trash", "Restored from trash", apply
        )

    async def permanent_delete(self, event_id: int, actor: AdminUser) -> None:
        event = await self._get_or_404(event_id)
        if event.deleted_at is None:
            raise AppError(
                "Move the event to trash before deleting it permanently.", code="not_trashed"
            )
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="event.delete_permanently",
            entity_type="event",
            entity_id=event.id,
            summary=f"Permanently deleted '{event.event_name}'",
        )
        await self.repository.delete(event)
        await self.repository.session.commit()

    async def list_revisions(self, event_id: int) -> list[RevisionOut]:
        await self._get_or_404(event_id)
        revisions = await self.revision_repository.list_for_entity("event", event_id)
        return [
            RevisionOut(
                id=revision.id,
                schema_version=revision.schema_version,
                snapshot=revision.snapshot,
                created_at=revision.created_at,
                created_by_email=revision.created_by.email if revision.created_by else None,
            )
            for revision in revisions
        ]

    async def _get_revision_or_404(self, event_id: int, revision_id: int) -> Revision:
        revision = await self.revision_repository.get(revision_id)
        if revision is None or revision.entity_type != "event" or revision.entity_id != event_id:
            raise NotFoundError("Revision not found.")
        return revision

    async def preview_revision_diff(self, event_id: int, revision_id: int) -> RevisionDiffOut:
        event = await self._get_or_404(event_id)
        revision = await self._get_revision_or_404(event_id, revision_id)
        return RevisionDiffOut(current=snapshot_entity(event), snapshot=revision.snapshot)

    async def restore_revision(
        self, event_id: int, revision_id: int, actor: AdminUser
    ) -> EventAdminOut:
        event = await self._get_or_404(event_id)
        revision = await self._get_revision_or_404(event_id, revision_id)

        applied, ignored = merge_revision_snapshot(revision.snapshot, _UPDATE_FIELDS)
        current_values = {field: getattr(event, field) for field in _UPDATE_FIELDS}
        merged = {
            **current_values,
            **applied,
            "tag_labels": [tag.label for tag in event.tags],
        }
        # Validated through the same schema ordinary updates use, so a
        # restore can never write a value that wouldn't otherwise be allowed.
        validated = EventAdminUpdate(**merged)

        await create_revision(
            self.repository.session,
            entity=event,
            entity_type="event",
            entity_id=event.id,
            actor_id=actor.id,
        )
        for field, value in validated.model_dump(exclude={"tag_labels"}).items():
            setattr(event, field, value)

        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="event.restore_revision",
            entity_type="event",
            entity_id=event.id,
            summary=f"Restored revision #{revision_id}",
            context={"ignored_fields": ignored} if ignored else None,
        )
        await self.repository.session.commit()
        # `updated_at` has a DB-side `onupdate`, so SQLAlchemy expires it
        # after any UPDATE regardless of `expire_on_commit` — it must be
        # explicitly included here or accessing it next would attempt an
        # implicit (sync) lazy-load and crash under the async driver.
        await self.repository.session.refresh(
            event, attribute_names=["tags", "talk", "updated_at"]
        )
        return _to_admin_out(event)
