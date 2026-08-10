"""Admin CRUD + lifecycle for Recognition (certifications/awards/
recognition/publications) — mirrors education_admin_service.py's shape
(no tags, no slug uniqueness needed).
"""

from __future__ import annotations

from app.models.admin_user import AdminUser
from app.models.recognition import Recognition
from app.repositories.recognition_repository import RecognitionRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.recognition_admin import (
    RecognitionAdminOut,
    RecognitionAdminWrite,
    RecognitionListItemAdminOut,
    RecognitionRevisionOut,
)
from app.services._admin_common import create_revision, merge_revision_snapshot, record_audit_event
from app.services.lifecycle_admin_service import LifecycleAdminMixin

_UPDATE_FIELDS = set(RecognitionAdminWrite.model_fields.keys())


def _to_admin_out(recognition: Recognition) -> RecognitionAdminOut:
    return RecognitionAdminOut(
        id=recognition.id,
        kind=recognition.kind,
        title_en=recognition.title_en,
        title_it=recognition.title_it,
        issuer=recognition.issuer,
        description_en=recognition.description_en,
        description_it=recognition.description_it,
        date_awarded=recognition.date_awarded,
        url=recognition.url,
        sort_order=recognition.sort_order,
        internal_notes=recognition.internal_notes,
        publication_status=recognition.publication_status,
        publish_at=recognition.publish_at,
        unpublish_at=recognition.unpublish_at,
        published_at=recognition.published_at,
        deleted_at=recognition.deleted_at,
        created_at=recognition.created_at,
        updated_at=recognition.updated_at,
    )


def _to_list_item(recognition: Recognition) -> RecognitionListItemAdminOut:
    return RecognitionListItemAdminOut(
        id=recognition.id,
        kind=recognition.kind,
        title_en=recognition.title_en,
        sort_order=recognition.sort_order,
        publication_status=recognition.publication_status,
        deleted_at=recognition.deleted_at,
    )


class RecognitionAdminService(LifecycleAdminMixin[RecognitionAdminOut]):
    entity_type = "recognition"

    def __init__(
        self, repository: RecognitionRepository, revision_repository: RevisionRepository
    ) -> None:
        self.repository = repository
        self.revision_repository = revision_repository

    def _to_out(self, entity: Recognition) -> RecognitionAdminOut:
        return _to_admin_out(entity)

    async def list_all(self, *, include_trashed: bool = False) -> list[RecognitionListItemAdminOut]:
        items = await self.repository.list_all_admin(include_trashed=include_trashed)
        return [_to_list_item(item) for item in items]

    async def get(self, recognition_id: int) -> RecognitionAdminOut:
        return _to_admin_out(await self._get_or_404(recognition_id))

    async def create(self, payload: RecognitionAdminWrite, actor: AdminUser) -> RecognitionAdminOut:
        recognition = Recognition(**payload.model_dump())
        await self.repository.create(recognition)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="recognition.create",
            entity_type="recognition",
            entity_id=recognition.id,
            summary=f"Created '{recognition.title_en}'",
        )
        await self.repository.session.commit()
        return _to_admin_out(recognition)

    async def update(
        self, recognition_id: int, payload: RecognitionAdminWrite, actor: AdminUser
    ) -> RecognitionAdminOut:
        recognition = await self._get_or_404(recognition_id)
        await create_revision(
            self.repository.session,
            entity=recognition,
            entity_type="recognition",
            entity_id=recognition.id,
            actor_id=actor.id,
        )
        for field, value in payload.model_dump().items():
            setattr(recognition, field, value)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="recognition.update",
            entity_type="recognition",
            entity_id=recognition.id,
            summary=f"Updated '{recognition.title_en}'",
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(recognition, attribute_names=["updated_at"])
        return _to_admin_out(recognition)

    async def list_revisions(self, recognition_id: int) -> list[RecognitionRevisionOut]:  # type: ignore[override]
        await self._get_or_404(recognition_id)
        revisions = await self.revision_repository.list_for_entity("recognition", recognition_id)
        return [
            RecognitionRevisionOut(
                id=revision.id,
                schema_version=revision.schema_version,
                snapshot=revision.snapshot,
                created_at=revision.created_at,
                created_by_email=revision.created_by.email if revision.created_by else None,
            )
            for revision in revisions
        ]

    async def restore_revision(
        self, recognition_id: int, revision_id: int, actor: AdminUser
    ) -> RecognitionAdminOut:
        recognition = await self._get_or_404(recognition_id)
        revision = await self._get_revision_or_404(recognition_id, revision_id)

        applied, ignored = merge_revision_snapshot(revision.snapshot, _UPDATE_FIELDS)
        current_values = {field: getattr(recognition, field) for field in _UPDATE_FIELDS}
        validated = RecognitionAdminWrite(**{**current_values, **applied})

        await create_revision(
            self.repository.session,
            entity=recognition,
            entity_type="recognition",
            entity_id=recognition.id,
            actor_id=actor.id,
        )
        for field, value in validated.model_dump().items():
            setattr(recognition, field, value)

        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="recognition.restore_revision",
            entity_type="recognition",
            entity_id=recognition.id,
            summary=f"Restored revision #{revision_id}",
            context={"ignored_fields": ignored} if ignored else None,
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(recognition, attribute_names=["updated_at"])
        return _to_admin_out(recognition)
