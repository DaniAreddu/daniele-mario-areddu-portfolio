"""Generic admin get/update for singleton content rows (Profile, Biography,
CommunityProfile, SiteSettings, SeoSettings, HomepageSettings).

These are always "live" — there's only ever one row, and editing it takes
effect immediately — so the six-lifecycle-endpoint pattern in
lifecycle_admin_service.py doesn't apply (a sensible domain-specific
adaptation, not a gap: a biography has no meaningful "draft" distinct from
"the current biography"). Revision history and audit logging still apply.
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.admin_user import AdminUser
from app.repositories.revision_repository import RevisionRepository
from app.services._admin_common import create_revision, record_audit_event

ModelT = TypeVar("ModelT")
PayloadT = TypeVar("PayloadT", bound=BaseModel)


async def get_or_create_singleton(session: AsyncSession, model: type[ModelT]) -> ModelT:
    """Shared by admin reads/writes and public reads alike: a singleton
    table's one row is created lazily, with column defaults, the first time
    anything asks for it — so a public endpoint for e.g. SiteSettings never
    404s just because nobody has opened the admin settings page yet.
    """
    result = await session.execute(select(model).limit(1))
    instance = result.scalars().first()
    if instance is None:
        instance = model()
        session.add(instance)
        await session.flush()
        await session.commit()
    return instance


class SingletonAdminService(Generic[ModelT, PayloadT]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[ModelT],
        entity_type: str,
        revision_repository: RevisionRepository,
    ) -> None:
        self.session = session
        self.model = model
        self.entity_type = entity_type
        self.revision_repository = revision_repository

    async def _get_or_create(self) -> ModelT:
        result = await self.session.execute(select(self.model).limit(1))
        instance = result.scalars().first()
        if instance is None:
            instance = self.model()
            self.session.add(instance)
            await self.session.flush()
        return instance

    async def get(self) -> ModelT:
        return await self._get_or_create()

    async def update(self, payload: PayloadT, actor: AdminUser) -> ModelT:
        instance = await self._get_or_create()
        await create_revision(
            self.session,
            entity=instance,
            entity_type=self.entity_type,
            entity_id=instance.id,  # type: ignore[attr-defined]
            actor_id=actor.id,
        )
        for field, value in payload.model_dump().items():
            setattr(instance, field, value)
        await record_audit_event(
            self.session,
            actor_id=actor.id,
            action=f"{self.entity_type}.update",
            entity_type=self.entity_type,
            entity_id=instance.id,  # type: ignore[attr-defined]
            summary=f"Updated {self.entity_type.replace('_', ' ')}",
        )
        await self.session.commit()
        await self.session.refresh(instance, attribute_names=["updated_at"])
        return instance

    async def list_revisions(self) -> list[dict[str, Any]]:
        instance = await self._get_or_create()
        revisions = await self.revision_repository.list_for_entity(
            self.entity_type, instance.id  # type: ignore[attr-defined]
        )
        return [
            {
                "id": revision.id,
                "schema_version": revision.schema_version,
                "snapshot": revision.snapshot,
                "created_at": revision.created_at,
                "created_by_email": revision.created_by.email if revision.created_by else None,
            }
            for revision in revisions
        ]
