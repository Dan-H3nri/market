"""StrategyAgent — designs campaign persuasion architecture."""

from __future__ import annotations

import json

from app.agents.base_agent import BaseAgent
from app.prompts.templates import STRATEGY_SYSTEM, STRATEGY_PROMPT


class StrategyAgent(BaseAgent):
    name = "strategy"
    role_description = "Defines campaign strategy, persuasion structure, emotional direction, marketing angle, and storytelling."

    def get_system_prompt(self) -> str:
        return STRATEGY_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        return STRATEGY_PROMPT.format(
            product_data=json.dumps(state.get("product_data", {}), ensure_ascii=False),
            audience_profile=json.dumps(state.get("audience_profile", {}), ensure_ascii=False),
            objective=state.get("objective", "conversions"),
            tone=state.get("tone", "persuasive"),
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        return {"strategy": parsed, "current_agent": self.name}
