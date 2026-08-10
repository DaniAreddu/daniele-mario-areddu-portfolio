"""Admin CRUD for the homepage's curated "featured items" join table.

`HomepageSettings` itself (hero copy, CTAs, section order/visibility) is a
singleton and is administered directly via `SingletonAdminService` in the
router, exactly like Profile/Biography/CommunityProfile — no separate
service needed for it here.
"""

from __future__ import annotations

from app.core.errors import AppError, NotFoundError
from app.models.admin_user import AdminUser
from app.models.site_settings import HomepageFeature
from app.repositories.event_repository import EventRepository
from app.repositories.homepage_repository import HomepageFeatureRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.homepage_admin import HomepageFeatureAdminOut, HomepageFeatureAdminWrite
from app.services._admin_common import record_audit_event


def _to_out(feature: HomepageFeature) -> HomepageFeatureAdminOut:
    return HomepageFeatureAdminOut(
        id=feature.id,
        entity_type=feature.entity_type,
        entity_id=feature.entity_id,
        sort_order=feature.sort_order,
    )


class HomepageFeatureAdminService:
    def __init__(
        self,
        repository: HomepageFeatureRepository,
        project_repository: ProjectRepository,
        event_repository: EventRepository,
    ) -> None:
        self.repository = repository
        self.project_repository = project_repository
        self.event_repository = event_repository

    async def list_all(self) -> list[HomepageFeatureAdminOut]:
        features = await self.repository.list_all()
        return [_to_out(feature) for feature in features]

    async def _get_or_404(self, feature_id: int) -> HomepageFeature:
        feature = await self.repository.get_by_id(feature_id)
        if feature is None:
            raise NotFoundError("Homepage feature not found.")
        return feature

    async def _validate_entity_exists(self, entity_type: str, entity_id: int) -> None:
        entity = (
            await self.project_repository.get_by_id(entity_id)
            if entity_type == "project"
            else await self.event_repository.get_by_id(entity_id)
        )
        if entity is None:
            raise AppError(
                f"No {entity_type} with id {entity_id} exists.", code="invalid_reference"
            )

    async def create(
        self, payload: HomepageFeatureAdminWrite, actor: AdminUser
    ) -> HomepageFeatureAdminOut:
        await self._validate_entity_exists(payload.entity_type, payload.entity_id)
        feature = HomepageFeature(**payload.model_dump())
        await self.repository.create(feature)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="homepage_feature.create",
            entity_type="homepage_feature",
            entity_id=feature.id,
            summary=f"Featured {payload.entity_type} #{payload.entity_id} on the homepage",
        )
        await self.repository.session.commit()
        return _to_out(feature)

    async def delete(self, feature_id: int, actor: AdminUser) -> None:
        feature = await self._get_or_404(feature_id)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="homepage_feature.delete",
            entity_type="homepage_feature",
            entity_id=feature.id,
            summary=f"Unfeatured {feature.entity_type} #{feature.entity_id} from the homepage",
        )
        await self.repository.delete(feature)
        await self.repository.session.commit()
