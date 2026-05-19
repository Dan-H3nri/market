"""Markdown-based persistent memory compatible with Obsidian."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from infrastructure.config.settings import get_settings
from infrastructure.logging.logger import get_logger


class MemoryManager:
    """File-based markdown memory for campaign learnings."""

    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger("memory")
        self.base_path = Path(self.settings.obsidian_memory_path)

    def _ensure_dir(self, subfolder: str) -> Path:
        d = self.base_path / subfolder
        d.mkdir(parents=True, exist_ok=True)
        return d

    def _write_note(self, folder: str, title: str, content: str, tags: list[str] | None = None) -> str:
        d = self._ensure_dir(folder)
        ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        slug = title.lower().replace(" ", "-")[:60]
        filename = f"{ts}_{slug}.md"
        path = d / filename

        tag_str = " ".join(f"#{t}" for t in (tags or []))
        note = f"""---
title: {title}
date: {datetime.now(timezone.utc).isoformat()}
tags: {tag_str}
---

{content}
"""
        path.write_text(note, encoding="utf-8")
        self.logger.info(f"Memory note saved: {path}")
        return str(path)

    def save_successful_pattern(self, campaign_id: str, pattern: str, details: str) -> str:
        return self._write_note(
            "successful_patterns",
            f"Success {campaign_id}",
            f"## Pattern\n{pattern}\n\n## Details\n{details}",
            tags=["success", campaign_id],
        )

    def save_failure(self, campaign_id: str, failure_type: str, details: str) -> str:
        return self._write_note(
            "failures",
            f"Failure {campaign_id} {failure_type}",
            f"## Failure Type\n{failure_type}\n\n## Details\n{details}",
            tags=["failure", failure_type, campaign_id],
        )

    def save_review(self, campaign_id: str, score: float, notes: list[str]) -> str:
        return self._write_note(
            "reviews",
            f"Review {campaign_id} score-{score}",
            f"## Score\n{score}/10\n\n## Notes\n" + "\n".join(f"- {n}" for n in notes),
            tags=["review", campaign_id],
        )

    def save_hook(self, campaign_id: str, hooks: list[str]) -> str:
        return self._write_note(
            "hooks",
            f"Hooks {campaign_id}",
            "\n".join(f"- {h}" for h in hooks),
            tags=["hook", campaign_id],
        )

    def save_niche_knowledge(self, niche: str, knowledge: str) -> str:
        return self._write_note(
            "niches",
            f"Niche {niche}",
            knowledge,
            tags=["niche", niche],
        )

    def save_prompt_learnings(self, agent_name: str, learning: str) -> str:
        return self._write_note(
            "prompts",
            f"Prompt {agent_name}",
            learning,
            tags=["prompt", agent_name],
        )
