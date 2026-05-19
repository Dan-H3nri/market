"""ProductResearchAgent — analyzes products for marketing potential."""

from __future__ import annotations

from app.agents.base_agent import BaseAgent
from app.prompts.templates import PRODUCT_RESEARCH_SYSTEM, PRODUCT_RESEARCH_PROMPT


class ProductResearchAgent(BaseAgent):
    name = "product_research"
    role_description = "Analyzes products, identifies benefits, differentiators, positioning, and competitors."

    def get_system_prompt(self) -> str:
        return PRODUCT_RESEARCH_SYSTEM

    def get_user_prompt(self, state: dict) -> str:
        return PRODUCT_RESEARCH_PROMPT.format(
            product_name=state.get("product_name", ""),
            niche=state.get("niche", ""),
            affiliate_link=state.get("affiliate_link", ""),
        )

    def process_output(self, parsed: dict | list, state: dict) -> dict:
        return {"product_data": parsed, "current_agent": self.name}
