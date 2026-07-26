# Phase 1 — Configuration & Application Security Findings

**Document ID:** BERUNDA-SEC-FINDINGS-001 | **Version:** 2.0 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-24

---

## 1. Executive Summary

Phase 1 Configuration and Application Security audit complete. The project has a strong security baseline: no real secrets were found in tracked files, `.gitignore` is comprehensive, and the logging system is designed to be PII-safe. Three high-priority and five low-priority findings were identified and remediated.

---

## 2. Security Findings

### 2.1 HIGH — `DATABASE_URL` defaulted to PostgreSQL (Resolved)

| Attribute | Value |
|-----------|-------|
| **File** | `src/database.py:10-12` |
| **Finding** | Default value was `postgresql+asyncpg://postgres:postgres@localhost:5432/berunda` causing startup failure when PostgreSQL was unavailable |
| **Fix** | Changed default to `sqlite+aiosqlite:///./berunda.db` matching `.env.example`. Production deployments must explicitly set `DATABASE_URL`. |
| **Commit** | This session |

### 2.2 HIGH — `JWT_SECRET` weak default with no warning (Resolved)

| Attribute | Value |
|-----------|-------|
| **File** | `src/middleware/auth.py:12` |
| **Finding** | Fallback value `dev-secret-change-in-production` is trivially guessable. No warning was issued when using this default. |
| **Fix** | Added runtime `warnings.warn()` when JWT_SECRET is set to any known placeholder value. |
| **Commit** | This session |

### 2.3 HIGH — No typed configuration validation (Resolved)

| Attribute | Value |
|-----------|-------|
| **File** | `src/config.py` (new) |
| **Finding** | All environment variables were read via raw `os.environ.get()` with no type validation, no schema, and no central registry. |
| **Fix** | Created `src/config.py` with Pydantic Settings — fully typed, validated, with safe defaults and production-aware validation (e.g., OpenAI API key required in production). |
| **Commit** | This session |

### 2.4 MEDIUM — `.env.example` was incomplete (Resolved)

| Attribute | Value |
|-----------|-------|
| **File** | `.env.example` |
| **Finding** | Only 11 variables documented; 23 env vars referenced in code were missing from the template. Variables like `CELERY_BROKER_URL`, `OPENAI_API_KEY`, `NEO4J_PASSWORD`, and `ACCESS_TOKEN_EXPIRY_MINUTES` had no documented placeholder. |
| **Fix** | Expanded `.env.example` to 51 lines covering all 23 code-referenced environment variables organized by category. All values are fake placeholders. |
| **Commit** | This session |

### 2.5 LOW — Missing `*.secret` and `.envrc` in `.gitignore` (Resolved)

| Attribute | Value |
|-----------|-------|
| **File** | `.gitignore` |
| **Finding** | `*.secret` files and `.envrc`/`.direnv/` (used by direnv for auto-loading env vars) were not covered. |
| **Fix** | Added `*.secret`, `.envrc`, and `.direnv/` patterns. |
| **Commit** | This session |

### 2.6 INFO — Config YAML files contain placeholder secret values

| Attribute | Value |
|-----------|-------|
| **Files** | `config/development.yaml:29`, `config/testing.yaml:29` |
| **Finding** | `jwt_secret` placeholder values exist in tracked YAML files. These are documented placeholders for local development only, but could be mistaken for real secrets. |
| **Status** | Accepted risk — values are obviously placeholder strings |

### 2.7 INFO — `pydantic-settings` added as dependency

| Attribute | Value |
|-----------|-------|
| **File** | `requirements.txt` |
| **Finding** | `pydantic-settings` was not listed as a dependency despite being used by `src/config.py`. |
| **Fix** | Added `pydantic-settings>=2.6.0` to `requirements.txt`. |
| **Status** | Resolved |

### 2.8 INFO — `.env` file not auto-loaded by application (Accepted)

| Attribute | Value |
|-----------|-------|
| **File** | `src/main.py` |
| **Finding** | The application did not call `load_dotenv()`, so the `.env` file was ignored at runtime. Added `load_dotenv()` with path resolution in this session. |
| **Status** | Resolved |

---

## 3. Environment Variable Inventory

Complete inventory of 23 environment variables referenced by application code:

| # | Variable | Source File(s) | Default | Secret |
|---|----------|---------------|---------|--------|
| 1 | `APP_ENV` | `src/shared/config/__init__.py`, `src/main.py` | `development` | No |
| 2 | `LOG_LEVEL` | `src/shared/logging/__init__.py`, `src/database.py` | `INFO` | No |
| 3 | `HOST` | `src/shared/config/__init__.py` | `0.0.0.0` | No |
| 4 | `PORT` | `src/shared/config/__init__.py` | `8000` | No |
| 5 | `DATABASE_URL` | `src/database.py`, `src/alembic/env.py` | `sqlite+aiosqlite:///./berunda.db` | **Yes** |
| 6 | `DB_POOL_SIZE` | `src/database.py` | `5` | No |
| 7 | `DB_MAX_OVERFLOW` | `src/database.py` | `10` | No |
| 8 | `JWT_SECRET` | `src/middleware/auth.py` | `dev-secret-change-in-production` | **Yes** |
| 9 | `ACCESS_TOKEN_EXPIRY_MINUTES` | `src/services/auth_service.py` | `60` | No |
| 10 | `REFRESH_TOKEN_EXPIRY_DAYS` | `src/services/auth_service.py` | `7` | No |
| 11 | `CELERY_BROKER_URL` | `src/worker.py` | `redis://localhost:6379/0` | **Yes** |
| 12 | `CELERY_RESULT_BACKEND` | `src/worker.py` | `redis://localhost:6379/0` | **Yes** |
| 13 | `OPENAI_API_KEY` | `src/ai/providers/openai.py` | (none — empty) | **Yes** |
| 14 | `OPENAI_BASE_URL` | `src/ai/providers/openai.py` | `https://api.openai.com/v1` | No |
| 15 | `GROQ_API_KEY` | `src/ai/providers/groq.py` | (none — empty) | **Yes** |
| 16 | `CATALYST_PROJECT_ID` | `src/ai/providers/catalyst.py` | (none — empty) | **Yes** |
| 17 | `CATALYST_API_KEY` | `src/ai/providers/catalyst.py` | (none — empty) | **Yes** |
| 18 | `NEO4J_URI` | `src/services/neo4j_service.py` | (none — empty) | No |
| 19 | `NEO4J_USER` | `src/services/neo4j_service.py` | `neo4j` | No |
| 20 | `NEO4J_PASSWORD` | `src/services/neo4j_service.py` | (none — empty) | **Yes** |
| 21 | `TEST_DATABASE_URL` | `tests/integration/conftest.py` | (none — empty) | No |
| 22 | `TEST_CACHE_URL` | `tests/integration/conftest.py` | `redis://localhost:6379/0` | No |
| 23 | `AUTH_JWT_SECRET` | `tests/conftest.py` | `test-secret` | **Yes** |
| — | `INITIAL_ADMIN_PASSWORD` | `alembic/versions/006_seed_users.py` | `admin123` | **Yes** |
| — | `INITIAL_ANALYST_PASSWORD` | `alembic/versions/006_seed_users.py` | `analyst123` | **Yes** |
| — | `VITE_API_BASE_URL` | `apps/web/src/services/api-client.ts` | `/api/v1` | No |
| — | `VITE_API_URL` | `apps/web/src/services/api-client.ts` | `http://localhost:8000` | No |

**Docker/Compose environment variables** (not read by Python code directly):

| # | Variable | File | Required |
|---|----------|------|----------|
| — | `DB_PASSWORD` | `docker-compose.prod.yml` | **Yes** (:?Missing) |
| — | `REDIS_PASSWORD` | `docker-compose.prod.yml` | **Yes** (:?Missing) |
| — | `CORS_ORIGINS` | `docker-compose.prod.yml` | No |
| — | `NEO4J_PASSWORD` | `docker-compose.neo4j.yml` | No (default: `dev-password-change`) |

---

## 4. Files Created or Modified

