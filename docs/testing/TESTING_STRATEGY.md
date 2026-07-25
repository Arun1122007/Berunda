# Testing Strategy & Observability Foundation

> **Document ID:** BERUNDA-TEST-001 | **Version:** 1.0 | **Status:** ACTIVE
> **Owner:** Phase 1 Testing & Observability Lead
> **Last Updated:** 2026-07-25

---

## 1. Test Architecture

### 1.1 Test Pyramid

```
         /\
        /  \          E2E (Playwright) — few, slow, full-stack
       /    \
      /      \        Integration (pytest + httpx) — moderate, live deps
     /        \
    /          \      Smoke (pytest) — critical-path validation
   /            \
  /______________\    Unit (pytest) — fast, isolated, pure logic
```

| Layer | Runner | Location | Speed | Network | DB |
|-------|--------|----------|-------|---------|----|
| Unit | pytest | `tests/unit/` | <100ms | mocked | mocked |
| Smoke | pytest | `tests/smoke/` | <2s | allowed | best-effort |
| Integration | pytest | `tests/integration/` | <30s | yes | postgres |
| E2E | Playwright | `tests/e2e/` | <5m | yes | yes |
| Performance | k6 | `tests/performance/` | <3m | yes | yes |
| Security | pytest + tools | `tests/security/` | varies | yes | yes |

### 1.2 Test Markers

| Marker | Usage | Skipped by default? |
|--------|-------|---------------------|
| `smoke` | Startup, health, readiness, DB boundary | No |
| `unit` | Isolated unit tests | No |
| `integration` | Requires live PostgreSQL/Redis | No |
| `e2e` | Full stack Playwright | Yes (`--run-e2e`) |
| `slow` | Tests >5s | Yes (`--runslow`) |
| `performance` | k6 benchmarks | Yes |
| `security` | Security scans | No |

---

## 2. Test Coverage

### 2.1 Current Configuration

- **Fail-under threshold**: 61% (enforced in `pyproject.toml` and `pytest.ini`)
- **Source**: `src/`
- **Omitted**: `src/__main__.py`, `src/config.py`
- **Report formats**: terminal (missing lines) + HTML (`reports/coverage_html/`)
- **Excluded patterns**: `except ImportError`, `raise NotImplementedError`, type-checking blocks

### 2.2 Coverage Targets (Phased)

| Phase | Target | Focus |
|-------|--------|-------|
| Phase 1 (now) | 61% floor | Core API, database, logging, middleware |
| Phase 2 | 70% | Services, repositories, routers |
| Phase 3 | 80%+ | AI/ML modules, pipelines, edge cases |

---

## 3. Observability Infrastructure

### 3.1 Structured JSON Logging

**Module**: `src/shared/logging/__init__.py`

- JSON-formatted log entries with `timestamp`, `level`, `logger`, `message`
- Correlation ID injection from request context
- Dual output: stdout (always) + rotating file (when `LOG_DIR` is set)
- Level resolution from `LOG_LEVEL` env (default: INFO)

**Log format**:
```json
{"timestamp": "2026-07-25 03:30:34,123", "level": "INFO", "logger": "src.main", "message": "Application startup", "correlation_id": "abc-123"}
```

### 3.2 Correlation IDs

**Module**: `src/middleware/__init__.py` (CorrelationIDMiddleware)

- Injects `X-Request-ID` header on every response
- Generates UUID if client does not provide one
- Propagates to structured logging via `CorrelationFilter`
- Available on `request.state.correlation_id`

### 3.3 Health & Readiness

| Endpoint | Purpose | Checks |
|----------|---------|--------|
| `GET /health` | Liveness probe | Python runtime, database (SELECT 1), Neo4j (if configured), uptime |
| `GET /ready` | Readiness probe | Python runtime, database connection state, Neo4j (if configured) |
| `GET /api/v1/status` | Service metadata | API version, environment, service name |

- `/health` returns `"healthy"` or `"degraded"`
- `/ready` returns `"ready"` or `"degraded"`
- Both return structured JSON with `checks` object

### 3.4 Global Error Handling

**Module**: `src/main.py` (global_exception_handler)

- Catches all unhandled `Exception` subclasses
- Logs with correlation ID and request path
- Returns `{"error": {"code": "INTERNAL_ERROR", "message": "An unexpected error occurred."}}`
- Never leaks stack traces or internal details to clients

### 3.5 Graceful Shutdown

**Module**: `src/main.py` (lifespan handler)

