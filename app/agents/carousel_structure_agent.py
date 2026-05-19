"""CarouselStructureAgent — designs slide-by-slide carousel narratives."""

from __future__ import annotations

import json

from app.agents.base_agent import BaseAgent
from app.prompts.templates import CAROUSEL_SYSTEM, CAROUSEL_PROMPT


class CarouselStructureAgent(BaseAgent):
    name = "carousel_structure"
    role_description = "Creates slide-by-slide carousel structure for retention and conversion."

    def get_system_prompt(self) -> str:
        return CAROUSEL_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        return CAROUSEL_PROMPT.format(
            copywriting=json.dumps(state.get("copywriting", {}), ensure_ascii=False),
            strategy=json.dumps(state.get("strategy", {}), ensure_ascii=False),
            audience_profile=json.dumps(state.get("audience_profile", {}), ensure_ascii=False),
            product_name=state.get("product_name", ""),
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        # parsed may be a list of slides
        slides = parsed if isinstance(parsed, list) else parsed.get("slides", [parsed])
        return {"carousel_structure": slides, "current_agent": self.name}
