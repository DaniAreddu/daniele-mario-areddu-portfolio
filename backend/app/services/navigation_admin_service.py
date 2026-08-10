"""Admin CRUD for navigation items — plain list, no draft/publish lifecycle
(mirrors skill_admin_service.py's rationale: a nav item is a structured
settings-like row, not long-form content). Audit logging still applies.
"""

from __future__ import annotations

from app.core.errors import NotFoundError
from app.models.admin_user import AdminUser
from app.models.navigation_item import NavigationItem
from app.repositories.navigation_repository import NavigationRepository
from app.schemas.navigation_admin import NavigationItemAdminOut, NavigationItemAdminWrite
from app.services._admin_common import record_audit_event


def _to_out(item: NavigationItem) -> NavigationItemAdminOut:
    return NavigationItemAdminOut(
        id=item.id,
        label_en=item.label_en,
        label_it=item.label_it,
        target=item.target,
        placement=item.placement,
        is_external=item.is_external,
        open_in_new_tab=item.open_in_new_tab,
        enabled=item.enabled,
        sort_order=item.sort_order,
        created_at=item.created_at,
        updated_at=item.updated_at,
    )


class NavigationAdminService:
    def __init__(self, repository: NavigationRepository) -> None:
        self.repository = repository

    async def list_all(self) -> list[NavigationItemAdminOut]:
        items = await self.repository.list_all()
        return [_to_out(item) for item in items]

    async def _get_or_404(self, item_id: int) -> NavigationItem:
        item = await self.repository.get_by_id(item_id)
        if item is None:
            raise NotFoundError("Navigation item not found.")
        return item

    async def create(
        self, payload: NavigationItemAdminWrite, actor: AdminUser
    ) -> NavigationItemAdminOut:
        item = NavigationItem(**payload.model_dump())
        await self.repository.create(item)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="navigation_item.create",
            entity_type="navigation_item",
            entity_id=item.id,
            summary=f"Created nav item '{item.label_en}'",
        )
        await self.repository.session.commit()
        return _to_out(item)

    async def update(
        self, item_id: int, payload: NavigationItemAdminWrite, actor: AdminUser
    ) -> NavigationItemAdminOut:
        item = await self._get_or_404(item_id)
        for field, value in payload.model_dump().items():
            setattr(item, field, value)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="navigation_item.update",
            entity_type="navigation_item",
            entity_id=item.id,
            summary=f"Updated nav item '{item.label_en}'",
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(item, attribute_names=["updated_at"])
        return _to_out(item)

    async def delete(self, item_id: int, actor: AdminUser) -> None:
        item = await self._get_or_404(item_id)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="navigation_item.delete",
            entity_type="navigation_item",
            entity_id=item.id,
            summary=f"Deleted nav item '{item.label_en}'",
        )
        await self.repository.delete(item)
        await self.repository.session.commit()
