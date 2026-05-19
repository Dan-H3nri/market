"""HashtagSEOAgent — generates optimized hashtags and keyword strategy."""

from __future__ import annotations

import json

from app.agents.base_agent import BaseAgent
from app.prompts.templates import HASHTAG_SYSTEM, HASHTAG_PROMPT


class HashtagSEOAgent(BaseAgent):
    name = "hashtag_seo"
    role_description = "Generates hashtags, keyword strategy, and optimizes social discoverability."

    def get_system_prompt(self) -> str:
        return HASHTAG_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        copy = state.get("copywriting", {})
        caption = copy.get("caption", "") if isinstance(copy, dict) else ""
        return HASHTAG_PROMPT.format(
            caption=caption,
            niche=state.get("niche", ""),
            product_name=state.get("product_name", ""),
            audience=state.get("audience", ""),
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        return {"hashtags": parsed, "current_agent": self.name}
