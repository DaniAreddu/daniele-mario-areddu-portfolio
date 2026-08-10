"""Public homepage content: settings singleton + resolved featured items.

Feature resolution reuses each entity type's existing public `list_all()`
(already filtered by `visible_now()`) rather than re-implementing the
publish/soft-delete predicate here — a feature pointing at an entity that
is no longer visible simply disappears from the response instead of
crashing or leaking draft content.
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.site_settings import HomepageSettings
from app.repositories.event_repository import EventRepository
from app.repositories.homepage_repository import HomepageFeatureRepository
from app.repositories.project_repository import ProjectRepository
from app.schemas.homepage import HomepageFeatureItemOut, HomepageOut
from app.services.localization import pick
from app.services.singleton_admin_service import get_or_create_singleton


class HomepageService:
    def __init__(
        self,
        session: AsyncSession,
        feature_repository: HomepageFeatureRepository,
        project_repository: ProjectRepository,
        event_repository: EventRepository,
    ) -> None:
        self.session = session
        self.feature_repository = feature_repository
        self.project_repository = project_repository
        self.event_repository = event_repository

    async def get(self, locale: str) -> HomepageOut:
        settings = await get_or_create_singleton(self.session, HomepageSettings)
        features = await self.feature_repository.list_all()

        projects_by_id = {p.id: p for p in await self.project_repository.list_all()}
        events_by_id = {e.id: e for e in await self.event_repository.list_all()}

        resolved: list[HomepageFeatureItemOut] = []
        for feature in features:
            if feature.entity_type == "project":
                project = projects_by_id.get(feature.entity_id)
                if project is None:
                    continue
                resolved.append(
                    HomepageFeatureItemOut(
                        entity_type="project",
                        title=pick(project, "title", locale),
                        summary=pick(project, "summary", locale),
                        url_path=f"/projects/{project.slug}",
                        image_url=project.cover_image_url,
                    )
                )
            elif feature.entity_type == "event":
                event = events_by_id.get(feature.entity_id)
                if event is None:
                    continue
                summary = (
                    pick(event, "short_description", locale)
                    if event.short_description_en
                    else ""
                )
                resolved.append(
                    HomepageFeatureItemOut(
                        entity_type="event",
                        title=event.event_name,
                        summary=summary,
                        url_path=f"/speaking/{event.slug}",
                        image_url=event.image,
                    )
                )

        return HomepageOut(
            hero_eyebrow=pick(settings, "hero_eyebrow", locale),
            hero_headline=pick(settings, "hero_headline", locale),
            hero_subheadline=pick(settings, "hero_subheadline", locale),
            primary_cta_label=pick(settings, "primary_cta_label", locale)
            if settings.primary_cta_label_en
            else None,
            primary_cta_url=settings.primary_cta_url,
            secondary_cta_label=pick(settings, "secondary_cta_label", locale)
            if settings.secondary_cta_label_en
            else None,
            secondary_cta_url=settings.secondary_cta_url,
            section_order=settings.section_order,
            section_visibility=settings.section_visibility,
            features=resolved,
        )
