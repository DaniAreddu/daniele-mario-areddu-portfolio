from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel

from app.schemas.common import ORMModel


class ProfileAdminWrite(BaseModel):
    full_name: str
    roles: list[str] = []
    location: str = ""
    base_country: str = ""
    availability_en: str = ""
    availability_it: str = ""
    tagline_en: str = ""
    tagline_it: str = ""
    positioning_statement_en: str = ""
    positioning_statement_it: str = ""
    brand_label: str = ""
    public_email: str
    github_url: str | None = None
    linkedin_url: str | None = None
    sessionize_url: str | None = None
    talks_count_label: str = "30+"
    speaking_years_label: str = ""
    speaking_regions_label: str = ""


class ProfileAdminOut(ORMModel):
    id: int
    full_name: str
    roles: list[str]
    location: str
    base_country: str
    availability_en: str
    availability_it: str
    tagline_en: str
    tagline_it: str
    positioning_statement_en: str
    positioning_statement_it: str
    brand_label: str
    public_email: str
    github_url: str | None
    linkedin_url: str | None
    sessionize_url: str | None
    talks_count_label: str
    speaking_years_label: str
    speaking_regions_label: str
    created_at: datetime
    updated_at: datetime


class BiographyAdminWrite(BaseModel):
    micro_en: str = ""
    micro_it: str = ""
    short_en: str = ""
    short_it: str = ""
    medium_en: str = ""
    medium_it: str = ""
    long_en: str = ""
    long_it: str = ""
    speaker_bio_en: str = ""
    speaker_bio_it: str = ""


class BiographyAdminOut(ORMModel):
    id: int
    micro_en: str
    micro_it: str
    short_en: str
    short_it: str
    medium_en: str
    medium_it: str
    long_en: str
    long_it: str
    speaker_bio_en: str
    speaker_bio_it: str
    created_at: datetime
    updated_at: datetime
