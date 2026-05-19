"""InstagramCopywriterAgent — generates hooks, captions, CTA, storytelling."""

from __future__ import annotations

import json

from app.agents.base_agent import BaseAgent
from app.prompts.templates import COPYWRITER_SYSTEM, COPYWRITER_PROMPT


class InstagramCopywriterAgent(BaseAgent):
    name = "instagram_copywriter"
    role_description = "Generates hooks, captions, CTA, storytelling, and engagement optimization."

    def get_system_prompt(self) -> str:
        return COPYWRITER_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        return COPYWRITER_PROMPT.format(
            product_data=json.dumps(state.get("product_data", {}), ensure_ascii=False),
            audience_profile=json.dumps(state.get("audience_profile", {}), ensure_ascii=False),
            strategy=json.dumps(state.get("strategy", {}), ensure_ascii=False),
            tone=state.get("tone", "persuasive"),
            product_name=state.get("product_name", ""),
            affiliate_link=state.get("affiliate_link", ""),
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        return {"copywriting": parsed, "current_agent": self.name}
