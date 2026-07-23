"""General-purpose utility functions used across the Berunda codebase."""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone


def generate_id(prefix: str = "BRN") -> str:
    """Generate a unique Berunda entity ID.

    Args:
        prefix: Two-to-four character uppercase prefix.

    Returns:
        Unique ID string (e.g., BRN-a1b2c3d4).
    """
    return f"{prefix}-{uuid.uuid4().hex[:8]}"


def hash_value(value: str) -> str:
    """Create a SHA-256 hex digest of a string value.

    Used for consistent hashing of non-sensitive identifiers.

    Args:
        value: Input string.

    Returns:
        SHA-256 hex digest.
    """
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def utc_now() -> datetime:
    """Return the current UTC timestamp."""
    return datetime.now(timezone.utc)


def truncate(text: str, max_length: int = 100) -> str:
    """Truncate text to a maximum length, appending ellipsis if needed.

    Args:
        text: Input text.
        max_length: Maximum length before truncation.

    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
