"""Structured logging — JSON-formatted logger with correlation IDs, levels, and PII-safe output."""

from __future__ import annotations

import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any


class CorrelationFilter(logging.Filter):
    """Inject correlation_id from the current request context into every log record."""

    def __init__(self) -> None:
        super().__init__()
        self._context: dict[str, str] = {}

    def set_correlation_id(self, cid: str) -> None:
        self._context["correlation_id"] = cid

    def filter(self, record: logging.LogRecord) -> bool:
        if "correlation_id" in self._context:
            record.correlation_id = self._context["correlation_id"]
        return True


_correlation_filter = CorrelationFilter()


def get_correlation_id() -> str | None:
    return _correlation_filter._context.get("correlation_id")


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


def _resolve_log_level() -> int:
    """Resolve log level from environment or default to INFO."""
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    env_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    return level_map.get(env_level, logging.INFO)


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
    handler.addFilter(_correlation_filter)
    logger.addHandler(handler)

    log_dir = os.environ.get("LOG_DIR", "")
    if log_dir:
        log_path = Path(log_dir) / "berunda.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = RotatingFileHandler(str(log_path), maxBytes=10_485_760, backupCount=5)
        file_handler.setFormatter(StructuredFormatter())
        file_handler.addFilter(_correlation_filter)
        logger.addHandler(file_handler)

    return logger


def get_correlation_filter() -> CorrelationFilter:
    return _correlation_filter
