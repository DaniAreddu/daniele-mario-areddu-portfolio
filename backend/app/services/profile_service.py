from __future__ import annotations

from app.core.errors import NotFoundError
from app.repositories.profile_repository import ProfileRepository
from app.schemas.profile import BiographyOut, ProfileOut
from app.services.localization import pick


class ProfileService:
    def __init__(self, repository: ProfileRepository) -> None:
        self.repository = repository

    async def get_profile(self, locale: str) -> ProfileOut:
        profile = await self.repository.get_profile()
        if profile is None:
            raise NotFoundError("Profile is not configured yet.")
        return ProfileOut(
            full_name=profile.full_name,
            roles=profile.roles,
            location=profile.location,
            base_country=profile.base_country,
            availability=pick(profile, "availability", locale),
            tagline=pick(profile, "tagline", locale),
            positioning_statement=pick(profile, "positioning_statement", locale),
            brand_label=profile.brand_label,
            public_email=profile.public_email,
            github_url=profile.github_url,
            linkedin_url=profile.linkedin_url,
            sessionize_url=profile.sessionize_url,
            talks_count_label=profile.talks_count_label,
            speaking_years_label=profile.speaking_years_label,
            speaking_regions_label=profile.speaking_regions_label,
        )

    async def get_biography(self, locale: str) -> BiographyOut:
        biography = await self.repository.get_biography()
        if biography is None:
            raise NotFoundError("Biography is not configured yet.")
        return BiographyOut(
            micro=pick(biography, "micro", locale),
            short=pick(biography, "short", locale),
            medium=pick(biography, "medium", locale),
            long=pick(biography, "long", locale),
            speaker_bio=pick(biography, "speaker_bio", locale),
        )
