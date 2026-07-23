"""Tests for structured logging."""

from __future__ import annotations

import io
import json
import logging

from src.shared.logging import StructuredFormatter, get_logger


class TestStructuredFormatter:
    def test_formatter_produces_json(self):
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="test_logger",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        output = formatter.format(record)
        parsed = json.loads(output)
        assert parsed["level"] == "INFO"
        assert parsed["message"] == "Test message"
        assert parsed["logger"] == "test_logger"
        assert "timestamp" in parsed

    def test_formatter_includes_correlation_id(self):
        formatter = StructuredFormatter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname=__file__,
            lineno=10,
            msg="msg",
            args=(),
            exc_info=None,
        )
        record.correlation_id = "corr-123"
        output = formatter.format(record)
        parsed = json.loads(output)
        assert parsed["correlation_id"] == "corr-123"


class TestGetLogger:
    def test_get_logger_returns_logger_instance(self):
        logger = get_logger("test_logger_instance")
        assert isinstance(logger, logging.Logger)

    def test_get_logger_same_name_returns_same_instance(self):
        logger1 = get_logger("same_logger")
        logger2 = get_logger("same_logger")
        assert logger1 is logger2

    def test_get_logger_outputs_json(self):
        logger = get_logger("json_output_test")
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
        logger.info("JSON check")
        output = stream.getvalue()
        parsed = json.loads(output)
        assert parsed["message"] == "JSON check"

    def test_logger_handles_multiple_calls(self):
        logger = get_logger("multi_call_test")
        stream = io.StringIO()
        handler = logging.StreamHandler(stream)
        handler.setFormatter(StructuredFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        logger.debug("debug msg")
        logger.info("info msg")
        logger.warning("warn msg")
        lines = stream.getvalue().strip().split("\n")
        assert len([ln for ln in lines if ln]) == 3
