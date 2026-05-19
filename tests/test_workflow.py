"""Smoke tests for the campaign engine."""

import json
import pytest

from app.models.schemas import CampaignRequest, CampaignOutput
from app.validators.campaign_validator import validate_campaign_request, validate_affiliate_link


def test_campaign_request_validation():
    data = {
        "product_name": "Test Product",
        "affiliate_link": "https://example.com",
        "niche": "Tech",
        "audience": "Professionals",
        "objective": "conversions",
        "tone": "persuasive",
    }
    req = validate_campaign_request(data)
    assert req.product_name == "Test Product"
    assert req.niche == "Tech"


def test_invalid_request_missing_field():
    with pytest.raises(Exception):
        validate_campaign_request({"product_name": ""})


def test_affiliate_link_validation():
    assert validate_affiliate_link("https://example.com") is True
    assert validate_affiliate_link("notaurl") is False


def test_campaign_output_schema():
    output = CampaignOutput()
    assert output.platform == "instagram"
    assert output.quality.score == 0.0
