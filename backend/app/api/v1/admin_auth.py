from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request, Response

from app.api.deps import (
    CurrentAdminUser,
    SettingsDep,
    get_admin_auth_service,
    require_admin_spa_header,
)
from app.core.client_ip import get_client_ip
from app.core.errors import UnauthorizedError
from app.core.security import sha256_hex
from app.schemas.admin_auth import (
    AdminLoginRequest,
    AdminLoginResult,
    AdminPasswordConfirmRequest,
    AdminRecoveryCodesOut,
    AdminTotpConfirmRequest,
    AdminTotpEnrollOut,
    AdminTotpVerifyRequest,
    AdminUserOut,
)
from app.services.admin_auth_service import AdminAuthService, SessionResult

router = APIRouter(prefix="/admin/auth")

AuthService = Annotated[AdminAuthService, Depends(get_admin_auth_service)]
RequireSpaHeader = Annotated[None, Depends(require_admin_spa_header)]


def _wire_status(internal_status: str) -> str:
    """Translate the internal session status ("mfa_pending"/"active") to the
    public API vocabulary ("mfa_required"/"authenticated") — kept distinct so
    the wire contract doesn't silently change if the internal state machine
    grows more statuses later.
    """
    return "mfa_required" if internal_status == "mfa_pending" else "authenticated"


def _set_session_cookie(response: Response, result: SessionResult, settings: SettingsDep) -> None:
    max_age = (
        settings.admin_mfa_pending_ttl_minutes * 60
        if result.status == "mfa_pending"
        else settings.admin_session_ttl_hours * 3600
    )
    response.set_cookie(
        key=settings.admin_session_cookie_name,
        value=result.token,
        max_age=max_age,
        httponly=True,
        secure=settings.is_production,
        samesite="strict",
        path="/api/v1/admin",
    )


@router.post("/login", response_model=AdminLoginResult)
async def login(
    payload: AdminLoginRequest,
    request: Request,
    response: Response,
    service: AuthService,
    settings: SettingsDep,
    _spa: RequireSpaHeader,
) -> AdminLoginResult:
    ip_hash = sha256_hex(get_client_ip(request))
    result = await service.login(
        payload.email, payload.password, ip_hash, request.headers.get("user-agent")
    )
    _set_session_cookie(response, result, settings)
    return AdminLoginResult(status=_wire_status(result.status))


@router.post("/totp/verify", response_model=AdminLoginResult)
async def verify_totp(
    payload: AdminTotpVerifyRequest,
    request: Request,
    response: Response,
    service: AuthService,
    settings: SettingsDep,
    _spa: RequireSpaHeader,
) -> AdminLoginResult:
    pending_token = request.cookies.get(settings.admin_session_cookie_name)
    if not pending_token:
        raise UnauthorizedError("Your sign-in attempt has expired. Please log in again.")
    ip_hash = sha256_hex(get_client_ip(request))
    result = await service.verify_totp(
        pending_token, payload.code, ip_hash, request.headers.get("user-agent")
    )
    _set_session_cookie(response, result, settings)
    return AdminLoginResult(status=_wire_status(result.status))


@router.post("/logout", status_code=204, response_model=None)
async def logout(
    request: Request,
    response: Response,
    service: AuthService,
    settings: SettingsDep,
    _spa: RequireSpaHeader,
) -> None:
    token = request.cookies.get(settings.admin_session_cookie_name)
    if token:
        await service.logout(token)
    response.delete_cookie(settings.admin_session_cookie_name, path="/api/v1/admin")


@router.get("/me", response_model=AdminUserOut)
async def me(user: CurrentAdminUser) -> AdminUserOut:
    return AdminUserOut.model_validate(user)


@router.post("/totp/enroll", response_model=AdminTotpEnrollOut)
async def enroll_totp(
    user: CurrentAdminUser, service: AuthService, _spa: RequireSpaHeader
) -> AdminTotpEnrollOut:
    return await service.begin_totp_enrollment(user)


@router.post("/totp/confirm", response_model=AdminRecoveryCodesOut)
async def confirm_totp(
    payload: AdminTotpConfirmRequest,
    user: CurrentAdminUser,
    service: AuthService,
    _spa: RequireSpaHeader,
) -> AdminRecoveryCodesOut:
    codes = await service.confirm_totp_enrollment(user, payload.code)
    return AdminRecoveryCodesOut(codes=codes)


@router.post("/totp/disable", status_code=204, response_model=None)
async def disable_totp(
    payload: AdminPasswordConfirmRequest,
    user: CurrentAdminUser,
    service: AuthService,
    _spa: RequireSpaHeader,
) -> None:
    await service.disable_totp(user, payload.password)


@router.post("/totp/recovery/regenerate", response_model=AdminRecoveryCodesOut)
async def regenerate_recovery_codes(
    payload: AdminPasswordConfirmRequest,
    user: CurrentAdminUser,
    service: AuthService,
    _spa: RequireSpaHeader,
) -> AdminRecoveryCodesOut:
    codes = await service.regenerate_recovery_codes(user, payload.password)
    return AdminRecoveryCodesOut(codes=codes)
