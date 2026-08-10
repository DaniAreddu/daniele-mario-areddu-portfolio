from __future__ import annotations

from fastapi import APIRouter

from app.api.deps import Locale
from app.schemas.journey import JourneyMilestoneOut
from app.seed.data import JOURNEY_MILESTONES

router = APIRouter()


@router.get("/journey", response_model=list[JourneyMilestoneOut])
async def list_journey(locale: Locale) -> list[JourneyMilestoneOut]:
    return [
        JourneyMilestoneOut(
            year=item["year"],
            title=item[f"title_{locale}"] if item.get(f"title_{locale}") else item["title_en"],
            text=item[f"text_{locale}"] if item.get(f"text_{locale}") else item["text_en"],
            kind=item["kind"],
            event_slug=item.get("event_slug"),
        )
        for item in JOURNEY_MILESTONES
    ]