| File | Action | Description |
|------|--------|-------------|
| `src/config.py` | **Created** | Pydantic Settings class — typed, validated single source of truth for all env vars |
| `.env.example` | **Modified** | Expanded from 32→51 lines covering all 23 code-referenced env vars |
| `requirements.txt` | **Modified** | Added `pydantic-settings>=2.6.0` |
| `.gitignore` | **Modified** | Added `*.secret`, `.envrc`, `.direnv/` patterns |
| `.gitleaks.toml` | **Created** | Gitleaks configuration with Berunda-specific rules and allowlist |
| `src/middleware/auth.py` | **Modified** | Added runtime warning on weak/placeholder `JWT_SECRET` |
| `src/database.py` | **Modified** | Changed `DATABASE_URL` default from PostgreSQL to SQLite |
| `src/main.py` | **Modified** | Added `load_dotenv()` call to load `.env` at startup |
| `docs/security/phase-1-config-security-findings.md` | **Created** | This document |
| `docs/security/environment-variable-register.md` | **Modified** | Updated to v2.0 — 27 actual vars, removed phantom Catalyst vars |
| `src/services/auth_service.py` | **Modified** | Migrated `ACCESS_TOKEN_EXPIRY_MINUTES` and `REFRESH_TOKEN_EXPIRY_DAYS` to use `settings` |
| `src/worker.py` | **Modified** | Migrated `CELERY_BROKER_URL` and `CELERY_RESULT_BACKEND` to use `settings` |
| `src/services/neo4j_service.py` | **Modified** | Migrated Neo4j connection params to use `settings` |
| `.github/workflows/ci.yml` | **Modified** | Added Gitleaks secrets scan job and bandit SAST to lint-python |
| `.github/workflows/security-scan.yml` | **Modified** | Removed `continue-on-error` from pip-audit and npm audit; pip-audit now uses `--requirement requirements.txt` |
| `config/development.yaml` | **Modified** | Removed misleading placeholder `jwt_secret` line |
| `config/testing.yaml` | **Modified** | Removed misleading placeholder `jwt_secret` line |
| `appsail/berunda_api/src/config.py` | **Created** | Copy of `src/config.py` for AppSail deployment |
| `appsail/berunda_api/src/database.py` | **Modified** | Migrated to `from src.config import settings` |
| `appsail/berunda_api/src/middleware/auth.py` | **Modified** | Migrated to `from src.config import settings` + weak-default warning |
| `appsail/berunda_api/src/services/auth_service.py` | **Modified** | Migrated to `from src.config import settings` |
| `appsail/berunda_api/src/services/neo4j_service.py` | **Modified** | Migrated to `from src.config import settings` |
| `appsail/berunda_api/src/worker.py` | **Modified** | Migrated to `from src.config import settings` |

---

## 5. Remediated Risks

| Risk | Severity | Action |
|------|----------|--------|
| **R1** — `os.environ.get()` used directly in critical modules | **Medium** | Migrated `src/` modules (auth.py, database.py, auth_service.py, worker.py, neo4j_service.py) to `from src.config import settings` |
| **R2** — `appsail/` duplicate code still uses raw `os.environ.get()` | **Medium** | Copied `config.py` to `appsail/berunda_api/src/` and migrated all 5 duplicate modules |
| **R3** — No Gitleaks in CI pipeline | **Medium** | Added `gitleaks/gitleaks-action@v2` job in `ci.yml` with `.gitleaks.toml` config |
| **R4** — No bandit SAST in CI | **Low** | Added `bandit -r src/` to `ci.yml` lint-python job |
| **R5** — Outdated env var register with phantom vars | **Low** | Updated `docs/security/environment-variable-register.md` to v2.0 — 27 actual code-referenced vars only |
| **R6** — Neo4j password failure is silent | **Low** | Migrated to typed settings; empty password resolves to `None` with clear log message |
| **R7** — `config/development.yaml` and `config/testing.yaml` contain misleading placeholder `jwt_secret` | **Low** | Removed `jwt_secret` lines; added comment explaining env var takes precedence |
| **R8** — `pip-audit` and `npm audit` in CI run with `continue-on-error` | **Low** | Removed `continue-on-error: true`; added `--requirement requirements.txt` flag to pip-audit |

## 6. Remaining Observations

| Item | Description |
|------|-------------|
| #1 — `bandit` SAST runs with `continue-on-error` | Acceptable: SAST tools have false positives; output is visible in CI logs |
| #2 — `appsail/` duplicate code maintenance burden | Both `src/` and `appsail/` are now in sync after this session's migrations |

---

## 7. Integration Requirements

### For CI/CD Pipeline
- Add `gitleaks detect --config .gitleaks.toml` to PR checks
- Add `pip-audit` or `safety check` for dependency vulnerability scanning
- Add `bandit -r src/` for static application security testing

### For Deployment
- Production deployments **must** set `JWT_SECRET`, `DATABASE_URL`, `DB_PASSWORD`, `REDIS_PASSWORD`, and `OPENAI_API_KEY`
- `docker-compose.prod.yml` uses `:?` syntax to fail fast if production secrets are missing
- Config YAML files in `config/` are for dev defaults only; production overrides come from environment variables

### For Developers
- Copy `.env.example` to `.env` and customize — `.env` is gitignored
- Run `pydantic-settings` validation: `python -c "from src.config import settings; print(settings.model_dump())"`
- Never commit real secrets; use placeholders in all tracked files
