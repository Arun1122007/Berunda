"""Dependency scanning — requirements parse validation, vulnerability check, pinning."""

from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]


@pytest.mark.unit
def test_requirements_parse():
    """Verify requirements.txt is a valid pip requirements file."""
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.exists():
        pytest.skip("requirements.txt not found")
    text = req_file.read_text(encoding="utf-8")
    lines = text.splitlines()
    issues = []
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if not stripped or ("=" not in stripped and ">" not in stripped and "<" not in stripped and "~=" not in stripped and "!=" not in stripped):
            if not stripped.startswith("-r") and not stripped.startswith("--"):
                issues.append(f"line {i}: no version specifier: {stripped}")
    assert not issues, "Requirements parse issues:\n" + "\n".join(issues)


@pytest.mark.unit
def test_no_vulnerable_versions():
    """Check for known vulnerable dependency versions (reference check)."""
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.exists():
        pytest.skip("requirements.txt not found")
    text = req_file.read_text(encoding="utf-8")

    KNOWN_VULNERABLE = {
        "urllib3": {"<1.26.18"},
        "requests": {"<2.31.0"},
        "cryptography": {"<39.0.1"},
        "jinja2": {"<3.1.3"},
        "werkzeug": {"<3.0.1"},
    }
    issues = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#") or not stripped:
            continue
        for pkg, bad_versions in KNOWN_VULNERABLE.items():
            if stripped.lower().startswith(pkg.lower()):
                for bad in bad_versions:
                    if bad in stripped or stripped.endswith(bad.replace("<", "==").replace(">", "==")):
                        issues.append(f"{stripped} matches known vulnerable version {bad}")
    assert not issues, "Potentially vulnerable dependencies:\n" + "\n".join(issues)


@pytest.mark.unit
def test_pinned_versions():
    """Verify production dependencies are pinned to specific versions."""
    req_file = PROJECT_ROOT / "requirements.txt"
    if not req_file.exists():
        pytest.skip("requirements.txt not found")
    text = req_file.read_text(encoding="utf-8")
    pinned = 0
    unpinned = 0
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("-"):
            continue
        if "==" in stripped:
            pinned += 1
        elif ">=" in stripped or ">" in stripped:
            unpinned += 1
    ratio = pinned / (pinned + unpinned) if (pinned + unpinned) > 0 else 0
    assert ratio >= 0.5, f"Only {pinned}/{pinned + unpinned} deps pinned ({ratio:.0%})"


@pytest.mark.unit
def test_requirements_lock_exists():
    """Verify a lockfile exists for reproducible builds."""
    lockfile = PROJECT_ROOT / "requirements.lock"
    assert lockfile.exists() or (PROJECT_ROOT / "Pipfile.lock").exists() or (PROJECT_ROOT / "poetry.lock").exists(), "No lockfile found (requirements.lock, Pipfile.lock, or poetry.lock)"
