from __future__ import annotations

from app.core.errors import NotFoundError
from app.repositories.community_repository import CommunityRepository
from app.schemas.community import CommunityActivityOut, CommunityProfileOut
from app.services.localization import pick


class CommunityService:
    def __init__(self, repository: CommunityRepository) -> None:
        self.repository = repository

    async def get_profile(self, locale: str) -> CommunityProfileOut:
        profile = await self.repository.get_profile()
        if profile is None:
            raise NotFoundError("Community profile is not configured yet.")
        activities = await self.repository.list_activities()
        return CommunityProfileOut(
            name=profile.name,
            role=pick(profile, "role", locale),
            mission=pick(profile, "mission", locale),
            description=pick(profile, "description", locale),
            vision=pick(profile, "vision", locale),
            collaboration=pick(profile, "collaboration", locale),
            founded_year=profile.founded_year,
            website_url=profile.website_url,
            activities=[
                CommunityActivityOut(
                    slug=activity.slug,
                    title=pick(activity, "title", locale),
                    description=pick(activity, "description", locale),
                    activity_date=activity.activity_date,
                    activity_type=activity.activity_type,
                    url=activity.url,
                )
                for activity in activities
            ],
        )
