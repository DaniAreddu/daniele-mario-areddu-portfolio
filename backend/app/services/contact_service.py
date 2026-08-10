from __future__ import annotations

from datetime import timedelta

from app.core.config import Settings
from app.core.errors import RateLimitedError
from app.core.logging import get_logger
from app.core.security import sha256_hex
from app.models.contact import ContactSubmission
from app.repositories.contact_repository import ContactRepository
from app.schemas.contact import ContactCreate, ContactResult
from app.services.email_service import send_contact_email

logger = get_logger(__name__)


class ContactService:
    def __init__(self, repository: ContactRepository, settings: Settings) -> None:
        self.repository = repository
        self.settings = settings

    async def submit(self, payload: ContactCreate, client_ip: str) -> ContactResult:
        # Honeypot: bots that fill the hidden field are silently accepted
        # without ever being persisted or emailed, so they cannot tell they failed.
        if payload.website:
            logger.warning("contact_honeypot_triggered")
            return ContactResult(received=True, email_delivered=False)

        ip_hash = sha256_hex(client_ip)
        recent_count = await self.repository.count_recent_from_ip_hash(
            ip_hash, within=timedelta(hours=1)
        )
        if recent_count >= self.settings.contact_rate_limit_per_hour:
            raise RateLimitedError("Too many requests. Please try again later.")

        submission = ContactSubmission(
            name=payload.name,
            email=payload.email,
            organization=payload.organization,
            request_type=payload.request_type,
            event_or_project=payload.event_or_project,
            indicative_date=payload.indicative_date,
            message=payload.message,
            consent_given=payload.consent_given,
            source_ip_hash=ip_hash,
            email_delivered=False,
        )

        delivered = await send_contact_email(self.settings, submission)
        submission.email_delivered = delivered

        await self.repository.create(submission)

        logger.info(
            "contact_submission_received",
            request_type=submission.request_type,
            email_delivered=delivered,
        )

        return ContactResult(received=True, email_delivered=delivered)
