"""System and metadata routes."""

from __future__ import annotations

from fastapi import APIRouter

from infrastructure.providers.factory import get_primary_llm

router = APIRouter(tags=["system"])


@router.get("/health")
async def health():
    return {"status": "ok", "service": "codagem-engine"}


@router.get("/agents")
async def list_agents():
    return {
        "agents": [
            {"name": "product_research", "role": "Analyze products, identify benefits, differentiators, positioning, competitors"},
            {"name": "audience_psychology", "role": "Define personas, emotional triggers, pain points, desires, objections"},
            {"name": "strategy", "role": "Campaign strategy, persuasion structure, emotional direction, storytelling"},
            {"name": "instagram_copywriter", "role": "Hooks, captions, CTA, storytelling, engagement optimization"},
            {"name": "carousel_structure", "role": "Slide-by-slide carousel design, retention, narrative flow"},
            {"name": "visual_prompt", "role": "Cinematic image prompts, visual direction, aesthetics"},
            {"name": "hashtag_seo", "role": "Hashtags, keyword strategy, discoverability optimization"},
            {"name": "compliance", "role": "Spam detection, claim review, policy compliance"},
            {"name": "quality_reviewer", "role": "Campaign quality scoring, weak section identification, revision triggers"},
        ],
        "tools": [
            {"name": "image_generation", "role": "Generate campaign images from visual prompts"},
        ],
    }


@router.get("/workflows")
async def list_workflows():
    return {
        "workflows": [
            {
                "name": "campaign_generation",
                "description": "Full Instagram campaign generation pipeline with reflection loops",
                "sequence": [
                    "product_research",
                    "audience_psychology",
                    "strategy",
                    "instagram_copywriter",
                    "carousel_structure",
                    "visual_prompt",
                    "image_generation",
                    "hashtag_seo",
                    "compliance",
                    "quality_reviewer",
                ],
                "features": ["reflection_loops", "quality_gating", "automatic_revision"],
            }
        ]
    }