- Startup: verifies DB connection, initializes Neo4j + NotificationService
- Shutdown: disposes DB engine, closes Neo4j connection
- Prometheus gauges reset on shutdown

### 3.6 Security Headers

**Module**: `src/middleware/__init__.py` (SecurityHeadersMiddleware)

| Header | Value |
|--------|-------|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Strict-Transport-Security` | `max-age=31536000; includeSubDomains` |

---

## 4. Test Details

### 4.1 Unit Tests (`tests/unit/`)

| File | What it validates |
|------|-------------------|
| `test_app.py` | Health endpoint structure, readiness checks, root info, API status, security headers, correlation IDs, error safety, metrics endpoint |
| `test_config.py` | YAML loading with environment overrides, deep merge, missing config fallback |
| `test_logging.py` | JSON formatting, correlation ID injection, logger singleton, multi-level output |
| `test_imports.py` | Clean imports for all modules (config, logging, validators, utils, app, ai, ml, pipelines) |
| `test_ai.py` | AI module behavior |
| `test_ml.py` | ML module behavior |
| `test_models.py` | ORM model instantiation |
| `test_routers.py` | Router endpoint wiring |
| `test_services.py` | Service layer business logic |
| `test_schemas.py` | Pydantic schema validation |
| `test_pipelines.py` | Pipeline execution |

**Fixtures** (`tests/unit/conftest.py`):
- Auto-mocking of external services (Catalyst, etc.)
- `mock_db_session` — mock SQLAlchemy session
- `mock_redis_client` — mock Redis client
- `mock_llm_client` — mock LLM client
- `mock_fir_repository` / `mock_entity_repository` — mock data repositories

### 4.2 Smoke Tests (`tests/smoke/`)

| File | What it validates |
|------|-------------------|
| `test_bootstrap.py` | App startup, all routers registered, Settings safe defaults, YAML config fallback, health endpoint (status, structure, uptime, content-type), readiness (DB check, status), error handling (404, JSON, no stack leak), API status metadata, all core module imports |
| `test_database_boundary.py` | `wait_for_db` returns False on unreachable DB, engine singleton behavior, dispose clears state, invalid URL raises ValueError, session factory produces sessions, double-dispose is safe, degraded health when DB is down |

**Fixtures** (`tests/smoke/conftest.py`):
- `smoke_app` — session-scoped FastAPI instance
- `smoke_client` — async HTTPX test client

### 4.3 Integration Tests (`tests/integration/`)

| File | What it validates |
|------|-------------------|
| `test_api_endpoints.py` | All CRUD endpoints, health, entities, graph, hotspots, anomalies, risk, RAG, audit auth, 404 handling (All with mocked DB session) |
| `test_auth_api.py` | Authentication integration (JWT, roles, permissions) |

**Fixtures** (`tests/integration/conftest.py`):
- DB session with transaction rollback
- Integration test client
- Sample FIR in DB

### 4.4 E2E Tests (`tests/e2e/`)

- **Framework**: Playwright (planned)
- **Markers**: `@pytest.mark.e2e`
- **Run**: `pytest -m e2e -v` or `npx playwright test`
- **Coverage**: Critical user journeys: login -> import FIR -> view graph -> query RAG

### 4.5 Performance Tests (`tests/performance/`)

- **Tool**: k6
- **Endpoints**: `/health`, `/ready`, `/api/v1/status`, `/api/v1/fir`, `/api/v1/entities`, `/api/v1/graph`, `POST /api/v1/auth/login`
- **Thresholds**: p95 < 500ms, error rate < 1%

### 4.6 Security Tests (`tests/security/`)

- **SAST**: CodeQL (GitHub), Ruff (Python)
- **DAST**: OWASP ZAP (scheduled)
- **Dependency scanning**: pip-audit, npm audit
- **Secrets detection**: TruffleHog, Gitleaks

---

## 5. Running Tests

### 5.1 Quick commands

```powershell
# All unit + smoke tests (fast, no external deps)
pytest tests/unit/ tests/smoke/ -v -m "smoke or unit"

# Smoke tests only
pytest tests/smoke/ -v

# With coverage
pytest tests/smoke/ tests/unit/ --cov=src --cov-report=term-missing --cov-report=html

# Full suite (excluding slow/e2e)
pytest tests/ -v --ignore=tests/e2e --ignore=tests/performance

# Integration tests only (requires PostgreSQL)
pytest tests/integration/ -v -m integration

# Single test file
pytest tests/smoke/test_bootstrap.py -v

