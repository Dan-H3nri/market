"""Central configuration — all values come from .env."""

from __future__ import annotations

import os
from pathlib import Path
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[2]


class _Env:
    """Namespace that reads env vars with optional defaults & type coercion."""

    def _get(self, key: str, default: str | None = None, *, required: bool = False) -> str:
        value = os.getenv(key, default)
        if required and value is None:
            raise EnvironmentError(f"Missing required env var: {key}")
        return value

    # ── Primary model ───────────────────────────────
    @property
    def primary_model(self) -> str:
        return self._get("PRIMARY_MODEL", "gpt-4o")

    @property
    def primary_model_url(self) -> str:
        return self._get("PRIMARY_MODEL_URL", "https://api.openai.com/v1")

    @property
    def primary_api_key(self) -> str:
        return self._get("PRIMARY_API_KEY", "")

    # ── Secondary model ─────────────────────────────
    @property
    def secondary_model(self) -> str:
        return self._get("SECONDARY_MODEL", "gpt-4o-mini")

    @property
    def secondary_model_url(self) -> str:
        return self._get("SECONDARY_MODEL_URL", "https://api.openai.com/v1")

    @property
    def secondary_api_key(self) -> str:
        return self._get("SECONDARY_API_KEY", "")

    # ── Fallback model ──────────────────────────────
    @property
    def fallback_model(self) -> str:
        return self._get("FALLBACK_MODEL", "gpt-3.5-turbo")

    @property
    def fallback_model_url(self) -> str:
        return self._get("FALLBACK_MODEL_URL", "https://api.openai.com/v1")

    @property
    def fallback_api_key(self) -> str:
        return self._get("FALLBACK_API_KEY", "")

    # ── Image generation ────────────────────────────
    @property
    def image_provider(self) -> str:
        return self._get("IMAGE_PROVIDER", "catgpt")

    @property
    def image_model(self) -> str:
        return self._get("IMAGE_MODEL", "dall-e")

    @property
    def image_api_url(self) -> str:
        return self._get("IMAGE_API_URL", "http://localhost:8000/v1")

    @property
    def image_api_key(self) -> str:
        return self._get("IMAGE_API_KEY", "")

    # ── LangGraph ───────────────────────────────────
    @property
    def max_review_loops(self) -> int:
        return int(self._get("MAX_REVIEW_LOOPS", "5"))

    @property
    def max_agent_retries(self) -> int:
        return int(self._get("MAX_AGENT_RETRIES", "3"))

    @property
    def quality_threshold(self) -> float:
        return float(self._get("QUALITY_THRESHOLD", "8.5"))

    # ── Database ────────────────────────────────────
    @property
    def database_url(self) -> str:
        return self._get("DATABASE_URL", "sqlite:///./app.db")

    # ── Memory ──────────────────────────────────────
    @property
    def obsidian_memory_path(self) -> str:
        return self._get("OBSIDIAN_MEMORY_PATH", "./memory")

    # ── Logging ─────────────────────────────────────
    @property
    def log_level(self) -> str:
        return self._get("LOG_LEVEL", "INFO")


@lru_cache(maxsize=1)
def get_settings() -> _Env:
    return _Env()
