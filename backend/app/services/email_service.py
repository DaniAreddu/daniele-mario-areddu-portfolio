"""Email delivery via SMTP (Mailpit locally, real SMTP in production)."""

from __future__ import annotations

from email.message import EmailMessage

import aiosmtplib

from app.core.config import Settings
from app.core.logging import get_logger
from app.models.contact import ContactSubmission

logger = get_logger(__name__)

REQUEST_TYPE_LABELS = {
    "speaking_invitation": "Speaking invitation",
    "workshop": "Workshop",
    "engineering_collaboration": "Engineering collaboration",
    "community_partnership": "Community partnership",
    "podcast_interview": "Podcast or interview",
    "other": "Other",
}


def _build_message(settings: Settings, submission: ContactSubmission) -> EmailMessage:
    message = EmailMessage()
    message["From"] = settings.smtp_sender
    message["To"] = settings.contact_recipient_email
    message["Reply-To"] = submission.email
    request_label = REQUEST_TYPE_LABELS.get(submission.request_type, submission.request_type)
    message["Subject"] = f"[Portfolio contact] {request_label} — {submission.name}"
    lines = [
        f"Name: {submission.name}",
        f"Email: {submission.email}",
        f"Organization: {submission.organization or '-'}",
        f"Request type: {request_label}",
        f"Event / project: {submission.event_or_project or '-'}",
        f"Indicative date: {submission.indicative_date or '-'}",
        "",
        "Message:",
        submission.message,
    ]
    message.set_content("\n".join(lines))
    return message


async def send_contact_email(settings: Settings, submission: ContactSubmission) -> bool:
    """Attempt SMTP delivery. Returns whether delivery actually succeeded."""
    message = _build_message(settings, submission)
    try:
        # An empty string (as opposed to unset/None) is treated the same as "no
        # credentials configured" — otherwise aiosmtplib attempts AUTH with an
        # empty username against servers like Mailpit that don't support it.
        await aiosmtplib.send(
            message,
            hostname=settings.smtp_host,
            port=settings.smtp_port,
            username=settings.smtp_user or None,
            password=settings.smtp_password or None,
            start_tls=settings.smtp_use_tls,
        )
        return True
    except Exception as exc:  # noqa: BLE001 - delivery failures must not crash the request
        logger.error("contact_email_delivery_failed", error=str(exc))
        return False
