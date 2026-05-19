"""AudiencePsychologyAgent — builds deep psychological audience profiles."""

from __future__ import annotations

import json

from app.agents.base_agent import BaseAgent
from app.prompts.templates import AUDIENCE_PSYCHOLOGY_SYSTEM, AUDIENCE_PSYCHOLOGY_PROMPT


class AudiencePsychologyAgent(BaseAgent):
    name = "audience_psychology"
    role_description = "Defines personas, emotional triggers, pain points, desires, objections, and psychological angles."

    def get_system_prompt(self) -> str:
        return AUDIENCE_PSYCHOLOGY_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        return AUDIENCE_PSYCHOLOGY_PROMPT.format(
            product_data=json.dumps(state.get("product_data", {}), ensure_ascii=False),
            audience=state.get("audience", ""),
            niche=state.get("niche", ""),
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        return {"audience_profile": parsed, "current_agent": self.name}
