# Phase 1 — Testing Strategy

**Document ID:** BERUNDA-TEST-001 | **Version:** 1.0 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-20

---

## Testing Levels

| Level | Language | Framework | Location | Dependencies |
|---|---|---|---|---|
| Unit | Python | pytest | `tests/unit/` | None (all mocked) |
| Unit | TypeScript | Vitest + Testing Library | `apps/web/__tests__/` | None (jsdom) |
| Integration | Python | pytest | `tests/integration/` | PostgreSQL, Redis |
| End-to-End | TypeScript | Playwright | `tests/e2e/` | Full stack |
| Performance | JavaScript | k6 | `tests/performance/` | Running application |
| Security | Python | pytest | `tests/security/` | Varies |

---

## Test Configuration

### Python (pytest.ini)
- Test paths: `tests/`
- File pattern: `test_*.py`
- Markers: `unit`, `integration`, `e2e`, `slow`, `performance`, `security`
- Coverage threshold: **80%** (enforced via `--cov-fail-under=80`)
- Strict markers and config validation
- All warnings as errors (except deprecation/user warnings)
- CLI logging at INFO level with structured format

### TypeScript (Vitest in vite.config.ts)
- Environment: jsdom
- Global test functions
- Setup file: `__tests__/setup.ts`
- CSS support enabled

---

## Phase 1 Bootstrap Tests

These tests validate that the project foundation is working:

| # | Test | File | Type | Description |
|---|---|---|---|---|
| 1 | App starts with valid config | `tests/unit/test_config.py` | Unit | Config loader returns expected values |
| 2 | App fails with missing config | `tests/unit/test_config.py` | Unit | Config loader raises error for missing required vars |
| 3 | Health endpoint returns OK | `tests/unit/test_app.py` | Unit | `GET /health` returns 200 with status |
| 4 | Readiness reflects deps | `tests/unit/test_app.py` | Unit | `GET /ready` returns dependency status |
| 5 | Global error handler | `tests/unit/test_app.py` | Unit | Unhandled errors return safe 500 |
| 6 | Root endpoint exists | `tests/unit/test_app.py` | Unit | `GET /` returns API info |
| 7 | Python package imports | `tests/unit/test_imports.py` | Unit | All Python modules import without error |
| 8 | Logger creates entries | `tests/unit/test_logging.py` | Unit | Logger produces structured JSON output |
| 9 | Frontend renders | `apps/web/__tests__/App.test.tsx` | Unit | App renders without crash |

---

## Coverage Threshold

**Phase 1 threshold:** 80%

**Rationale:** The bootstrap phase has a small number of focused tests with high coverage on the code that exists. As the codebase grows in Phase 2, the threshold may need adjustment. The 80% target is aspirational for the full project but achievable for the Phase 1 bootstrap code.

**Current coverage target areas:**
- `src/main.py` (FastAPI app): 100% route coverage
- `src/shared/config/__init__.py`: 100% coverage
- `src/shared/logging/__init__.py`: 100% coverage
- `apps/api/common/`: Unit tested through Python tests

---

## Test Fixtures

Existing fixtures in `tests/conftest.py`:

| Fixture | Scope | Purpose |
|---|---|---|
| `sample_fir_data` | Session | Load sample FIR JSON |
| `sample_entities_data` | Session | Load sample entity JSON |
| `crime_type_codes` | Session | Load crime type CSV |
| `test_db_path` | Function | Temp SQLite database path |
| `in_memory_db` | Function | In-memory SQLAlchemy session |
| `app` | Function | FastAPI application instance |
| `async_client` | Function | Async HTTP test client |
| `client` | Function | Sync HTTP test client |
| `auth_headers_*` | Function | Auth headers for different roles |
| `mock_catalyst_*` | Function | Catalyst service mocks |
| `sample_entity_match/non_match` | Function | Entity resolution test data |

---

## Running Tests

```powershell
# All tests with coverage
pytest --cov=src --cov-report=term-missing

# Unit tests only
pytest -m unit -v

# Integration tests (requires PostgreSQL + Redis)
pytest -m integration -v

# Frontend tests
cd apps/web && npm test

# All tests (Python + Frontend)
make test
```

---

## Test Quality Rules

1. **No fake tests** — every test must assert a meaningful behavior
2. **No `|| true` masking** — test failures must be visible (CI issue noted in audit)
3. **Deterministic** — tests must produce same result on every run
4. **Isolated** — unit tests must not depend on network or databases
5. **Fast** — unit tests should complete in < 1 second
6. **Descriptive names** — `test_health_endpoint_returns_200` not `test_health`
7. **Arrange-Act-Assert** — clear AAA pattern in each test

---

## Known Limitations

| Limitation | Impact | Resolution |
|---|---|---|
| No integration tests yet | Integration test fixtures are placeholders | Implement in Phase 2 |
| No E2E tests yet | Playwright configured but not implemented | Implement in Phase 2 |
| No performance tests | k6 script referenced but not created | Implement in Phase 2 |
| CI masks failures with `|| true` | False positives in CI | Fix in Phase 2 |
| No database models | Integration tests cannot run against real schema | Implement in Phase 2 |
