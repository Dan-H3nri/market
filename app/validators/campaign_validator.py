"""Input/state validators used across the engine."""

from __future__ import annotations

import re

from app.models.schemas import CampaignRequest


def validate_campaign_request(data: dict) -> CampaignRequest:
    return CampaignRequest(**data)


def sanitize_product_name(name: str) -> str:
    return re.sub(r"[<>\"'&]", "", name).strip()[:200]


def validate_affiliate_link(link: str) -> bool:
    return bool(re.match(r"^https?://", link))


def validate_quality_score(score: float) -> bool:
    return 0.0 <= score <= 10.0
