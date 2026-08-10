"""Admin CRUD + lifecycle for Education — see experience_admin_service.py
for the pattern this mirrors (no tags needed here, so it's a shorter
version of the same shape).
"""

from __future__ import annotations

from app.models.admin_user import AdminUser
from app.models.education import Education
from app.repositories.education_repository import EducationRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.education_admin import (
    EducationAdminOut,
    EducationAdminWrite,
    EducationListItemAdminOut,
    EducationRevisionOut,
)
from app.services._admin_common import create_revision, merge_revision_snapshot, record_audit_event
from app.services.lifecycle_admin_service import LifecycleAdminMixin

_UPDATE_FIELDS = set(EducationAdminWrite.model_fields.keys())


def _to_admin_out(education: Education) -> EducationAdminOut:
    return EducationAdminOut(
        id=education.id,
        institution=education.institution,
        degree_en=education.degree_en,
        degree_it=education.degree_it,
        field=education.field,
        location=education.location,
        start_year=education.start_year,
        end_year=education.end_year,
        is_ongoing=education.is_ongoing,
        description_en=education.description_en,
        description_it=education.description_it,
        activities=education.activities,
        url=education.url,
        logo_media_url=education.logo_media_url,
        sort_order=education.sort_order,
        internal_notes=education.internal_notes,
        publication_status=education.publication_status,
        publish_at=education.publish_at,
        unpublish_at=education.unpublish_at,
        published_at=education.published_at,
        deleted_at=education.deleted_at,
        created_at=education.created_at,
        updated_at=education.updated_at,
    )


def _to_list_item(education: Education) -> EducationListItemAdminOut:
    return EducationListItemAdminOut(
        id=education.id,
        institution=education.institution,
        degree_en=education.degree_en,
        sort_order=education.sort_order,
        publication_status=education.publication_status,
        deleted_at=education.deleted_at,
    )


class EducationAdminService(LifecycleAdminMixin[EducationAdminOut]):
    entity_type = "education"

    def __init__(
        self, repository: EducationRepository, revision_repository: RevisionRepository
    ) -> None:
        self.repository = repository
        self.revision_repository = revision_repository

    def _to_out(self, entity: Education) -> EducationAdminOut:
        return _to_admin_out(entity)

    async def list_all(self, *, include_trashed: bool = False) -> list[EducationListItemAdminOut]:
        items = await self.repository.list_all_admin(include_trashed=include_trashed)
        return [_to_list_item(item) for item in items]

    async def get(self, education_id: int) -> EducationAdminOut:
        return _to_admin_out(await self._get_or_404(education_id))

    async def create(self, payload: EducationAdminWrite, actor: AdminUser) -> EducationAdminOut:
        education = Education(**payload.model_dump())
        await self.repository.create(education)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="education.create",
            entity_type="education",
            entity_id=education.id,
            summary=f"Created '{education.institution}'",
        )
        await self.repository.session.commit()
        return _to_admin_out(education)

    async def update(
        self, education_id: int, payload: EducationAdminWrite, actor: AdminUser
    ) -> EducationAdminOut:
        education = await self._get_or_404(education_id)
        await create_revision(
            self.repository.session,
            entity=education,
            entity_type="education",
            entity_id=education.id,
            actor_id=actor.id,
        )
        for field, value in payload.model_dump().items():
            setattr(education, field, value)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="education.update",
            entity_type="education",
            entity_id=education.id,
            summary=f"Updated '{education.institution}'",
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(education, attribute_names=["updated_at"])
        return _to_admin_out(education)

    async def list_revisions(self, education_id: int) -> list[EducationRevisionOut]:  # type: ignore[override]
        await self._get_or_404(education_id)
        revisions = await self.revision_repository.list_for_entity("education", education_id)
        return [
            EducationRevisionOut(
                id=revision.id,
                schema_version=revision.schema_version,
                snapshot=revision.snapshot,
                created_at=revision.created_at,
                created_by_email=revision.created_by.email if revision.created_by else None,
            )
            for revision in revisions
        ]

    async def restore_revision(
        self, education_id: int, revision_id: int, actor: AdminUser
    ) -> EducationAdminOut:
        education = await self._get_or_404(education_id)
        revision = await self._get_revision_or_404(education_id, revision_id)

        applied, ignored = merge_revision_snapshot(revision.snapshot, _UPDATE_FIELDS)
        current_values = {field: getattr(education, field) for field in _UPDATE_FIELDS}
        validated = EducationAdminWrite(**{**current_values, **applied})

        await create_revision(
            self.repository.session,
            entity=education,
            entity_type="education",
            entity_id=education.id,
            actor_id=actor.id,
        )
        for field, value in validated.model_dump().items():
            setattr(education, field, value)

        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="education.restore_revision",
            entity_type="education",
            entity_id=education.id,
            summary=f"Restored revision #{revision_id}",
            context={"ignored_fields": ignored} if ignored else None,
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(education, attribute_names=["updated_at"])
        return _to_admin_out(education)
