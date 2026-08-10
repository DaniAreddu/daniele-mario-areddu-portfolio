from __future__ import annotations

from pydantic import BaseModel, EmailStr, Field

from app.schemas.common import ORMModel


class AdminLoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=200)


class AdminLoginResult(BaseModel):
    status: str  # "mfa_required" | "authenticated"


class AdminTotpVerifyRequest(BaseModel):
    # Accepts either a 6-digit TOTP code or a formatted recovery code
    # ("XXXX-XXXX-XXXX"), so the length bound must cover both.
    code: str = Field(min_length=6, max_length=32)


class AdminUserOut(ORMModel):
    id: int
    email: str
    role: str
    totp_enabled: bool


class AdminTotpEnrollOut(BaseModel):
    secret: str
    otpauth_uri: str
    qr_data_uri: str


class AdminTotpConfirmRequest(BaseModel):
    code: str = Field(min_length=6, max_length=6)


class AdminRecoveryCodesOut(BaseModel):
    codes: list[str]


class AdminPasswordConfirmRequest(BaseModel):
    password: str = Field(min_length=1, max_length=200)