# With verbose logging
pytest tests/ -v --log-cli-level=DEBUG
```

### 5.2 Make targets

```powershell
python -m pytest tests/   # or:
.\berunda.ps1 test        # if the orchestration script supports it
```

### 5.3 CI/CD Integration

All tests are wired into `.github/workflows/ci.yml` and `.github/workflows/test.yml`:

- **ci.yml**: Runs lint + test-python + test-node + build + docker on push/PR to main
- **test.yml**: Full test suite with per-layer jobs on PR to any branch

---

## 6. Known Gaps & Limitations

### 6.1 Current Gaps

| # | Gap | Impact | Timeline |
|---|-----|--------|----------|
| GAP-01 | No E2E test automation | Manual regression only | Phase 2 |
| GAP-02 | No contract tests (PACT/schema) | API changes may break consumers silently | Phase 2 |
| GAP-03 | No mutation testing | Coverage % may not reflect test quality | Phase 3 |
| GAP-04 | No load testing in CI | Performance regressions can slip | Phase 2 |
| GAP-05 | Integration conftest has placeholders | Integration tests skip critical path validation | Phase 1.5 |
| GAP-06 | No database migration tests | Schema changes untested | Phase 2 |
| GAP-07 | No chaos / resilience tests | Fault tolerance unvalidated | Phase 3 |
| GAP-08 | No log-based alerting tests | Monitoring alert rules untested | Phase 2 |

### 6.2 Known Limitations

| # | Limitation | Reason |
|---|------------|--------|
| L-01 | `wait_for_db` test uses real DB attempt — not fully isolated | Engine is module-level singleton; mocking requires careful teardown |
| L-02 | Health test may show "degraded" if DB is not running locally | Expected — tests assert `in ("healthy", "degraded")` |
| L-03 | Integration tests use mocked DB session, not real PostgreSQL | Live PG requires docker-compose services |
| L-04 | Coverage omits `src/config.py` | Pydantic Settings is configuration, not application logic |
| L-05 | `test_database_boundary` uses `dispose_engine()` which affects other tests if run in same session | Tests are ordered; smoke tests run last or in isolation |

### 6.3 Mitigation Strategy

1. **GAP-01, GAP-02, GAP-06**: Prioritize for Phase 2 with dedicated tickets
2. **L-01, L-03, L-05**: Use `pytest-order` or separate test sessions; document ordering requirements
3. **L-02**: Acceptable — health endpoint is tested, degraded state is valid

---

## 7. Integration Instructions

### 7.1 Adding a New Test

1. Choose the correct layer (unit/smoke/integration/e2e/performance/security)
2. Create `test_<feature>.py` in the appropriate directory
3. Add the correct marker: `@pytest.mark.<layer>`
4. Use existing fixtures from `tests/conftest.py` or the layer-specific `conftest.py`
5. Follow naming: `def test_<action>_<expected_behavior>()`
6. Run locally: `pytest tests/<layer>/test_<feature>.py -v`
7. Verify coverage: `pytest --cov=src --cov-fail-under=61`

### 7.2 Adding a New Module

1. If the module imports external services, add a mock target in `tests/unit/conftest.py`
2. Add an import test in `tests/smoke/test_bootstrap.py::TestCoreModuleImports`
3. Add module-specific unit tests in `tests/unit/test_<module>.py`

### 7.3 Test Data

- Static fixtures go in `tests/fixtures/` (JSON, CSV)
- Dynamic fixtures go in conftest.py fixtures
- Large synthetic data in `data/synthetic/`
- Use `tmp_path` for file-based tests (pytest built-in)

### 7.4 Continuous Improvement

- Coverage reports at `reports/coverage_html/`
- Run monthly gap analysis against GAP items above
- Update this document when test architecture changes

---

## 8. References

| Document | Location |
|----------|----------|
| CI/CD Pipeline | `.github/workflows/ci.yml` |
| Full Test Workflow | `.github/workflows/test.yml` |
| Security Scanning | `.github/workflows/security-scan.yml` |
| Pytest Configuration | `pyproject.toml` (tool.pytest.ini_options) |
| Pytest Markers | `tests/pytest.ini` |
| Pre-commit Hooks | `.pre-commit-config.yaml` |
| Logging Module | `src/shared/logging/__init__.py` |
| Middleware (Correlation ID) | `src/middleware/__init__.py` |
| Health/Readiness Endpoints | `src/main.py` |
| Global Error Handler | `src/main.py` (global_exception_handler) |
| Database Layer | `src/database.py` |
| Settings | `src/config.py` |
| Test Fixtures | `tests/conftest.py` |
| Agent Instructions | `AGENTS.md` |
