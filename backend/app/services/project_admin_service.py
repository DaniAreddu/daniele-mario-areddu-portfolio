"""Admin CRUD, publication lifecycle, and revision history for Projects —
follows the exact pattern established for Speaking events (see
event_admin_service.py and docs/admin-guide.md).
"""

from __future__ import annotations

import re
from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError

from app.core.errors import AppError, NotFoundError
from app.models.admin_user import AdminUser
from app.models.project import Project
from app.models.revision import Revision
from app.models.tag import Tag
from app.repositories.project_repository import ProjectRepository
from app.repositories.revision_repository import RevisionRepository
from app.repositories.tag_repository import TagRepository
from app.schemas.project_admin import (
    ProjectAdminCreate,
    ProjectAdminOut,
    ProjectAdminUpdate,
    ProjectListItemAdminOut,
    ProjectRevisionOut,
)
from app.services._admin_common import create_revision, merge_revision_snapshot, record_audit_event

_UPDATE_FIELDS = set(ProjectAdminUpdate.model_fields.keys()) - {"tag_labels"}


def _slugify_tag(label: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-")


def _to_admin_out(project: Project) -> ProjectAdminOut:
    return ProjectAdminOut(
        id=project.id,
        slug=project.slug,
        title_en=project.title_en,
        title_it=project.title_it,
        summary_en=project.summary_en,
        summary_it=project.summary_it,
        problem_en=project.problem_en,
        problem_it=project.problem_it,
        challenge_en=project.challenge_en,
        challenge_it=project.challenge_it,
        approach_en=project.approach_en,
        approach_it=project.approach_it,
        architecture_en=project.architecture_en,
        architecture_it=project.architecture_it,
        key_decisions_en=project.key_decisions_en,
        key_decisions_it=project.key_decisions_it,
        outcome_en=project.outcome_en,
        outcome_it=project.outcome_it,
        lessons_en=project.lessons_en,
        lessons_it=project.lessons_it,
        confidentiality_note_en=project.confidentiality_note_en,
        confidentiality_note_it=project.confidentiality_note_it,
        external_url=project.external_url,
        cover_image_url=project.cover_image_url,
        is_featured=project.is_featured,
        sort_order=project.sort_order,
        internal_notes=project.internal_notes,
        tags=sorted(tag.label for tag in project.tags),
        related_skills=[skill.skill_name for skill in project.skills],
        publication_status=project.publication_status,
        publish_at=project.publish_at,
        unpublish_at=project.unpublish_at,
        published_at=project.published_at,
        deleted_at=project.deleted_at,
        created_at=project.created_at,
        updated_at=project.updated_at,
    )


def _to_list_item(project: Project) -> ProjectListItemAdminOut:
    return ProjectListItemAdminOut(
        id=project.id,
        slug=project.slug,
        title_en=project.title_en,
        is_featured=project.is_featured,
        sort_order=project.sort_order,
        publication_status=project.publication_status,
        deleted_at=project.deleted_at,
    )


class ProjectAdminService:
    def __init__(
        self,
        repository: ProjectRepository,
        tag_repository: TagRepository,
        revision_repository: RevisionRepository,
    ) -> None:
        self.repository = repository
        self.tag_repository = tag_repository
        self.revision_repository = revision_repository

    async def list_all(self, *, include_trashed: bool = False) -> list[ProjectListItemAdminOut]:
        projects = await self.repository.list_all_admin(include_trashed=include_trashed)
        return [_to_list_item(project) for project in projects]

    async def get(self, project_id: int) -> ProjectAdminOut:
        project = await self._get_or_404(project_id)
        return _to_admin_out(project)

    async def _get_or_404(self, project_id: int) -> Project:
        project = await self.repository.get_by_id(project_id)
        if project is None:
            raise NotFoundError("Project not found.")
        return project

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

    async def create(self, payload: ProjectAdminCreate, actor: AdminUser) -> ProjectAdminOut:
        if await self.repository.get_by_slug_any(payload.slug) is not None:
            raise AppError("A project with this slug already exists.", code="slug_conflict")

        data = payload.model_dump(exclude={"tag_labels"})
        project = Project(**data)
        project.tags = await self._resolve_tags(payload.tag_labels)

        try:
            await self.repository.create(project)
            await record_audit_event(
                self.repository.session,
                actor_id=actor.id,
                action="project.create",
                entity_type="project",
                entity_id=project.id,
                summary=f"Created '{project.title_en}'",
            )
            await self.repository.session.commit()
        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise AppError(
                "Could not save the project: check that referenced values are valid.",
                code="invalid_reference",
            ) from exc

        await self.repository.session.refresh(project, attribute_names=["tags", "skills"])
        return _to_admin_out(project)

    async def update(
        self, project_id: int, payload: ProjectAdminUpdate, actor: AdminUser
    ) -> ProjectAdminOut:
        project = await self._get_or_404(project_id)
        await create_revision(
            self.repository.session,
            entity=project,
            entity_type="project",
            entity_id=project.id,
            actor_id=actor.id,
        )

        for field, value in payload.model_dump(exclude={"tag_labels"}).items():
            setattr(project, field, value)
        project.tags = await self._resolve_tags(payload.tag_labels)

        try:
            await record_audit_event(
                self.repository.session,
                actor_id=actor.id,
                action="project.update",
                entity_type="project",
                entity_id=project.id,
                summary=f"Updated '{project.title_en}'",
            )
            await self.repository.session.commit()
        except IntegrityError as exc:
            await self.repository.session.rollback()
            raise AppError(
                "Could not save the project: check that referenced values are valid.",
                code="invalid_reference",
            ) from exc

        await self.repository.session.refresh(
            project, attribute_names=["tags", "skills", "updated_at"]
        )
        return _to_admin_out(project)

    async def _transition(
        self,
        project_id: int,
        actor: AdminUser,
        action: str,
        summary: str,
        apply: Callable[[Project], None],
    ) -> ProjectAdminOut:
        project = await self._get_or_404(project_id)
        apply(project)
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action=action,
            entity_type="project",
            entity_id=project.id,
            summary=summary,
        )
        await self.repository.session.commit()
        # `updated_at` has a DB-side `onupdate`, expired after any UPDATE
        # regardless of `expire_on_commit` — must be explicitly refreshed.
        await self.repository.session.refresh(
            project, attribute_names=["tags", "skills", "updated_at"]
        )
        return _to_admin_out(project)

    async def publish(self, project_id: int, actor: AdminUser) -> ProjectAdminOut:
        def apply(project: Project) -> None:
            project.publication_status = "PUBLISHED"
            project.publish_at = None
            project.unpublish_at = None
            if project.published_at is None:
                project.published_at = datetime.now(UTC)

        return await self._transition(project_id, actor, "project.publish", "Published", apply)

    async def schedule(
        self, project_id: int, publish_at: datetime, actor: AdminUser
    ) -> ProjectAdminOut:
        def apply(project: Project) -> None:
            project.publication_status = "SCHEDULED"
            project.publish_at = publish_at

        return await self._transition(
            project_id, actor, "project.schedule", f"Scheduled for {publish_at.isoformat()}", apply
        )

    async def unpublish(self, project_id: int, actor: AdminUser) -> ProjectAdminOut:
        def apply(project: Project) -> None:
            project.publication_status = "DRAFT"
            project.publish_at = None
            project.unpublish_at = None

        return await self._transition(project_id, actor, "project.unpublish", "Unpublished", apply)

    async def archive(self, project_id: int, actor: AdminUser) -> ProjectAdminOut:
        def apply(project: Project) -> None:
            project.publication_status = "ARCHIVED"

        return await self._transition(project_id, actor, "project.archive", "Archived", apply)

    async def soft_delete(self, project_id: int, actor: AdminUser) -> ProjectAdminOut:
        def apply(project: Project) -> None:
            project.deleted_at = datetime.now(UTC)

        return await self._transition(project_id, actor, "project.trash", "Moved to trash", apply)

    async def restore_from_trash(self, project_id: int, actor: AdminUser) -> ProjectAdminOut:
        def apply(project: Project) -> None:
            project.deleted_at = None

        return await self._transition(
            project_id, actor, "project.restore_from_trash", "Restored from trash", apply
        )

    async def permanent_delete(self, project_id: int, actor: AdminUser) -> None:
        project = await self._get_or_404(project_id)
        if project.deleted_at is None:
            raise AppError(
                "Move the project to trash before deleting it permanently.", code="not_trashed"
            )
        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="project.delete_permanently",
            entity_type="project",
            entity_id=project.id,
            summary=f"Permanently deleted '{project.title_en}'",
        )
        await self.repository.delete(project)
        await self.repository.session.commit()

    async def list_revisions(self, project_id: int) -> list[ProjectRevisionOut]:
        await self._get_or_404(project_id)
        revisions = await self.revision_repository.list_for_entity("project", project_id)
        return [
            ProjectRevisionOut(
                id=revision.id,
                schema_version=revision.schema_version,
                snapshot=revision.snapshot,
                created_at=revision.created_at,
                created_by_email=revision.created_by.email if revision.created_by else None,
            )
            for revision in revisions
        ]

    async def _get_revision_or_404(self, project_id: int, revision_id: int) -> Revision:
        revision = await self.revision_repository.get(revision_id)
        if (
            revision is None
            or revision.entity_type != "project"
            or revision.entity_id != project_id
        ):
            raise NotFoundError("Revision not found.")
        return revision

    async def restore_revision(
        self, project_id: int, revision_id: int, actor: AdminUser
    ) -> ProjectAdminOut:
        project = await self._get_or_404(project_id)
        revision = await self._get_revision_or_404(project_id, revision_id)

        applied, ignored = merge_revision_snapshot(revision.snapshot, _UPDATE_FIELDS)
        current_values = {field: getattr(project, field) for field in _UPDATE_FIELDS}
        merged = {
            **current_values,
            **applied,
            "tag_labels": [tag.label for tag in project.tags],
        }
        validated = ProjectAdminUpdate(**merged)

        await create_revision(
            self.repository.session,
            entity=project,
            entity_type="project",
            entity_id=project.id,
            actor_id=actor.id,
        )
        for field, value in validated.model_dump(exclude={"tag_labels"}).items():
            setattr(project, field, value)

        await record_audit_event(
            self.repository.session,
            actor_id=actor.id,
            action="project.restore_revision",
            entity_type="project",
            entity_id=project.id,
            summary=f"Restored revision #{revision_id}",
            context={"ignored_fields": ignored} if ignored else None,
        )
        await self.repository.session.commit()
        await self.repository.session.refresh(
            project, attribute_names=["tags", "skills", "updated_at"]
        )
        return _to_admin_out(project)
