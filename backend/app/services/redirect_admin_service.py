"""Admin CRUD for redirects — plain list, no draft/publish lifecycle.

Two safety properties are enforced here, on top of the schema-layer
`/`-prefix and self-reference checks: no duplicate `source_path`, and no
redirect chain that would eventually loop back to its own source. Both are
checked in Python against the small, fully in-memory redirect set (a
personal portfolio's redirect table is expected to stay in the tens of
rows, not thousands) rather than a recursive SQL query.
"""

from __future__ import annotations

from app.core.errors import AppError, NotFoundError
from app.models.admin_user import AdminUser
from app.models.redirect import Redirect
from app.repositories.redirect_repository import RedirectRepository
from app.schemas.redirect_admin import RedirectAdminOut, RedirectAdminWrite
from app.services._admin_common import record_audit_event

_MAX_CHAIN_HOPS = 20


def _to_out(redirect: Redirect) -> RedirectAdminOut:
    return RedirectAdminOut(
        id=redirect.id,
        source_path=redirect.source_path,
        destination_path=redirect.destination_path,
        status_code=redirect.status_code,
        enabled=redirect.enabled,
        created_at=redirect.created_at,
        updated_at=redirect.updated_at,
    )


class RedirectAdminService:
    def __init__(self, repository: RedirectRepository) -> None:
        self.repository = repository

    async def list_all(self) -> list[RedirectAdminOut]:
        redirects = await self.repository.list_all()
        return [_to_out(redirect) for redirect in redirects]

    async def _get_or_404(self, redirect_id: int) -> Redirect:
        redirect = await self.repository.get_by_id(redirect_id)
        if redirect is None:
            raise NotFoundError("Redirect not found.")
        return redirect

    async def _check_for_loop(
        self, source_path: str, destination_path: str, *, exclude_id: int | None
    ) -> None:
        existing = await self.repository.list_all()
        by_source = {
            r.source_path: r.destination_path for r in existing if r.id != exclude_id
        }
        current = destination_path
        for _ in range(_MAX_CHAIN_HOPS):
            if current == source_path:
                raise AppError(
                    "This redirect would create a loop with an existing redirect.",
                    code="redirect_loop",
                )
            if current not in by_source:
                return
            current = by_source[current]
        raise AppError(
            "This redirect chain is too long (possible loop).", code="redirect_loop"
        )

    async def create(self, payload: RedirectAdminWrite, actor: AdminUser) -> RedirectAdminOut:
        if await self.repository.get_by_source_path(payload.source_path) is not None:
            raise AppError(
                "A redirect from this path already exists.", code="source_path_conflict"
            )
        await self._check_for_loop(payload.source_path, payload.destination_path, exclude_id=None)

        redirect = Redirect(**payload.model_dump())
        await self.repository.create(redirect)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="redirect.create",
            entity_type="redirect",
            entity_id=redirect.id,
            summary=f"Created redirect '{redirect.source_path}' -> '{redirect.destination_path}'",
        )
        await self.repository.session.commit()
        return _to_out(redirect)

    async def update(
        self, redirect_id: int, payload: RedirectAdminWrite, actor: AdminUser
    ) -> RedirectAdminOut:
        redirect = await self._get_or_404(redirect_id)
        existing_with_source = await self.repository.get_by_source_path(payload.source_path)
        if existing_with_source is not None and existing_with_source.id != redirect_id:
            raise AppError(
                "A redirect from this path already exists.", code="source_path_conflict"
            )
        await self._check_for_loop(
            payload.source_path, payload.destination_path, exclude_id=redirect_id
        )

        for field, value in payload.model_dump().items():
            setattr(redirect, field, value)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="redirect.update",
            entity_type="redirect",
            entity_id=redirect.id,
            summary=f"Updated redirect '{redirect.source_path}' -> '{redirect.destination_path}'",
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(redirect, attribute_names=["updated_at"])
        return _to_out(redirect)

    async def delete(self, redirect_id: int, actor: AdminUser) -> None:
        redirect = await self._get_or_404(redirect_id)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="redirect.delete",
            entity_type="redirect",
            entity_id=redirect.id,
            summary=f"Deleted redirect '{redirect.source_path}'",
        )
        await self.repository.delete(redirect)
        await self.repository.session.commit()
