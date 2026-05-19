"""Structured logging with file output."""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from infrastructure.config.settings import get_settings


class _JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "ts": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "msg": record.getMessage(),
        }
        if record.exc_info and record.exc_info[1]:
            payload["exc"] = self.formatException(record.exc_info)
        return json.dumps(payload)


def _ensure_log_dir() -> Path:
    p = Path("outputs/logs")
    p.mkdir(parents=True, exist_ok=True)
    return p


def setup_logging() -> logging.Logger:
    level_name = get_settings().log_level.upper()
    level = getattr(logging, level_name, logging.INFO)

    logger = logging.getLogger("codagem")
    logger.setLevel(level)

    if not logger.handlers:
        # Console handler
        sh = logging.StreamHandler(sys.stdout)
        sh.setLevel(level)
        sh.setFormatter(_JsonFormatter())
        logger.addHandler(sh)

        # File handler — one per day
        log_dir = _ensure_log_dir()
        fh = logging.FileHandler(log_dir / f"engine_{datetime.now().strftime('%Y%m%d')}.log")
        fh.setLevel(level)
        fh.setFormatter(_JsonFormatter())
        logger.addHandler(fh)

    return logger


def get_logger(name: str | None = None) -> logging.Logger:
    child = "codagem"
    if name:
        child = f"codagem.{name}"
    return logging.getLogger(child)
