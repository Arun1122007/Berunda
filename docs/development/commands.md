# Development Commands Reference

**Document ID:** BERUNDA-DEV-CMD-001 | **Version:** 2.0 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-25

---

## Unified Command Interface

The project supports three command interfaces. Choose the one most natural for your platform.

### PowerShell Script (berunda.ps1) — Primary

| Command | Description |
|---|---|
| `.\berunda.ps1 setup` | Install all dependencies (pip, npm) |
| `.\berunda.ps1 build` | Build all applications |
| `.\berunda.ps1 test` | Run all tests |
| `.\berunda.ps1 lint` | Run linters (ruff, ESLint) |
| `.\berunda.ps1 format` | Auto-format code (ruff format + fix, eslint --fix) |
| `.\berunda.ps1 typecheck` | Run mypy and TypeScript type checks |
| `.\berunda.ps1 migrate` | Run database migrations (alembic upgrade head) |
| `.\berunda.ps1 seed` | Load demo/seed data |
| `.\berunda.ps1 reset` | Full reset: clean artifacts + db, ready for reinstall |
| `.\berunda.ps1 clean` | Remove build artifacts only |
| `.\berunda.ps1 docker-build` | Build Docker images |
| `.\berunda.ps1 docker-up` | Start Docker Compose services |
| `.\berunda.ps1 docker-down` | Stop Docker Compose services |
| `.\berunda.ps1 help` | Show help message |

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
| `make security-check` | Run security audit checks |
| `make docker-build` | Build Docker images |
| `make docker-up` | Start Docker Compose services |
| `make docker-down` | Stop Docker Compose services |
| `make docker-logs` | View Docker Compose logs |

### Dev Scripts (scripts/dev/*.ps1)

| Script | Purpose |
|---|---|
| `.\scripts\dev\setup.ps1` | Create .env, install all deps |
| `.\scripts\dev\dev.ps1` | Start backend + frontend dev servers |
| `.\scripts\dev\test.ps1` | Run specific test/lint/typecheck scopes |
| `.\scripts\dev\docker.ps1` | Docker Compose lifecycle management |
| `.\scripts\dev\db.ps1` | Database migrations, seeding, reset |

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
| `ruff check src/ scripts/ tests/` | Lint Python files |
| `ruff format --check src/ scripts/ tests/` | Check formatting |
| `ruff format src/ scripts/ tests/` | Auto-format Python files |
| `ruff check --fix src/ scripts/ tests/` | Auto-fix lint issues |
| `mypy src/ --ignore-missing-imports` | Type check Python |
| `uvicorn src.main:app --reload --port 8000` | Start FastAPI dev server |
| `alembic -c src/alembic.ini upgrade head` | Run DB migrations |
| `alembic -c src/alembic.ini downgrade -1` | Rollback one migration |
| `alembic -c src/alembic.ini history` | List migration history |
| `python -c "from src.main import app; print('OK')"` | Verify package import |

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

## Database Commands

| Command | Description |
|---|---|
| `alembic -c src/alembic.ini upgrade head` | Apply all pending migrations |
| `alembic -c src/alembic.ini downgrade -1` | Rollback last migration |
| `alembic -c src/alembic.ini revision --autogenerate -m "desc"` | Create new migration |
| `alembic -c src/alembic.ini current` | Show current migration |
| `alembic -c src/alembic.ini history` | Show migration history |
| `python -m scripts.data.seed_demo` | Load demo seed data |

## Runtime Versions

| File | Tool | Current |
|---|---|---|
| `.python-version` | pyenv | 3.11.9 |
| `.nvmrc` | nvm | 20 |
| `.node-version` | nodenv/fnm | 20.18.0 |
| `package.json` engines | npm | >=20.0.0 |
| `pyproject.toml` requires-python | pip | >=3.10 |

## Security Commands

| Command | Description |
|---|---|
| `pip-audit --strict` | Audit Python dependencies for vulnerabilities |
| `npm audit --audit-level=high` | Audit Node.js dependencies |
| `trufflehog filesystem --directory .` | Scan for secrets |
| `pre-commit run --all-files` | Run all pre-commit hooks |
| `pre-commit install` | Install pre-commit hooks |

## Quick Start Sequence

```powershell
# 1. Prerequisites check
python --version    # need >= 3.10
node --version      # need >= 20
npm --version

# 2. Install everything (one command)
.\berunda.ps1 setup

# 3. Create environment config
cp .env.example .env

# 4. Start development
# Terminal 1:
uvicorn src.main:app --reload --port 8000
# Terminal 2:
cd apps/web && npm run dev

# 5. Verify
curl http://localhost:8000/health
curl http://localhost:8000/ready

# 6. Run tests
pytest -m unit
cd apps/web && npm test
```
