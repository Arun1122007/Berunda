# CI and Catalyst Deployment Report

> **Document ID:** BERUNDA-PH3-REPORT-08 | **Version:** 1.0 | **Status:** FINAL
> **Date:** 2026-07-26

---

## 1. CI Pipeline Configuration

### 1.1 Available Makefile Targets
A root `Makefile` provides standardized targets:

| Target | Description |
|---|---|
| `make test` | Run backend pytest suite |
| `make lint` | Run ruff check on src/ |
| `make lint-fix` | Auto-fix lint issues |
| `make typecheck` | Run mypy type checking |
| `make install` | Install Python dependencies |
| `make dev` | Start uvicorn dev server |
| `make build-web` | Build frontend production bundle |
| `make install-web` | Install npm dependencies |
| `make check` | Verify backend imports |
| `make all` | Run full CI pipeline (check → lint → test) |

### 1.2 GitHub Actions (Recommended)
The project is designed for GitHub Actions CI:

```yaml
# .github/workflows/ci.yml (recommended)
jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.13" }
      - run: pip install -r requirements.txt
      - run: make lint
      - run: make test

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "24" }
      - run: make install-web
      - run: make build-web
```

---

## 2. Zoho Catalyst Deployment

### 2.1 AppSail Container Configuration
The `appsail/berunda_api/` directory contains Catalyst-specific deployment:

- **`Dockerfile`** — Container build for Catalyst AppSail
- **`src/`** — Catalyst-compatible application code
- **`.catalystrc`** — Catalyst CLI configuration

### 2.2 Environment Variable Mapping
| Variable | Source | Purpose |
|---|---|---|
| `DATABASE_URL` | Catalyst Data Store | PostgreSQL connection |
| `JWT_SECRET` | `.env.production` | Token signing (must be 32+ chars) |
| `AI_PROVIDER` | `.env.production` | LLM backend (`catalyst` or `mock`) |
| `REDIS_URL` | Catalyst AppSail | Cache layer |

### 2.3 Deployment Steps
1. Install Catalyst CLI: `npm install -g zcatalyst-cli`
2. Authenticate: `catalyst login`
3. Deploy: `catalyst deploy --project berunda --environment production`
4. Verify: `curl https://berunda-xxxxxxxx.catalystapps.com/health`

---

## 3. Database Migration Strategy

### 3.1 Alembic Chain
```
001_initial_schema -> 002_seed_demo_data -> 003_add_constraints_and_indexes
-> 004_auth_tables -> 005_ai_tables -> 006_seed_users -> 007_phase3_p0_tables
```

### 3.2 Migration Verification
```bash
alembic -c src/alembic.ini history
```
Returns single linear chain from `<base>` to `edce56cd43ea` (head).

### 3.3 Catalyst Data Store
- ZCQL-compatible schema validated via `tests/database/test_catalyst_schema.py`
- All constraints and indexes verified via `003_add_constraints_and_indexes.py`
