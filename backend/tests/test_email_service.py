from __future__ import annotations

from unittest.mock import AsyncMock, patch

from app.core.config import get_settings
from app.models.contact import ContactSubmission
from app.services.email_service import send_contact_email


async def test_empty_smtp_credentials_are_sent_as_none_not_empty_string():
    """Some deployments set SMTP_USER=/SMTP_PASSWORD= as empty strings rather
    than leaving them unset (e.g. via a Compose env_file). aiosmtplib treats a
    non-None username as "please authenticate", which breaks servers like
    Mailpit that don't support AUTH at all. Empty strings must be normalized
    to None before being passed through."""
    settings = get_settings().model_copy(update={"smtp_user": "", "smtp_password": ""})
    submission = ContactSubmission(
        name="Test",
        email="test@example.com",
        request_type="other",
        message="A test message long enough to pass validation.",
        consent_given=True,
    )

    with patch("app.services.email_service.aiosmtplib.send", new_callable=AsyncMock) as mock_send:
        delivered = await send_contact_email(settings, submission)

    assert delivered is True
    _, kwargs = mock_send.call_args
    assert kwargs["username"] is None
    assert kwargs["password"] is None
