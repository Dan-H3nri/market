"""QualityReviewerAgent — scores campaign quality and triggers revision loops."""

from __future__ import annotations

import json

from app.agents.base_agent import BaseAgent
from app.prompts.templates import QUALITY_REVIEW_SYSTEM, QUALITY_REVIEW_PROMPT
from infrastructure.config.settings import get_settings


class QualityReviewerAgent(BaseAgent):
    name = "quality_reviewer"
    role_description = "Reviews all generated content, scores quality, identifies weak sections, triggers revision loops."

    def get_system_prompt(self) -> str:
        return QUALITY_REVIEW_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        threshold = get_settings().quality_threshold
        return QUALITY_REVIEW_PROMPT.format(
            product_data=json.dumps(state.get("product_data", {}), ensure_ascii=False),
            audience_profile=json.dumps(state.get("audience_profile", {}), ensure_ascii=False),
            strategy=json.dumps(state.get("strategy", {}), ensure_ascii=False),
            copywriting=json.dumps(state.get("copywriting", {}), ensure_ascii=False),
            carousel_structure=json.dumps(state.get("carousel_structure", []), ensure_ascii=False),
            visual_prompt_data=json.dumps(state.get("visual_prompt_data", {}), ensure_ascii=False),
            hashtags=json.dumps(state.get("hashtags", {}), ensure_ascii=False),
            compliance_notes=json.dumps(state.get("compliance_notes", {}), ensure_ascii=False),
            tone=state.get("tone", "persuasive"),
            revision_history=json.dumps(state.get("revision_history", []), ensure_ascii=False),
            quality_threshold=threshold,
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        threshold = get_settings().quality_threshold
        score = float(parsed.get("score", 0.0))
        passed = score >= threshold
        parsed["passed"] = passed

        result = {
            "quality_review": parsed,
            "quality_score": score,
            "needs_revision": not passed,
            "current_agent": self.name,
        }

        if not passed and parsed.get("weak_sections"):
            result["revision_target"] = parsed["weak_sections"][0]
        return result
