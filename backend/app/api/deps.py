from __future__ import annotations

from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import Settings, get_settings
from app.core.i18n import resolve_locale
from app.db.session import get_db_session
from app.repositories.community_repository import CommunityRepository
from app.repositories.contact_repository import ContactRepository
from app.repositories.education_repository import EducationRepository
from app.repositories.event_repository import EventRepository
from app.repositories.experience_repository import ExperienceRepository
from app.repositories.passion_repository import PassionRepository
from app.repositories.profile_repository import ProfileRepository
from app.repositories.project_repository import ProjectRepository
from app.repositories.skill_repository import SkillRepository
from app.repositories.talk_repository import TalkRepository
from app.services.community_service import CommunityService
from app.services.contact_service import ContactService
from app.services.education_service import EducationService
from app.services.event_service import EventService
from app.services.experience_service import ExperienceService
from app.services.passion_service import PassionService
from app.services.profile_service import ProfileService
from app.services.project_service import ProjectService
from app.services.skill_service import SkillService
from app.services.talk_service import TalkService

DbSession = Annotated[AsyncSession, Depends(get_db_session)]
Locale = Annotated[str, Depends(resolve_locale)]
SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_profile_service(session: DbSession) -> ProfileService:
    return ProfileService(ProfileRepository(session))


def get_education_service(session: DbSession) -> EducationService:
    return EducationService(EducationRepository(session))


def get_experience_service(session: DbSession) -> ExperienceService:
    return ExperienceService(ExperienceRepository(session))


def get_skill_service(session: DbSession) -> SkillService:
    return SkillService(SkillRepository(session))


def get_project_service(session: DbSession) -> ProjectService:
    return ProjectService(ProjectRepository(session))


def get_talk_service(session: DbSession) -> TalkService:
    return TalkService(TalkRepository(session))


def get_event_service(session: DbSession) -> EventService:
    return EventService(EventRepository(session))


def get_passion_service(session: DbSession) -> PassionService:
    return PassionService(PassionRepository(session))


def get_community_service(session: DbSession) -> CommunityService:
    return CommunityService(CommunityRepository(session))


def get_contact_service(session: DbSession, settings: SettingsDep) -> ContactService:
    return ContactService(ContactRepository(session), settings)
