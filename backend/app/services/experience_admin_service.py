"""Admin CRUD + lifecycle for Experience — uses LifecycleAdminMixin for the
publish/schedule/unpublish/archive/trash/restore/permanent-delete machinery
(see lifecycle_admin_service.py) and owns create/update/restore_revision
itself, following the pattern established by Event/ProjectAdminService.
"""

from __future__ import annotations

import re

from sqlalchemy.exc import IntegrityError

from app.core.errors import AppError
from app.models.admin_user import AdminUser
from app.models.experience import Experience
from app.models.tag import Tag
from app.repositories.experience_repository import ExperienceRepository
from app.repositories.revision_repository import RevisionRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.experience_admin import (
    ExperienceAdminOut,
    ExperienceAdminWrite,
    ExperienceListItemAdminOut,
    ExperienceRevisionOut,
)
from app.services._admin_common import create_revision, merge_revision_snapshot, record_audit_event
from app.services.lifecycle_admin_service import LifecycleAdminMixin

_UPDATE_FIELDS = set(ExperienceAdminWrite.model_fields.keys()) - {"tag_labels"}


def _slugify_tag(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def _to_admin_out(experience: Experience) -> ExperienceAdminOut:
    return ExperienceAdminOut(
        id=experience.id,
        organization=experience.organization,
        role_en=experience.role_en,
        role_it=experience.role_it,
        employment_type=experience.employment_type,
        location=experience.location,
        location_mode=experience.location_mode,
        start_date=experience.start_date,
        end_date=experience.end_date,
        is_current=experience.is_current,
        summary_en=experience.summary_en,
        summary_it=experience.summary_it,
        long_description_en=experience.long_description_en,
        long_description_it=experience.long_description_it,
        highlights_en=experience.highlights_en,
        highlights_it=experience.highlights_it,
        achievements_en=experience.achievements_en,
        achievements_it=experience.achievements_it,
        company_url=experience.company_url,
        logo_media_url=experience.logo_media_url,
        is_featured=experience.is_featured,
        sort_order=experience.sort_order,
        internal_notes=experience.internal_notes,
        tags=sorted(tag.label for tag in experience.tags),
        publication_status=experience.publication_status,
        publish_at=experience.publish_at,
        unpublish_at=experience.unpublish_at,
        published_at=experience.published_at,
        deleted_at=experience.deleted_at,
        created_at=experience.created_at,
        updated_at=experience.updated_at,
    )


def _to_list_item(experience: Experience) -> ExperienceListItemAdminOut:
    return ExperienceListItemAdminOut(
        id=experience.id,
        organization=experience.organization,
        role_en=experience.role_en,
        is_current=experience.is_current,
        sort_order=experience.sort_order,
        publication_status=experience.publication_status,
        deleted_at=experience.deleted_at,
    )


class ExperienceAdminService(LifecycleAdminMixin[ExperienceAdminOut]):
    entity_type = "experience"

    def __init__(
        self,
        repository: ExperienceRepository,
        tag_repository: TagRepository,
        revision_repository: RevisionRepository,
    ) -> None:
        self.repository = repository
        self.tag_repository = tag_repository
        self.revision_repository = revision_repository

    def _to_out(self, entity: Experience) -> ExperienceAdminOut:
        return _to_admin_out(entity)

    def _refresh_attrs(self) -> list[str]:
        return ["tags"]

    async def list_all(self, *, include_trashed: bool = False) -> list[ExperienceListItemAdminOut]:
        items = await self.repository.list_all_admin(include_trashed=include_trashed)
        return [_to_list_item(item) for item in items]

    async def get(self, experience_id: int) -> ExperienceAdminOut:
        experience = await self._get_or_404(experience_id)
        return _to_admin_out(experience)

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

    async def create(self, payload: ExperienceAdminWrite, actor: AdminUser) -> ExperienceAdminOut:
        data = payload.model_dump(exclude={"tag_labels"})
        experience = Experience(**data)
        experience.tags = await self._resolve_tags(payload.tag_labels)
        try:
            await self.repository.create(experience)
            await record_audit_event(
                self.repository.session,
                actor_id=actor.id,
                action="experience.create",
                entity_type="experience",
                entity_id=experience.id,
                summary=f"Created '{experience.organization}'",
            )
            await self.repository.session.commit()
        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise AppError(
                "Could not save the experience entry.", code="invalid_reference"
            ) from exc
        await self.repository.session.refresh(experience, attribute_names=["tags"])
        return _to_admin_out(experience)

    async def update(
        self, experience_id: int, payload: ExperienceAdminWrite, actor: AdminUser
    ) -> ExperienceAdminOut:
        experience = await self._get_or_404(experience_id)
        await create_revision(
            self.repository.session,
            entity=experience,
            entity_type="experience",
            entity_id=experience.id,
            actor_id=actor.id,
        )
        for field, value in payload.model_dump(exclude={"tag_labels"}).items():
            setattr(experience, field, value)
        experience.tags = await self._resolve_tags(payload.tag_labels)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="experience.update",
            entity_type="experience",
            entity_id=experience.id,
            summary=f"Updated '{experience.organization}'",
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(experience, attribute_names=["tags", "updated_at"])
        return _to_admin_out(experience)

    async def list_revisions(self, experience_id: int) -> list[ExperienceRevisionOut]:  # type: ignore[override]
        await self._get_or_404(experience_id)
        revisions = await self.revision_repository.list_for_entity("experience", experience_id)
        return [
            ExperienceRevisionOut(
                id=revision.id,
                schema_version=revision.schema_version,
                snapshot=revision.snapshot,
                created_at=revision.created_at,
                created_by_email=revision.created_by.email if revision.created_by else None,
            )
            for revision in revisions
        ]

    async def restore_revision(
        self, experience_id: int, revision_id: int, actor: AdminUser
    ) -> ExperienceAdminOut:
        experience = await self._get_or_404(experience_id)
        revision = await self._get_revision_or_404(experience_id, revision_id)

        applied, ignored = merge_revision_snapshot(revision.snapshot, _UPDATE_FIELDS)
        current_values = {field: getattr(experience, field) for field in _UPDATE_FIELDS}
        merged = {
            **current_values,
            **applied,
            "tag_labels": [tag.label for tag in experience.tags],
        }
        validated = ExperienceAdminWrite(**merged)

        await create_revision(
            self.repository.session,
            entity=experience,
            entity_type="experience",
            entity_id=experience.id,
            actor_id=actor.id,
        )
        for field, value in validated.model_dump(exclude={"tag_labels"}).items():
            setattr(experience, field, value)

        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="experience.restore_revision",
            entity_type="experience",
            entity_id=experience.id,
            summary=f"Restored revision #{revision_id}",
            context={"ignored_fields": ignored} if ignored else None,
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(
            experience, attribute_names=["tags", "updated_at"]
        )
        return _to_admin_out(experience)
