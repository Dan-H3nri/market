"""Pydantic models for API I/O and internal validation."""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Optional


# ── Request models ─────────────────────────────────

class CampaignRequest(BaseModel):
    product_name: str = Field(..., min_length=1, max_length=200)
    affiliate_link: str = Field(..., min_length=1)
    niche: str = Field(..., min_length=1, max_length=100)
    audience: str = Field(..., min_length=1, max_length=200)
    objective: str = Field(default="conversions", max_length=100)
    tone: str = Field(default="persuasive", max_length=100)


# ── Response models ────────────────────────────────

class ProductData(BaseModel):
    name: str = ""
    niche: str = ""
    benefits: list[str] = Field(default_factory=list)
    differentiators: list[str] = Field(default_factory=list)
    positioning: str = ""
    use_cases: list[str] = Field(default_factory=list)
    competitors: list[str] = Field(default_factory=list)


class AudienceProfile(BaseModel):
    persona: str = ""
    emotional_triggers: list[str] = Field(default_factory=list)
    pain_points: list[str] = Field(default_factory=list)
    desires: list[str] = Field(default_factory=list)
    objections: list[str] = Field(default_factory=list)
    psychological_angles: list[str] = Field(default_factory=list)


class Strategy(BaseModel):
    campaign_strategy: str = ""
    persuasion_structure: str = ""
    emotional_direction: str = ""
    marketing_angle: str = ""
    storytelling_strategy: str = ""


class Copywriting(BaseModel):
    hooks: list[str] = Field(default_factory=list)
    caption: str = ""
    cta: str = ""
    storytelling: str = ""
    engagement_tips: list[str] = Field(default_factory=list)


class CarouselSlide(BaseModel):
    slide_number: int = 0
    type: str = ""
    headline: str = ""
    body: str = ""
    visual_direction: str = ""


class VisualPromptData(BaseModel):
    cinematic_prompt: str = ""
    visual_direction: str = ""
    aesthetic: str = ""
    optimization_notes: str = ""


class HashtagData(BaseModel):
    primary_hashtags: list[str] = Field(default_factory=list)
    secondary_hashtags: list[str] = Field(default_factory=list)
    niche_hashtags: list[str] = Field(default_factory=list)
    keyword_strategy: str = ""
    seo_notes: str = ""


class ComplianceData(BaseModel):
    is_compliant: bool = True
    spam_flags: list[str] = Field(default_factory=list)
    claim_flags: list[str] = Field(default_factory=list)
    policy_notes: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class QualityReview(BaseModel):
    score: float = 0.0
    passed: bool = False
    review_notes: list[str] = Field(default_factory=list)
    weak_sections: list[str] = Field(default_factory=list)
    improvement_suggestions: list[str] = Field(default_factory=list)


class CampaignContent(BaseModel):
    headline: str = ""
    caption: str = ""
    cta: str = ""
    hashtags: list[str] = Field(default_factory=list)
    bio_suggestion: str = ""
    carousel_slides: list[CarouselSlide] = Field(default_factory=list)
    image_prompt: str = ""
    generated_image: str = ""


class CampaignMetadata(BaseModel):
    tone: str = ""
    strategy: str = ""
    persona: str = ""
    pain_points: list[str] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)


class CampaignQuality(BaseModel):
    score: float = 0.0
    review_notes: list[str] = Field(default_factory=list)


class CampaignOutput(BaseModel):
    campaign_id: str = ""
    platform: str = "instagram"
    product: dict = Field(default_factory=dict)
    content: CampaignContent = Field(default_factory=CampaignContent)
    metadata: CampaignMetadata = Field(default_factory=CampaignMetadata)
    quality: CampaignQuality = Field(default_factory=CampaignQuality)
