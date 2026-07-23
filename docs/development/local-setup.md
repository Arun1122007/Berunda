# Local Development Setup

**Document ID:** BERUNDA-DEV-SETUP-001 | **Version:** 1.0 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-20

---

## Prerequisites

| Tool | Minimum Version | Recommended | Verification |
|---|---|---|---|
| Python | 3.10 | 3.11+ | `python --version` |
| Node.js | 20.0.0 | 20 LTS | `node --version` |
| npm | 9.0.0 | 10+ | `npm --version` |
| Git | 2.30 | 2.40+ | `git --version` |
| PowerShell | 5.1 | 7+ (pwsh) | `$PSVersionTable.PSVersion` |
| Docker (optional) | 24.0 | 27+ | `docker --version` |

---

## Supported Versions

| Python | Status |
|--------|--------|
| 3.10 | Supported |
| 3.11 | CI default |
| 3.12 | Supported |
| 3.13 | ✅ Tested (3.13.5) |

| Node.js | Status |
|---------|--------|
| 20.x | Supported (CI default) |
| 22.x | Supported |
| 24.x | ✅ Tested (24.15.0) |

---

## Installation Steps

### 1. Clone the Repository

```powershell
git clone https://github.com/Arun1122007/Berunda.git
cd Berunda
```

### 2. Install Python Dependencies

```powershell
pip install -r requirements.txt
pip install -e .  # Install the berunda package in development mode
```

### 3. Install Node.js Dependencies

```powershell
npm install
cd apps/web && npm install && cd ../..
cd apps/api && npm install && cd ../..
cd apps/worker && npm install && cd ../..
```

Or use the unified script:

```powershell
.\berunda.ps1 setup
```

### 4. Configure Environment

```powershell
cp .env.example .env
```

Edit `.env` with your settings. For local development, most values can remain as defaults.

### 5. Verify Installation

```powershell
python -c "import berunda; print('Python package OK')"
pytest --version
node --version
```

---

## Environment Setup

### Required Environment Variables

See `docs/security/environment-variable-register.md` for the complete register.

For minimal local development (health endpoints only), no environment variables are required. The FastAPI server will start with safe defaults.

### Development Configuration

The configuration loader reads from `config/base.yaml` and merges with environment-specific overrides from `config/development.yaml`. Environment is selected via `APP_ENV` variable (default: `development`).

---

## Startup Steps

### Quick Start (Python Backend + Frontend)

```powershell
# Terminal 1: Start the Python FastAPI server
uvicorn src.main:app --reload --port 8000

# Terminal 2: Start the frontend dev server
cd apps/web
npm run dev
```

### Using Make

```powershell
make setup      # Install all dependencies
make dev        # Start both backend and frontend
```

### Using Docker

```powershell
docker-compose up -d
```

---

## Validation Steps

### Health Check

```powershell
# Backend health
curl http://localhost:8000/health
# Expected: {"status": "healthy", "version": "0.1.0"}

# Backend readiness
curl http://localhost:8000/ready
# Expected: {"status": "ready", "checks": {...}}

# Frontend
Open http://localhost:5173 in browser
```

### Run Tests

```powershell
# All tests
pytest

# Unit tests only
pytest -m unit

# With coverage
pytest --cov=src --cov-report=term-missing

# Frontend tests
cd apps/web && npm test
```

---

## Common Errors

| Error | Cause | Solution |
|---|---|---|
| `ModuleNotFoundError: No module named 'berunda'` | Package not installed | `pip install -e .` |
| `Port 8000 already in use` | Another process on port | `netstat -ano | findstr :8000` then kill or use `--port` |
| `Missing required environment variable` | `.env` not configured | Copy `.env.example` to `.env` |
| `npm ERR!` during install | Node version mismatch | Check `node --version` >= 20 |
| `pytest: command not found` | pytest not installed | `pip install pytest` or `pip install -r requirements.txt` |

---

## Reset Procedure

```powershell
# Clean all build artifacts
.\berunda.ps1 clean

# Or manually:
Remove-Item -Recurse -Force apps/web/dist, apps/api/dist -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force __pycache__ -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .pytest_cache, .mypy_cache, .ruff_cache -ErrorAction SilentlyContinue

# Clean node_modules (if needed)
Remove-Item -Recurse -Force node_modules -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force apps/web/node_modules -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force apps/api/node_modules -ErrorAction SilentlyContinue

# Reset database
Remove-Item -Force data/berunda_dev.db -ErrorAction SilentlyContinue

# Reinstall
.\berunda.ps1 setup
```

---

## Platform-Specific Notes

### Windows
- PowerShell 5.1 is the default shell; all scripts support it
- Use `.\berunda.ps1` prefix for PowerShell scripts (e.g., `.\berunda.ps1 setup`)
- Path separators: scripts auto-detect OS paths
- Line endings: `.gitattributes` handles CRLF/LF conversion
- Docker: Use Docker Desktop for Windows with WSL2 backend

### Linux/Mac
- Use `make` commands for development tasks
- `bash berunda.ps1` is available via PowerShell Core
- Line endings are LF by default
- Docker Engine or Docker Desktop available

### CI Environment (GitHub Actions)
- Ubuntu-latest runner
- Python 3.11, Node.js 20
- PostgreSQL 16 (integration tests)
- Redis 7 (integration tests)
- All environment variables set via GitHub Secrets
