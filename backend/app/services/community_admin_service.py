"""Admin CRUD + lifecycle for community activities (CommunityProfile is a
singleton handled separately via SingletonAdminService — see
admin_community.py).
"""

from __future__ import annotations

from app.core.errors import AppError
from app.models.admin_user import AdminUser
from app.models.community import CommunityActivity
from app.repositories.community_repository import CommunityRepository
from app.repositories.revision_repository import RevisionRepository
from app.schemas.community_admin import (
    CommunityActivityAdminOut,
    CommunityActivityAdminWrite,
    CommunityActivityListItemAdminOut,
    CommunityActivityRevisionOut,
)
from app.services._admin_common import create_revision, merge_revision_snapshot, record_audit_event
from app.services.lifecycle_admin_service import LifecycleAdminMixin

_UPDATE_FIELDS = set(CommunityActivityAdminWrite.model_fields.keys())


class _ActivityRepoAdapter:
    """Adapts CommunityRepository's activity-specific method names to the
    plain get_by_id/delete/session shape LifecycleAdminMixin expects,
    without renaming the underlying repository's clearer method names
    (which also serves the unrelated CommunityProfile singleton).
    """

    def __init__(self, repository: CommunityRepository) -> None:
        self._repository = repository
        self.session = repository.session

    async def get_by_id(self, entity_id: int) -> CommunityActivity | None:
        return await self._repository.get_activity_by_id(entity_id)

    async def delete(self, entity: CommunityActivity) -> None:
        await self._repository.delete_activity(entity)


def _to_admin_out(activity: CommunityActivity) -> CommunityActivityAdminOut:
    return CommunityActivityAdminOut(
        id=activity.id,
        slug=activity.slug,
        title_en=activity.title_en,
        title_it=activity.title_it,
        description_en=activity.description_en,
        description_it=activity.description_it,
        activity_date=activity.activity_date,
        activity_type=activity.activity_type,
        url=activity.url,
        logo_media_url=activity.logo_media_url,
        is_featured=activity.is_featured,
        sort_order=activity.sort_order,
        internal_notes=activity.internal_notes,
        publication_status=activity.publication_status,
        publish_at=activity.publish_at,
        unpublish_at=activity.unpublish_at,
        published_at=activity.published_at,
        deleted_at=activity.deleted_at,
        created_at=activity.created_at,
        updated_at=activity.updated_at,
    )


def _to_list_item(activity: CommunityActivity) -> CommunityActivityListItemAdminOut:
    return CommunityActivityListItemAdminOut(
        id=activity.id,
        slug=activity.slug,
        title_en=activity.title_en,
        activity_type=activity.activity_type,
        sort_order=activity.sort_order,
        publication_status=activity.publication_status,
        deleted_at=activity.deleted_at,
    )


class CommunityActivityAdminService(LifecycleAdminMixin[CommunityActivityAdminOut]):
    entity_type = "community_activity"

    def __init__(
        self, repository: CommunityRepository, revision_repository: RevisionRepository
    ) -> None:
        self.community_repository = repository
        self.repository = _ActivityRepoAdapter(repository)
        self.revision_repository = revision_repository

    def _to_out(self, entity: CommunityActivity) -> CommunityActivityAdminOut:
        return _to_admin_out(entity)

    async def list_all(
        self, *, include_trashed: bool = False
    ) -> list[CommunityActivityListItemAdminOut]:
        items = await self.community_repository.list_activities_admin(
            include_trashed=include_trashed
        )
        return [_to_list_item(item) for item in items]

    async def get(self, activity_id: int) -> CommunityActivityAdminOut:
        return _to_admin_out(await self._get_or_404(activity_id))

    async def create(
        self, payload: CommunityActivityAdminWrite, actor: AdminUser
    ) -> CommunityActivityAdminOut:
        if await self.community_repository.get_activity_by_slug_any(payload.slug) is not None:
            raise AppError("An activity with this slug already exists.", code="slug_conflict")
        activity = CommunityActivity(**payload.model_dump())
        await self.community_repository.create_activity(activity)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="community_activity.create",
            entity_type="community_activity",
            entity_id=activity.id,
            summary=f"Created '{activity.title_en}'",
        )
        await self.repository.session.commit()
        return _to_admin_out(activity)

    async def update(
        self, activity_id: int, payload: CommunityActivityAdminWrite, actor: AdminUser
    ) -> CommunityActivityAdminOut:
        activity = await self._get_or_404(activity_id)
        await create_revision(
            self.repository.session,
            entity=activity,
            entity_type="community_activity",
            entity_id=activity.id,
            actor_id=actor.id,
        )
        for field, value in payload.model_dump().items():
            setattr(activity, field, value)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="community_activity.update",
            entity_type="community_activity",
            entity_id=activity.id,
            summary=f"Updated '{activity.title_en}'",
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(activity, attribute_names=["updated_at"])
        return _to_admin_out(activity)

    async def list_revisions(self, activity_id: int) -> list[CommunityActivityRevisionOut]:  # type: ignore[override]
        await self._get_or_404(activity_id)
        revisions = await self.revision_repository.list_for_entity(
            "community_activity", activity_id
        )
        return [
            CommunityActivityRevisionOut(
                id=revision.id,
                schema_version=revision.schema_version,
                snapshot=revision.snapshot,
                created_at=revision.created_at,
                created_by_email=revision.created_by.email if revision.created_by else None,
            )
            for revision in revisions
        ]

    async def restore_revision(
        self, activity_id: int, revision_id: int, actor: AdminUser
    ) -> CommunityActivityAdminOut:
        activity = await self._get_or_404(activity_id)
        revision = await self._get_revision_or_404(activity_id, revision_id)

        applied, ignored = merge_revision_snapshot(revision.snapshot, _UPDATE_FIELDS)
        current_values = {field: getattr(activity, field) for field in _UPDATE_FIELDS}
        validated = CommunityActivityAdminWrite(**{**current_values, **applied})

        await create_revision(
            self.repository.session,
            entity=activity,
            entity_type="community_activity",
            entity_id=activity.id,
            actor_id=actor.id,
        )
        for field, value in validated.model_dump().items():
            setattr(activity, field, value)

        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="community_activity.restore_revision",
            entity_type="community_activity",
            entity_id=activity.id,
            summary=f"Restored revision #{revision_id}",
            context={"ignored_fields": ignored} if ignored else None,
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(activity, attribute_names=["updated_at"])
        return _to_admin_out(activity)
