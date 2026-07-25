from __future__ import annotations
import logging
import sys
from typing import Optional


class StructuredFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base = super().format(record)
        return f"[{record.levelname}] {record.name}: {base}"


def setup_logging(level: Optional[str] = None) -> None:
    log_level = (level or "INFO").upper()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(StructuredFormatter("%(asctime)s %(message)s"))
    logging.basicConfig(level=log_level, handlers=[handler], force=True)
