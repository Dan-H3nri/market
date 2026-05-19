"""Strongly-typed campaign state for LangGraph workflow."""

from __future__ import annotations

from typing import TypedDict, Optional


class CampaignState(TypedDict, total=False):
    # ── Input ─────────────────────────────────────
    product_name: str
    affiliate_link: str
    niche: str
    audience: str
    objective: str
    tone: str

    # ── Agent outputs ─────────────────────────────
    product_data: dict
    audience_profile: dict
    strategy: dict
    copywriting: dict
    carousel_structure: list
    visual_prompt_data: dict
    generated_image_path: str
    hashtags: dict
    compliance_notes: dict
    quality_review: dict

    # ── Workflow control ──────────────────────────
    revision_history: list
    current_agent: str
    review_loop_count: int
    quality_score: float
    needs_revision: bool
    revision_target: str
    error: str

    # ── Final output ──────────────────────────────
    final_output: dict
    campaign_id: str
