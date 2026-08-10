from __future__ import annotations

from app.schemas.common import ORMModel


class ProfileOut(ORMModel):
    full_name: str
    roles: list[str]
    location: str
    base_country: str
    availability: str
    tagline: str
    positioning_statement: str
    brand_label: str
    public_email: str
    github_url: str | None
    linkedin_url: str | None
    sessionize_url: str | None
    talks_count_label: str
    speaking_years_label: str
    speaking_regions_label: str


class BiographyOut(ORMModel):
    micro: str
    short: str
    medium: str
    long: str
    speaker_bio: str
