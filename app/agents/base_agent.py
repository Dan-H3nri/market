"""Base agent class — all specialized agents inherit from this."""

from __future__ import annotations

import json
import re
import asyncio
from abc import ABC, abstractmethod

from infrastructure.config.settings import get_settings
from infrastructure.providers.factory import generate_json_with_fallback, generate_with_fallback
from infrastructure.logging.logger import get_logger

_THINK_RE = re.compile(r"<think>.*?</think>", re.DOTALL)


class BaseAgent(ABC):
    """Template for every agent in the engine."""

    name: str = "base"
    role_description: str = ""

    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger(self.name)
        self._retries = self.settings.max_agent_retries

    @abstractmethod
    def get_system_prompt(self) -> str:
        ...

    @abstractmethod
    def get_user_prompt(self, state: dict) -> str:
        ...

    async def run(self, state: dict) -> dict:
        """Execute the agent with retry logic."""
        self.logger.info(f"Agent [{self.name}] starting")
        last_err = None
        for attempt in range(1, self._retries + 1):
            try:
                user_prompt = self.get_user_prompt(state)
                self.logger.info(f"Agent [{self.name}] attempt {attempt}/{self._retries}")
                response = await generate_json_with_fallback(
                    prompt=user_prompt,
                    system=self.get_system_prompt(),
                )
                parsed = self._parse_response(response.content)
                result = self.process_output(parsed, state)
                self.logger.info(f"Agent [{self.name}] completed successfully")
                return result
            except Exception as exc:
                last_err = exc
                self.logger.warning(f"Agent [{self.name}] attempt {attempt} failed: {exc}")
                if attempt < self._retries:
                    await asyncio.sleep(1 * attempt)
        self.logger.error(f"Agent [{self.name}] all retries exhausted: {last_err}")
        return {self.name: {"error": str(last_err)}, "error": f"Agent {self.name} failed: {last_err}"}

    def _parse_response(self, raw: str) -> dict | list:
        text = raw.strip()
        text = _THINK_RE.sub("", text).strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:])
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        return json.loads(text)

    @abstractmethod
    def process_output(self, parsed: dict | list, state: dict) -> dict:
        ...
