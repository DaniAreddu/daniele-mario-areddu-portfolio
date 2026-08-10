from __future__ import annotations

from unittest.mock import MagicMock

from app.core.client_ip import get_client_ip


def _request_with(headers: dict[str, str], client_host: str | None = "10.0.0.5") -> MagicMock:
    request = MagicMock()
    request.headers = headers
    request.client = MagicMock(host=client_host) if client_host else None
    return request


def test_prefers_x_forwarded_for_when_present():
    request = _request_with({"x-forwarded-for": "203.0.113.9, 10.0.0.1"})
    assert get_client_ip(request) == "203.0.113.9"


def test_falls_back_to_direct_peer_without_forwarded_header():
    request = _request_with({}, client_host="192.0.2.1")
    assert get_client_ip(request) == "192.0.2.1"


def test_falls_back_to_unknown_without_any_client_info():
    request = _request_with({}, client_host=None)
    assert get_client_ip(request) == "unknown"


def test_strips_whitespace_around_forwarded_ip():
    request = _request_with({"x-forwarded-for": "  203.0.113.9 , 10.0.0.1"})
    assert get_client_ip(request) == "203.0.113.9"
