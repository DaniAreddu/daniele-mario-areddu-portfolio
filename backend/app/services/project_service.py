from __future__ import annotations

from app.core.errors import NotFoundError
from app.models.project import Project
from app.repositories.project_repository import ProjectRepository
from app.schemas.project import ProjectDetailOut, ProjectListItemOut
from app.services.localization import pick


def _to_list_item(project: Project, locale: str) -> ProjectListItemOut:
    return ProjectListItemOut(
        slug=project.slug,
        title=pick(project, "title", locale),
        summary=pick(project, "summary", locale),
        technologies=project.technologies,
        is_featured=project.is_featured,
        external_url=project.external_url,
    )


def _to_detail(project: Project, locale: str) -> ProjectDetailOut:
    return ProjectDetailOut(
        slug=project.slug,
        title=pick(project, "title", locale),
        summary=pick(project, "summary", locale),
        problem=pick(project, "problem", locale),
        challenge=pick(project, "challenge", locale),
        approach=pick(project, "approach", locale),
        architecture=pick(project, "architecture", locale),
        key_decisions=pick(project, "key_decisions", locale),
        outcome=pick(project, "outcome", locale),
        lessons=pick(project, "lessons", locale),
        confidentiality_note=pick(project, "confidentiality_note", locale),
        technologies=project.technologies,
        related_skills=[skill.skill_name for skill in project.skills],
        external_url=project.external_url,
        is_featured=project.is_featured,
    )


class ProjectService:
    def __init__(self, repository: ProjectRepository) -> None:
        self.repository = repository

    async def list_all(self, locale: str) -> list[ProjectListItemOut]:
        projects = await self.repository.list_all()
        return [_to_list_item(project, locale) for project in projects]

    async def get_by_slug(self, slug: str, locale: str) -> ProjectDetailOut:
        project = await self.repository.get_by_slug(slug)
        if project is None:
            raise NotFoundError(f"Project '{slug}' was not found.")
        return _to_detail(project, locale)
