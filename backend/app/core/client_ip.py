"""Real client IP resolution behind the Nginx gateway.

The gateway is the only way to reach this API in both development and
production (see docker-compose.yml / docker-compose.prod.yml and
nginx/gateway.conf, which sets X-Forwarded-For via proxy-common.conf). Without
this, `request.client.host` would always be the gateway container's own
address for every request, collapsing every visitor into a single IP for
rate-limiting purposes — silently defeating per-visitor abuse protection.
"""

from __future__ import annotations

from fastapi import Request


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("x-forwarded-for")
    if forwarded_for:
        # The gateway is the sole trusted proxy; its first hop value is the
        # real client. Any further entries would be attacker-supplied.
        return forwarded_for.split(",")[0].strip()
    return request.client.host if request.client else "unknown"
