"""ComplianceAgent — reviews campaigns for spam, unrealistic claims, policy violations."""

from __future__ import annotations

import json

from app.agents.base_agent import BaseAgent
from app.prompts.templates import COMPLIANCE_SYSTEM, COMPLIANCE_PROMPT


class ComplianceAgent(BaseAgent):
    name = "compliance"
    role_description = "Reviews campaigns for spam patterns, unrealistic claims, and platform policy compliance."

    def get_system_prompt(self) -> str:
        return COMPLIANCE_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        copy = state.get("copywriting", {})
        captions = copy.get("caption", "") if isinstance(copy, dict) else ""
        cta = copy.get("cta", "") if isinstance(copy, dict) else ""
        hashtags_data = state.get("hashtags", {})
        hash_str = ""
        if isinstance(hashtags_data, dict):
            all_tags = (
                hashtags_data.get("primary_hashtags", [])
                + hashtags_data.get("secondary_hashtags", [])
                + hashtags_data.get("niche_hashtags", [])
            )
            hash_str = " ".join(all_tags)
        return COMPLIANCE_PROMPT.format(
            caption=captions,
            hashtags=hash_str,
            cta=cta,
            product_name=state.get("product_name", ""),
            affiliate_link=state.get("affiliate_link", ""),
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        return {"compliance_notes": parsed, "current_agent": self.name}
