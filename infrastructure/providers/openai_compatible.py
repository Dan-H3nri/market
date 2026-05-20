"""OpenAI-compatible provider — works with OpenAI, local models, proxies."""

from __future__ import annotations

import json
import re
import httpx

from infrastructure.providers.base_provider import BaseLLMProvider, LLMResponse


def _strip_think_tags(text: str) -> str:
    """Remove <think>...</think> blocks that reasoning models may emit."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()


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

    @staticmethod
    def _parse_sse(text: str) -> dict:
        """Parse Server-Sent Events response into a unified dict.

        Some local proxies always stream, even when ``stream`` is False.
        This assembles all ``data:`` lines into a single OpenAI-compatible
        response object.
        """
        content_parts: list[str] = []
        model = ""
        usage = None
        role = ""

        for line in text.splitlines():
            line = line.strip()
            if not line or not line.startswith("data:"):
                continue
            payload = line[len("data:"):].strip()
            if payload == "[DONE]":
                break
            try:
                chunk = json.loads(payload)
            except json.JSONDecodeError:
                continue
            model = chunk.get("model", model) or model
            usage = chunk.get("usage") or usage
            for choice in chunk.get("choices", []):
                delta = choice.get("delta", {})
                if delta.get("role"):
                    role = delta["role"]
                if delta.get("content"):
                    content_parts.append(delta["content"])
                # Non-streaming response format
                msg = choice.get("message", {})
                if msg.get("content") and not content_parts:
                    content_parts.append(msg["content"])

        return {
            "choices": [{"message": {"role": role or "assistant", "content": "".join(content_parts)}}],
            "model": model,
            "usage": usage,
        }

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
            "stream": False,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            resp = await client.post(
                f"{self.url}/chat/completions",
                headers=self._headers(),
                json=payload,
            )
            resp.raise_for_status()
            content_type = resp.headers.get("content-type", "")

            if "text/event-stream" in content_type or resp.text.strip().startswith("data:"):
                data = self._parse_sse(resp.text)
            else:
                data = resp.json()

        message_content = data["choices"][0]["message"]["content"]
        usage = data.get("usage")
        return LLMResponse(
            content=message_content,
            model=data.get("model", self.model),
            provider=self.name,
            usage=usage,
        )

    async def generate_json(self, prompt: str, system: str | None = None, **kwargs) -> LLMResponse:
        json_system = (system or "") + "\nYou MUST respond with valid JSON only. No markdown, no commentary."
        resp = await self.generate(prompt, system=json_system, **kwargs)
        text = _strip_think_tags(resp.content)
        if text.startswith("```"):
            text = text.split("\n", 1)[1] if "\n" in text else text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()
        resp.content = text
        return resp
