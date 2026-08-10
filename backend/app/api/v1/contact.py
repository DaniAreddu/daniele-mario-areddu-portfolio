from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Request

from app.api.deps import get_contact_service
from app.core.client_ip import get_client_ip
from app.schemas.contact import ContactCreate, ContactResult
from app.services.contact_service import ContactService

router = APIRouter()


@router.post("/contact", response_model=ContactResult, status_code=201)
async def submit_contact(
    payload: ContactCreate,
    request: Request,
    service: Annotated[ContactService, Depends(get_contact_service)],
) -> ContactResult:
    return await service.submit(payload, get_client_ip(request))
