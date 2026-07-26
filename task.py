from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.resolve()
VENV_PYTHON = (
    ROOT / "venv" / "Scripts" / "python.exe"
    if sys.platform == "win32"
    else ROOT / "venv" / "bin" / "python"
)


def _run(cmd: list[str], cwd: str | None = None) -> int:
    print(f"[task] {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=cwd or str(ROOT))


def cmd_test_backend() -> int:
    return _run([str(VENV_PYTHON), "-m", "pytest", "-v", "--tb=short", "tests/"])


def cmd_test_all() -> int:
    return _run([str(VENV_PYTHON), "-m", "pytest", "-v", "--tb=short", "--cov=src", "tests/"])


def cmd_lint() -> int:
    return _run([str(VENV_PYTHON), "-m", "ruff", "check", "src/"])


def cmd_typecheck() -> int:
    return _run([str(VENV_PYTHON), "-m", "mypy", "src/"])


def cmd_migrate_check() -> int:
    return _run(
        [str(VENV_PYTHON), "-m", "alembic", "check"],
        cwd=str(ROOT / "src"),
    )


def cmd_build_web() -> int:
    web_dir = ROOT / "apps" / "web"
    if not web_dir.is_dir():
        print("[task] apps/web not found — skipping frontend build")
        return 0
    return _run(["npm", "run", "build"], cwd=str(web_dir))


def cmd_verify_phase3() -> int:
    code = cmd_test_backend()
    if code != 0:
        return code
    code = cmd_lint()
    if code != 0:
        return code
    return cmd_migrate_check()


def cmd_check() -> int:
    print("[task] Environment check")
    py = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable
    print(f"  Python: {py}")
    code = _run([py, "-c", "import tenacity; print('  tenacity:', getattr(tenacity, '__version__', '>=9.0.0'))"])
    code |= _run([py, "-c", "import fastapi; print('  fastapi:', fastapi.__version__)"])
    code |= _run([py, "-c", "import sqlalchemy; print('  sqlalchemy:', sqlalchemy.__version__)"])
    return code


def main() -> int:
    targets = {
        "test": cmd_test_backend,
        "test-backend": cmd_test_backend,
        "test-all": cmd_test_all,
        "lint": cmd_lint,
        "typecheck": cmd_typecheck,
        "migrate-check": cmd_migrate_check,
        "build-web": cmd_build_web,
        "verify-phase3": cmd_verify_phase3,
        "check": cmd_check,
    }

    if len(sys.argv) < 2 or sys.argv[1] not in targets:
        print(f"Usage: python task.py <{'|'.join(targets)}>")
        print(f"Targets: {', '.join(sorted(targets))}")
        return 1

    return targets[sys.argv[1]]()


if __name__ == "__main__":
    sys.exit(main())
