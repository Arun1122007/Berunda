# Dependency and Environment Report

> **Document ID:** BERUNDA-REMEDIATION-006  
> **Defect:** P3V-OBS-002  
> **Status:** CLOSED  

---

## 1. Defect Description

No cross-platform task runner existed. Project relied on `make` (Linux-only) or ad-hoc commands.

## 2. Remediation

### `task.py` — Cross-Platform Task Runner

A Python-based task runner (`python task.py <target>`) supporting Windows and Linux natively.

| Target | Description |
|--------|-------------|
| `test-backend` | Run backend test suite (pytest -v) |
| `test-all` | Run tests with coverage |
| `lint` | Run ruff linter on `src/` |
| `typecheck` | Run mypy on `src/` |
| `migrate-check` | Run alembic check |
| `build-web` | Build frontend (if apps/web exists) |
| `verify-phase3` | Test + lint + migration check |
| `check` | Verify Python environment and installed packages |

### `requirements.txt` Verification

| Package | Version | Status |
|---------|---------|--------|
| `tenacity` | `>=9.0.0` | Already present |
| `fastapi` | `>=0.115.0` | Present |
| `httpx` | `>=0.27.0` | Present |
| `alembic` | `>=1.13.0` | Present |

## 3. Verification

```bash
python task.py check
# → Python: ...\venv\Scripts\python.exe
# → tenacity: 9.0.0
# → fastapi: 0.115.x
# → sqlalchemy: 2.0.x
```
