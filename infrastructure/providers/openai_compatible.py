"""OpenAI-compatible provider — works with OpenAI, local models, proxies."""

from __future__ import annotations

import json
import httpx

from infrastructure.providers.base_provider import BaseLLMProvider, LLMResponse


class OpenAICompatibleProvider(BaseLLMProvider):
    """Provider for any OpenAI-compatible API endpoint."""

    name = "openai_compatible"

    def __init__(self, model: str, url: str, api_key: str, **kwargs):
        super().__init__(model, url, api_key, **kwargs)
        self.timeout = kwargs.get("timeout", 120.0)

    def _headers(self) -> dict:
        hdrs = {"Content-Type": "application/json"}
        if self.api_key:
            hdrs["Authorization"] = f"Bearer {self.api_key}"
        return hdrs

    async def generate(self, prompt: str, system: str | None = None, **kwargs) -> LLMResponse:
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": kwargs.get("model", self.model),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 4096),
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.url}/chat/completions",
                headers=self._headers(),
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()

        content = data["choices"][0]["message"]["content"]
        usage = data.get("usage")
        return LLMResponse(
            content=content,
            model=data.get("model", self.model),
            provider=self.name,
            usage=usage,
        )

    async def generate_json(self, prompt: str, system: str | None = None, **kwargs) -> LLMResponse:
        json_system = (system or "") + "\nYou MUST respond with valid JSON only. No markdown, no commentary."
        resp = await self.generate(prompt, system=json_system, **kwargs)
        # Strip markdown fences if the model wraps output
        text = resp.content.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
        resp.content = text
        return resp
