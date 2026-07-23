"""Structured logging — JSON-formatted logger with correlation IDs, levels, and PII-safe output."""

from __future__ import annotations

import json
import logging
import sys
from typing import Any


class StructuredFormatter(logging.Formatter):
    """JSON formatter for structured log output."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        if hasattr(record, "correlation_id"):
            log_entry["correlation_id"] = record.correlation_id
        if record.exc_info and record.exc_info[0]:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, default=str)


def get_logger(name: str, level: str | None = None) -> logging.Logger:
    """Get a structured JSON logger instance.

    Args:
        name: Logger name (typically __name__).
        level: Log level override. Defaults to INFO.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(level or _resolve_log_level())

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter())
    logger.addHandler(handler)

    return logger


def _resolve_log_level() -> int:
    """Resolve log level from environment or default to INFO."""
    import os

    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    env_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    return level_map.get(env_level, logging.INFO)
