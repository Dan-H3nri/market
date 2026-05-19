"""Provider factory — create LLM providers from config tier."""
from __future__ import annotations

from infrastructure.config.settings import get_settings
from infrastructure.providers.base_provider import BaseLLMProvider, LLMResponse
from infrastructure.providers.openai_compatible import OpenAICompatibleProvider

_REGISTRY: dict[str, type[BaseLLMProvider]] = {
    "openai_compatible": OpenAICompatibleProvider,
    # Extend with more providers as needed
}


def register_provider(name: str, cls: type[BaseLLMProvider]) -> None:
    _REGISTRY[name] = cls


def _make(model: str, url: str, api_key: str, provider_type: str = "openai_compatible", **kw) -> BaseLLMProvider:
    cls = _REGISTRY.get(provider_type, OpenAICompatibleProvider)
    return cls(model=model, url=url, api_key=api_key, **kw)


def get_primary_llm() -> BaseLLMProvider:
    s = get_settings()
    return _make(s.primary_model, s.primary_model_url, s.primary_api_key)


def get_secondary_llm() -> BaseLLMProvider:
    s = get_settings()
    return _make(s.secondary_model, s.secondary_model_url, s.secondary_api_key)


def get_fallback_llm() -> BaseLLMProvider:
    s = get_settings()
    return _make(s.fallback_model, s.fallback_model_url, s.fallback_api_key)


async def generate_with_fallback(prompt: str, system: str | None = None, **kwargs) -> LLMResponse:
    """Try primary → secondary → fallback."""
    providers = [get_primary_llm, get_secondary_llm, get_fallback_llm]
    last_err: Exception | None = None
    for fn in providers:
        try:
            return await fn().generate(prompt, system=system, **kwargs)
        except Exception as exc:
            last_err = exc
            continue
    raise RuntimeError(f"All LLM providers failed. Last error: {last_err}")


async def generate_json_with_fallback(prompt: str, system: str | None = None, **kwargs) -> LLMResponse:
    providers = [get_primary_llm, get_secondary_llm, get_fallback_llm]
    last_err: Exception | None = None
    for fn in providers:
        try:
            return await fn().generate_json(prompt, system=system, **kwargs)
        except Exception as exc:
            last_err = exc
            continue
    raise RuntimeError(f"All LLM providers failed. Last error: {last_err}")
