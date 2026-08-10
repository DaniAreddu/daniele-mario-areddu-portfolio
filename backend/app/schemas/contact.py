from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

RequestType = Literal[
    "speaking_invitation",
    "workshop",
    "engineering_collaboration",
    "community_partnership",
    "podcast_interview",
    "other",
]


class ContactCreate(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    email: EmailStr
    organization: str | None = Field(default=None, max_length=200)
    request_type: RequestType
    event_or_project: str | None = Field(default=None, max_length=200)
    indicative_date: str | None = Field(default=None, max_length=80)
    message: str = Field(min_length=10, max_length=4000)
    consent_given: bool
    # Honeypot: hidden from real users via CSS. Any non-empty value is treated
    # as spam and silently accepted (see ContactService.submit) rather than
    # rejected, so bots cannot tell their submission was detected.
    website: str = Field(default="", max_length=200)

    @field_validator("consent_given")
    @classmethod
    def _must_consent(cls, value: bool) -> bool:
        if not value:
            raise ValueError("Privacy consent is required.")
        return value


class ContactResult(BaseModel):
    received: bool
    email_delivered: bool
