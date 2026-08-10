"""Admin CRUD for social links — plain list, no draft/publish lifecycle."""

from __future__ import annotations

from app.core.errors import NotFoundError
from app.models.admin_user import AdminUser
from app.models.social_link import SocialLink
from app.repositories.social_link_repository import SocialLinkRepository
from app.schemas.social_link_admin import SocialLinkAdminOut, SocialLinkAdminWrite
from app.services._admin_common import record_audit_event


def _to_out(link: SocialLink) -> SocialLinkAdminOut:
    return SocialLinkAdminOut(
        id=link.id,
        label=link.label,
        url=link.url,
        icon=link.icon,
        enabled=link.enabled,
        sort_order=link.sort_order,
        created_at=link.created_at,
        updated_at=link.updated_at,
    )


class SocialLinkAdminService:
    def __init__(self, repository: SocialLinkRepository) -> None:
        self.repository = repository

    async def list_all(self) -> list[SocialLinkAdminOut]:
        links = await self.repository.list_all()
        return [_to_out(link) for link in links]

    async def _get_or_404(self, link_id: int) -> SocialLink:
        link = await self.repository.get_by_id(link_id)
        if link is None:
            raise NotFoundError("Social link not found.")
        return link

    async def create(self, payload: SocialLinkAdminWrite, actor: AdminUser) -> SocialLinkAdminOut:
        link = SocialLink(**payload.model_dump())
        await self.repository.create(link)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="social_link.create",
            entity_type="social_link",
            entity_id=link.id,
            summary=f"Created social link '{link.label}'",
        )
        await self.repository.session.commit()
        return _to_out(link)

    async def update(
        self, link_id: int, payload: SocialLinkAdminWrite, actor: AdminUser
    ) -> SocialLinkAdminOut:
        link = await self._get_or_404(link_id)
        for field, value in payload.model_dump().items():
            setattr(link, field, value)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="social_link.update",
            entity_type="social_link",
            entity_id=link.id,
            summary=f"Updated social link '{link.label}'",
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(link, attribute_names=["updated_at"])
        return _to_out(link)

    async def delete(self, link_id: int, actor: AdminUser) -> None:
        link = await self._get_or_404(link_id)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="social_link.delete",
            entity_type="social_link",
            entity_id=link.id,
            summary=f"Deleted social link '{link.label}'",
        )
        await self.repository.delete(link)
        await self.repository.session.commit()
