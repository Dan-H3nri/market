"""VisualPromptAgent — generates cinematic prompts for AI image generation."""

from __future__ import annotations

import json

from app.agents.base_agent import BaseAgent
from app.prompts.templates import VISUAL_PROMPT_SYSTEM, VISUAL_PROMPT_PROMPT


class VisualPromptAgent(BaseAgent):
    name = "visual_prompt"
    role_description = "Generates cinematic image prompts, visual direction, and aesthetic guidelines."

    def get_system_prompt(self) -> str:
        return VISUAL_PROMPT_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        return VISUAL_PROMPT_PROMPT.format(
            carousel_structure=json.dumps(state.get("carousel_structure", []), ensure_ascii=False),
            strategy=json.dumps(state.get("strategy", {}), ensure_ascii=False),
            product_name=state.get("product_name", ""),
            niche=state.get("niche", ""),
            tone=state.get("tone", "persuasive"),
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        return {"visual_prompt_data": parsed, "current_agent": self.name}
