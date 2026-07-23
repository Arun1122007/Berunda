# Development Commands Reference

**Document ID:** BERUNDA-DEV-CMD-001 | **Version:** 1.0 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-20

---

## Unified Command Interface

The project supports multiple command interfaces. Choose the one most natural for your platform.

### Makefile (Cross-Platform)

| Command | Description |
|---|---|
| `make setup` | Install all dependencies (Python + Node.js) |
| `make dev` | Start both backend (FastAPI) and frontend (Vite) concurrently |
| `make build` | Build all applications |
| `make test` | Run all tests |
| `make test-unit` | Run unit tests only |
| `make test-integration` | Run integration tests only |
| `make lint` | Run all linters |
| `make lint-fix` | Auto-fix lint issues |
| `make typecheck` | Run type checkers |
| `make clean` | Remove build artifacts |
| `make docker-build` | Build Docker images |
| `make docker-up` | Start Docker Compose services |
| `make docker-down` | Stop Docker Compose services |
| `make docker-logs` | View Docker Compose logs |
| `make security-check` | Run security audit checks |

### PowerShell Script (berunda.ps1)

| Command | Description |
|---|---|
| `.\berunda.ps1 setup` | Install all dependencies |
| `.\berunda.ps1 build` | Build all applications |
| `.\berunda.ps1 test` | Run all tests |
| `.\berunda.ps1 lint` | Run linters and type checkers |
| `.\berunda.ps1 clean` | Remove build artifacts |
| `.\berunda.ps1 docker-build` | Build Docker images |
| `.\berunda.ps1 docker-up` | Start Docker Compose services |
| `.\berunda.ps1 docker-down` | Stop Docker Compose services |
| `.\berunda.ps1 help` | Show help message |

---

## Python Commands

| Command | Description |
|---|---|
| `pip install -r requirements.txt` | Install Python dependencies |
| `pip install -e .` | Install berunda package in dev mode |
| `pytest` | Run all Python tests |
| `pytest -m unit` | Run unit tests only |
| `pytest -m integration` | Run integration tests only |
| `pytest --cov=src --cov-report=term-missing` | Tests with coverage |
| `ruff check src/ apps/ tests/` | Lint Python files |
| `ruff format --check src/ apps/ tests/` | Check formatting |
| `ruff format src/ apps/ tests/` | Auto-format Python files |
| `mypy src/ --ignore-missing-imports` | Type check Python |
| `uvicorn src.main:app --reload --port 8000` | Start FastAPI dev server |
| `python -c "import berunda; print('OK')"` | Verify package import |

---

## Node.js / Frontend Commands

| Command | Description |
|---|---|
| `npm install` | Install root workspace dependencies |
| `npm run build` | Build all workspaces |
| `npm run test` | Run all workspace tests |
| `npm run lint` | Lint all workspaces |
| `npm run clean` | Clean all workspace artifacts |
| `cd apps/web && npm run dev` | Start Vite dev server |
| `cd apps/web && npm run build` | Build frontend for production |
| `cd apps/web && npm run test` | Run Vitest frontend tests |
| `cd apps/web && npm run lint` | Run ESLint |
| `cd apps/web && npm run typecheck` | Run TypeScript type check |
| `cd apps/web && npm run preview` | Preview production build |
| `cd apps/api && npm run deploy:*` | Deploy specific Catalyst function |

---

## Docker Commands

| Command | Description |
|---|---|
| `docker-compose build` | Build all Docker images |
| `docker-compose up -d` | Start all services in background |
| `docker-compose down` | Stop all services |
| `docker-compose logs -f` | Follow service logs |
| `docker-compose ps` | List running services |
| `docker-compose exec api sh` | Shell into API container |
| `docker-compose exec frontend sh` | Shell into frontend container |

---

## Security Commands

| Command | Description |
|---|---|
| `pip-audit --strict` | Audit Python dependencies for vulnerabilities |
| `npm audit --audit-level=high` | Audit Node.js dependencies |
| `trufflehog filesystem --directory .` | Scan for secrets |

---

## Git Commands

| Command | Description |
|---|---|
| `pre-commit run --all-files` | Run all pre-commit hooks |
| `pre-commit install` | Install pre-commit hooks |
| `git secrets --scan` | Scan for committed secrets |

---

## Quick Start Sequence

For a new developer:

```powershell
# 1. Prerequisites check
python --version
node --version
npm --version

# 2. Install everything
pip install -r requirements.txt
pip install -e .
npm install
cd apps/web && npm install && cd ../..

# 3. Start development
# Terminal 1:
uvicorn src.main:app --reload --port 8000

# Terminal 2:
cd apps/web && npm run dev

# 4. Verify
curl http://localhost:8000/health
curl http://localhost:8000/ready

# 5. Run tests
pytest -v -m unit
cd apps/web && npm test
```
