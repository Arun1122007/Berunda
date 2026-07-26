"""Validation — FIR schema checks, field constraints, and type coercion."""

from __future__ import annotations

from typing import Any


def validate_fir_record(record: dict[str, Any]) -> list[str]:
    """Validate a FIR record against the canonical schema.

    Args:
        record: FIR record dictionary.

    Returns:
        List of validation error messages (empty if valid).
    """
    errors: list[str] = []

    required_fields = ["fir_number", "district_code", "crime_type", "date_registered"]
    for field in required_fields:
        if field not in record or record[field] is None:
            errors.append(f"Missing required field: {field}")

    if record.get("fir_number") and (
        not isinstance(record["fir_number"], str) or len(record["fir_number"]) < 5
    ):
        errors.append("fir_number must be a string with at least 5 characters")

    return errors


def coerce_types(record: dict[str, Any]) -> dict[str, Any]:
    """Coerce field types in a record to match expected schema types.

    Args:
        record: FIR record dictionary.

    Returns:
        Record with coerced types.
    """
    coerced = dict(record)
    import contextlib

    numeric_fields = ["age", "year", "pin_code"]
    for field in numeric_fields:
        if field in coerced and coerced[field] is not None:
            with contextlib.suppress(ValueError, TypeError):
                coerced[field] = int(coerced[field])
    return coerced
