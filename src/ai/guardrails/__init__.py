"""Guardrails — I/O filtering, content safety, PII masking, and constraint enforcement for AI."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


@dataclass
class GuardrailResult:
    passed: bool
    reason: str = ""
    severity: str = "info"  # info, warn, block


class InputGuardrail:
    """Blocks problematic inputs before they reach the LLM."""

    def __init__(self):
        # Sensitive data patterns (Indian context)
        self.pii_patterns = {
            "aadhaar": re.compile(r"\b\d{4}\s?\d{4}\s?\d{4}\b"),
            "phone": re.compile(r"\b(?:\+91|0)?[6-9]\d{9}\b"),
            "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
            "pan": re.compile(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"),
        }
        self.toxic_patterns = re.compile(
            r"(hate|kill|attack|discriminat|abuse|threat)", re.IGNORECASE
        )
        self.injection_patterns = re.compile(
            r"(ignore.*instructions|system.*prompt|forget.*rules|you are.*assistant)",
            re.IGNORECASE,
        )

    def check(self, text: str) -> GuardrailResult:
        # Check PII
        for name, pattern in self.pii_patterns.items():
            if pattern.search(text):
                return GuardrailResult(
                    passed=False,
                    reason=f"Input contains PII: {name}",
                    severity="block",
                )

        # Check toxicity
        if self.toxic_patterns.search(text):
            return GuardrailResult(
                passed=False,
                reason="Input contains toxic language",
                severity="block",
            )

        # Check injection
        if self.injection_patterns.search(text):
            return GuardrailResult(
                passed=False,
                reason="Potential prompt injection detected",
                severity="block",
            )

        return GuardrailResult(passed=True)


class OutputGuardrail:
    """Validates LLM outputs before returning to user."""

    def __init__(self):
        self.sensitive_terms = re.compile(
            r"\b(caste|religion|community|scheduled caste|scheduled tribe|obc|general category)\b",
            re.IGNORECASE,
        )

    def check(self, text: str, context: dict[str, Any] | None = None) -> GuardrailResult:
        # Check for unsubstantiated claims
        unsubstantiated = re.compile(
            r"\b(always|never|every|all|certainly|definitely)\b", re.IGNORECASE
        )
        if unsubstantiated.search(text) and not context:
            return GuardrailResult(
                passed=False,
                reason="Output contains absolute claims without supporting context",
                severity="warn",
            )

        # Check for sensitive demographic mentions
        if self.sensitive_terms.search(text):
            return GuardrailResult(
                passed=False,
                reason="Output contains sensitive demographic references",
                severity="warn",
            )

        return GuardrailResult(passed=True)


class GuardrailManager:
    """Manages input and output guardrails."""

    def __init__(self):
        self.input_guardrail = InputGuardrail()
        self.output_guardrail = OutputGuardrail()

    def check_input(self, text: str) -> GuardrailResult:
        return self.input_guardrail.check(text)

    def check_output(self, text: str, context: dict | None = None) -> GuardrailResult:
        return self.output_guardrail.check(text, context)
