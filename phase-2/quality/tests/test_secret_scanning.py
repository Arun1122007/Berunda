"""Secret scanning tests — verify no secrets are hardcoded in codebase."""

from __future__ import annotations

import re
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"


def _get_python_files():
    return sorted(SRC_DIR.rglob("*.py"))


@pytest.mark.security
@pytest.mark.unit
def test_no_jwt_secrets_in_code():
    """Verify no JWT secrets are hardcoded beyond test/placeholder values."""
    pattern = re.compile(
        r"""JWT_SECRET\s*=\s*["'][^"']+["']"""
    )
    allowed = {
        "dev-secret-change-in-production",
        "replace-with-a-random-64-hex-char-string",
        "replace_this_with_a_secure_random_string_in_production",
        "test-secret",
        "test-secret-not-for-production",
    }
    issues = []
    for pyfile in _get_python_files():
        text = pyfile.read_text(encoding="utf-8", errors="ignore")
        for match in pattern.finditer(text):
            line = text[: match.start()].count("\n") + 1
            val = match.group(0).split("=", 1)[1].strip().strip('"').strip("'")
            if val not in allowed:
                issues.append(f"{pyfile.relative_to(PROJECT_ROOT)}:{line}")
    assert not issues, "Hardcoded JWT secrets found:\n" + "\n".join(issues)


@pytest.mark.security
@pytest.mark.unit
def test_no_password_in_logs():
    """Verify passwords are never included in log statements."""
    pattern = re.compile(
        r"""logger\.(info|debug|warning|error|critical)\([^)]*password""",
        re.IGNORECASE,
    )
    issues = []
    for pyfile in _get_python_files():
        text = pyfile.read_text(encoding="utf-8", errors="ignore")
        for i, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                issues.append(f"{pyfile.relative_to(PROJECT_ROOT)}:{i}")
    assert not issues, "Passwords found in log statements:\n" + "\n".join(issues)


@pytest.mark.security
@pytest.mark.unit
def test_no_api_keys_in_source():
    """Verify no API keys are hardcoded in source code."""
    pattern = re.compile(
        r"""(?i)(api_key|apikey|api_secret|api\.key)\s*[=:]\s*['\"][A-Za-z0-9_\-]{16,}['\"]"""
    )
    allowed_files = {"config.py"}
    issues = []
    for pyfile in _get_python_files():
        if pyfile.name in allowed_files:
            continue
        text = pyfile.read_text(encoding="utf-8", errors="ignore")
        for i, line in enumerate(text.splitlines(), 1):
            if pattern.search(line):
                issues.append(f"{pyfile.relative_to(PROJECT_ROOT)}:{i}: {line.strip()[:80]}")
    assert not issues, "Potential API keys found:\n" + "\n".join(issues[:10])


@pytest.mark.security
@pytest.mark.unit
def test_env_example_has_no_real_secrets():
    """Verify .env.example contains only placeholder values, no real secrets."""
    env_example = PROJECT_ROOT / ".env.example"
    if not env_example.exists():
        pytest.skip(".env.example not found")
    text = env_example.read_text(encoding="utf-8")
    suspicious = []
    for i, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#") or not stripped or "=" not in stripped:
            continue
        key, _, val = stripped.partition("=")
        if val and val not in (
            "",
            "development", "test", "staging", "production",
            "INFO", "DEBUG", "WARNING", "ERROR",
            "0.0.0.0", "8000",
        ) and not val.startswith("replace") and not val.startswith("your_") and not val.startswith("http"):
            if key.strip().endswith(("_KEY", "_SECRET", "_PASSWORD", "_TOKEN")):
                if val != "":
                    suspicious.append(f"{i}: {key.strip()}={val[:30]}...")
    msg = "\n".join(suspicious) if suspicious else "No real secrets found in .env.example"
    assert not suspicious, f"Suspicious values in .env.example:\n{msg}"
