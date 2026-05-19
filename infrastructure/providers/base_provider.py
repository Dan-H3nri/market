"""Abstract base for all LLM providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class LLMResponse:
    content: str
    model: str
    provider: str
    usage: dict | None = None


class BaseLLMProvider(ABC):
    """Every provider must implement this interface."""

    name: str = "base"

    def __init__(self, model: str, url: str, api_key: str, **kwargs):
        self.model = model
        self.url = url.rstrip("/")
        self.api_key = api_key
        self.extra = kwargs

    @abstractmethod
    async def generate(self, prompt: str, system: str | None = None, **kwargs) -> LLMResponse:
        ...

    @abstractmethod
    async def generate_json(self, prompt: str, system: str | None = None, **kwargs) -> LLMResponse:
        ...

    async def health_check(self) -> bool:
        try:
            resp = await self.generate("ping", system="Reply with OK.")
            return bool(resp.content)
        except Exception:
            return False
