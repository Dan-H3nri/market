"""FastAPI routes for campaign generation."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from infrastructure.services.campaign_service import run_campaign, get_campaign
from app.models.schemas import CampaignRequest, CampaignOutput

router = APIRouter(prefix="/api/v1", tags=["campaigns"])


@router.post("/generate-campaign", response_model=dict)
async def generate_campaign(request: CampaignRequest):
    """Run the full agent workflow and return a campaign package."""
    try:
        result = await run_campaign(request.model_dump())
        return result
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@router.get("/campaigns/{campaign_id}")
async def fetch_campaign(campaign_id: str):
    result = await get_campaign(campaign_id)
    if not result:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return result
