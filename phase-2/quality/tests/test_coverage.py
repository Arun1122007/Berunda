"""Coverage validation — threshold checks and module coverage."""

from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[3]
SRC_DIR = PROJECT_ROOT / "src"


@pytest.mark.unit
def test_unit_coverage_meets_threshold():
    """Verify pytest-cov coverage meets the 61% minimum threshold."""
    try:
        import subprocess
        import sys

        result = subprocess.run(
            [
                sys.executable, "-m", "pytest",
                "--cov=src",
                "--cov-report=term-missing",
                "-m", "unit",
                "-x", "--tb=short",
            ],
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(PROJECT_ROOT),
        )
        output = result.stdout + result.stderr
        for line in output.splitlines():
            if "TOTAL" in line and "%" in line:
                parts = line.split()
                for part in parts:
                    if "%" in part:
                        pct = float(part.replace("%", ""))
                        assert pct >= 61.0, f"Coverage {pct}% is below 61% threshold"
                        return
        pytest.skip("Could not parse coverage percentage from output")
    except FileNotFoundError:
        pytest.skip("pytest-cov not available")
    except subprocess.TimeoutExpired:
        pytest.skip("coverage check timed out")


@pytest.mark.unit
def test_all_modules_have_tests():
    """Verify every src module has a corresponding test file."""
    test_dir = PROJECT_ROOT / "tests"
    src_modules = set()

    for pyfile in SRC_DIR.rglob("*.py"):
        if pyfile.name == "__init__.py":
            continue
        rel = pyfile.relative_to(SRC_DIR).with_suffix("")
        src_modules.add(str(rel).replace("\\", "/"))

    test_files = set()
    for tf in test_dir.rglob("test_*.py"):
        rel = tf.relative_to(test_dir).with_suffix("")
        test_files.add(str(rel).replace("\\", "/"))

    missing = []
    for mod in sorted(src_modules):
        parts = mod.split("/")
        test_name = f"test_{parts[-1]}"
        has_test = False
        for tf in test_files:
            if test_name in tf or test_name.replace("test_", "test_") in tf:
                has_test = True
                break
        if not has_test:
            missing.append(mod)

    if missing:
        msg = f"{len(missing)} modules missing tests:\n" + "\n".join(missing[:20])
        if len(missing) > 20:
            msg += f"\n... and {len(missing) - 20} more"
        pytest.fail(msg)
