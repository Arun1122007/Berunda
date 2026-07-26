# 09 — Test Strategy and Quality Gates

**Document ID:** BERUNDA-ARCH2-TEST-001
**Version:** 1.0 | **Status:** APPROVED — Phase 2 test strategy baseline
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-26

---

## 1. Test Strategy Overview

The test strategy follows a risk-weighted approach: P0 feature paths must be fully covered before Day 8. Security tests must pass before Day 9. Demo rehearsal must complete before Day 10.

```
Day 1–3: Unit tests (services, ML)
Day 3–5: API contract tests (all P0 endpoints)
Day 5–6: Security boundary tests
Day 6–7: AI evaluation tests
Day 7–8: End-to-end demo flow tests
Day 9:   Demo rehearsal test
Day 10:  Demo-day smoke tests
```

---

## 2. Test Levels

### Level 0: Static Analysis

| Field | Value |
|-------|-------|
| **Purpose** | Catch syntax errors, type errors, import cycles |
| **Scope** | All Python files in `src/`; all TypeScript in `apps/web/src/` |
| **Tools** | `ruff` (Python linting), `mypy --strict` (type checking), `eslint` (TypeScript) |
| **Environment** | Local, CI |
| **Entry criteria** | Any code push |
| **Exit criteria** | Zero ruff errors; zero mypy errors on service/router files; zero eslint errors |
| **Automation** | GitHub Actions CI on every push |
| **Blocking severity** | BLOCKER — no merge with linting errors |
| **Artifacts** | `make lint` output; CI log |

---

### Level 1: Unit Tests

| Field | Value |
|-------|-------|
| **Purpose** | Test individual service functions, ML algorithms, and utility functions in isolation |
| **Scope** | All functions in `src/services/`, `src/ml/`, `src/pipelines/`, `src/ai/` |
| **Tools** | `pytest`; `pytest-asyncio`; `unittest.mock` |
| **Test data** | Fixtures from `tests/fixtures/`; no DB required (mocked) |
| **Environment** | Local |
| **Entry criteria** | Service function implemented |
| **Exit criteria** | ≥ 70% line coverage on all P0 service files; 0 failing tests |
| **Automation** | `make test-unit` |
| **Blocking severity** | BLOCKER for P0 services |
| **Artifacts** | `coverage.xml`; `pytest-report.xml` |

#### Unit Test Ownership

| Test Module | Covers | Blocker? |
|-------------|--------|---------|
| `tests/unit/test_auth_service.py` | Login, lockout, refresh, JWT decode | Yes |
| `tests/unit/test_fir_service.py` | CrimeNo gen, status machine, jurisdiction filter | Yes |
| `tests/unit/test_entity_service.py` | Extraction review, merge queue | Yes |
| `tests/unit/test_entity_resolution.py` | Soundex blocking, weighted scoring, threshold | Yes |
| `tests/unit/test_rag_service.py` | Jurisdiction scoping, guardrails, citation check | Yes |
| `tests/unit/test_risk_service.py` | Feature list validation, score range, fairness gate | Yes |
| `tests/unit/test_audit_service.py` | Event write, immutability check | Yes |
| `tests/unit/test_guardrails_service.py` | Protected-char refusal, citation validation | Yes |
| `tests/unit/test_graph_service.py` | NetworkX graph construction, BFS | Yes |
| `tests/unit/test_hotspot_service.py` | Density computation, district filter | No |
| `tests/unit/test_anomaly_service.py` | z-score computation, alert level | No |

---

### Level 2: Component Tests (API Contract Tests)

| Field | Value |
|-------|-------|
| **Purpose** | Verify API endpoints behave per the specification in Doc 05 |
| **Scope** | All 39 P0 endpoints; auth flows; error responses |
| **Tools** | `pytest` + `httpx.AsyncClient` with FastAPI `TestClient`; in-memory SQLite |
| **Test data** | Seed fixtures from `tests/fixtures/seed.py` |
| **Environment** | Local (SQLite); CI |
| **Entry criteria** | Endpoint router implemented |
| **Exit criteria** | All P0 endpoint tests passing; error codes match spec |
| **Automation** | `make test-api` |
| **Blocking severity** | BLOCKER for P0 |
| **Artifacts** | `pytest-api-report.xml` |

---

### Level 3: Database Integration Tests

| Field | Value |
|-------|-------|
| **Purpose** | Verify ORM models, migrations, constraints, and jurisdiction filters against real DB |
| **Scope** | All 5 new tables; all existing tables with new columns; jurisdiction filter correctness |
| **Tools** | `pytest`; Alembic test database; `pytest-postgresql` or Catalyst Data Store dev instance |
| **Environment** | catalyst-dev (Catalyst Data Store) |
| **Entry criteria** | Alembic migration 007–011 complete |
| **Exit criteria** | All constraints enforced; audit log INSERT-only permission verified |
| **Automation** | `make test-db` |
| **Blocking severity** | BLOCKER — schema must be verified before parallel implementation |

---

### Level 4: Authorization Tests

| Field | Value |
|-------|-------|
| **Purpose** | Verify every RBAC boundary and jurisdiction scope rule |
| **Scope** | All 39 endpoints × 4 roles matrix; cross-district IDOR; protected-field exclusion |
| **Tools** | `pytest` + JWT fixtures for each role |
| **Test data** | Fixture users for all 4 roles; fixture FIRs across 2 districts |
| **Environment** | Local |
| **Entry criteria** | All API contract tests passing |
| **Exit criteria** | All 20 critical security test scenarios pass (see §4) |
| **Automation** | `make test-auth` |
| **Blocking severity** | BLOCKER — must pass before demo day |

---

### Level 5: AI Evaluation Tests

| Field | Value |
|-------|-------|
| **Purpose** | Verify AI capabilities meet acceptance thresholds |
| **Scope** | NER F1, entity resolution recall, risk score calibration, RAG citation, protected-char refusal |
| **Tools** | `scripts/validation/eval_ner.py`; `scripts/validation/eval_er.py`; `scripts/validation/eval_rag.py` |
| **Test data** | 200-FIR evaluation set from `data/synthetic/` with ground truth JSON |
| **Environment** | Local (spaCy + scikit-learn available) |
| **Entry criteria** | AI pipelines implemented; seed data loaded |
| **Exit criteria** | All acceptance thresholds met (see Doc 06 §5) |
| **Automation** | `make evaluate-ai` |
| **Blocking severity** | BLOCKER — must pass before demo day |

---

### Level 6: Security Tests

| Field | Value |
|-------|-------|
| **Purpose** | Verify all security controls from Doc 07 are implemented |
| **Scope** | 20 threats in THR-001 to THR-020 |
| **Tools** | `pytest` + `bandit` (Python security scan) + manual tests |
| **Environment** | Local |
| **Entry criteria** | All API tests passing |
| **Exit criteria** | All 20 security test scenarios in §4 pass |
| **Automation** | `make test-security` |
| **Blocking severity** | BLOCKER |

---

### Level 7: End-to-End Tests

| Field | Value |
|-------|-------|
| **Purpose** | Verify the 10 demo steps work together from login to RAG answer |
| **Scope** | Full demo workflow with planted patterns |
| **Tools** | Manual browser test + checklist; optional: Playwright |
| **Test data** | Full demo seed dataset with all planted patterns |
| **Environment** | catalyst-dev or local with full stack |
| **Entry criteria** | All integration tests pass; seed data loaded |
| **Exit criteria** | All 10 demo steps complete without error; no manual data patches needed |
| **Automation** | Manual (Playwright optional if time allows) |
| **Blocking severity** | BLOCKER for demo release |

---

### Level 8: Performance Tests

| Field | Value |
|-------|-------|
| **Purpose** | Verify p95 latency targets under demo-scale data |
| **Scope** | FIR list (5000 records), global search, graph BFS, RAG query |
| **Tools** | `locust` or `k6` for local load test; manual timing for Catalyst |
| **Targets** | Search p95 < 3s; FIR list p95 < 2s; RAG (with LLM) p95 < 10s; RAG (mock) p95 < 500ms |
| **Environment** | Local with 5000-FIR dataset |
| **Entry criteria** | Full 2000-FIR demo dataset loaded |
| **Automation** | `make test-perf` |
| **Blocking severity** | HIGH (not blocker if MockProvider used for demo) |

---

### Level 9: Deployment Smoke Tests

| Field | Value |
|-------|-------|
| **Purpose** | Verify Catalyst deployment is functioning before demo |
| **Scope** | 6 smoke tests (login, FIR list, FIR detail, hotspot, RAG, graph) |
| **Tools** | Manual HTTP calls via curl or Postman |
| **Environment** | catalyst-demo |
| **Entry criteria** | Step 9 of deployment sequence complete |
| **Exit criteria** | All 6 smoke tests return expected status codes |
| **Automation** | `make smoke-catalyst-demo` |
| **Blocking severity** | BLOCKER for demo |

---

### Level 10: Demo Rehearsal

| Field | Value |
|-------|-------|
| **Purpose** | Full end-to-end rehearsal of demo story (10 steps) |
| **Scope** | DEMO-STEP-01 through DEMO-STEP-10 |
| **Environment** | catalyst-demo with seeded data |
| **Entry criteria** | All lower-level tests passing; seed data loaded |
| **Exit criteria** | 10 steps complete in ≤ 12 minutes; no manual intervention; fallback video ready |
| **Automation** | Manual with timer |
| **Blocking severity** | BLOCKER — demo cannot proceed if rehearsal fails |

---

## 3. Required Critical Test Scenarios

| TC-ID | Scenario | Level | Expected Outcome |
|-------|---------|-------|-----------------|
| TC-001 | Authorized INVESTIGATOR creates FIR with valid data | L2, L7 | HTTP 201; CrimeNo generated; NER triggered in BackgroundTask |
| TC-002 | Unauthenticated user is denied FIR list | L2, L4 | HTTP 401 UNAUTHORIZED |
| TC-003 | INVESTIGATOR A cannot access FIR from INVESTIGATOR B's district | L4 | HTTP 403 JURISDICTION_DENIED |
| TC-004 | Invalid FIR input (future OccurrenceDate) is rejected | L2 | HTTP 422 with field detail |
| TC-005 | FIR document upload succeeds (PDF ≤ 10 MB) | L2, L7 | HTTP 200; document_id returned; EvidenceMaster created |
| TC-006 | Invalid file type (EXE disguised as PDF) is rejected | L2, L6 | HTTP 415 UNSUPPORTED_MEDIA_TYPE |
| TC-007 | NER extraction completes and populates queue | L2, L5 | Queue items with status=PENDING; entity types correct |
| TC-008 | NER pipeline fails safely (model unavailable) | L1, L2 | FIRProcessingState.status=EXTRACTION_FAILED; FIR record intact; officer notified |
| TC-009 | Original BriefFacts unchanged after AI extraction | L2 | GET /firs/{id} → BriefFacts matches original; no AI-modified content |
| TC-010 | Officer edits AI suggestion (EDIT action) | L2 | Original text preserved in queue; edited value written to target table |
| TC-011 | Officer rejects all AI suggestions | L2 | No target records created; queue items status=REJECTED |
| TC-012 | Approved extraction values stored in correct target table | L3, L7 | PERSON → src_Accused or int_PersonEntity; VEHICLE → int_VehicleLink |
| TC-013 | FIR search returns only authorized records | L4 | INVESTIGATOR A gets own-district results only; SCRB_ANALYST gets all |
| TC-014 | RAG query does not return other-district chunks | L5, L6 | INVESTIGATOR A's RAG context contains only own-district FIR chunks |
| TC-015 | Evidence upload is traceable via audit log | L3 | gov_AuditLog has FIR.UPLOAD entry with correct fir_id and file_hash |
| TC-016 | FIR status change is audited | L3 | gov_AuditLog has FIR.STATUS_CHANGE with from/to status |
| TC-017 | Related-case suggestions include supporting signals | L2, L5 | API-FIR-009 response has signals with type and description; disclaimer present |
| TC-018 | Report access respects permissions (audit log own-only for INVESTIGATOR) | L4 | GET /api/v1/audit-logs with different user_id → 403 or filtered |
| TC-019 | Sensitive action (entity merge) recorded in audit log | L3 | ENTITY.MERGE.APPROVE in gov_AuditLog with score and entity IDs |
| TC-020 | Deployment health check succeeds on Catalyst | L9 | GET /health → 200 `{ "status": "healthy", "checks": { "database": true } }` |
| TC-021 | Demo data reset is safe and idempotent | L9 | After second seed run: same record count; no duplicate CrimeNos |
| TC-022 | Risk model fairness check passes | L5 | gov_FairnessCheckResult status=PASS; CasteRef not in feature list |
| TC-023 | Protected-characteristic RAG query is refused | L5, L6 | HTTP 403 PROTECTED_CHARACTERISTIC_QUERY; audit event logged |
| TC-024 | Entity resolution finds planted duplicates | L5 | `Raju Kumar` variants produce ≥ 1 merge candidate with score ≥ 0.65 |
| TC-025 | Graph BFS finds planted hidden link | L7 | API-GRP-002 returns path connecting Case 001 ↔ Case 042 via Raju Kumar and vehicle KA-01-AB-9999 |
| TC-026 | Audit log is append-only (no delete) | L6 | DELETE on gov_AuditLog via app user → permission denied |
| TC-027 | Account lockout after 5 failed logins | L2 | 6th login attempt → 403 ACCOUNT_LOCKED |
| TC-028 | JWT with tampered role claim is rejected | L4 | Manually modify role in JWT → 403 ACCESS_DENIED |
| TC-029 | SCRB_ANALYST cannot create FIR | L4 | POST /api/v1/firs with SCRB_ANALYST token → 403 |
| TC-030 | Hotspot anomaly badge appears for planted pattern | L7 | MG Road district shows AlertLevel=3 anomaly in hotspot response |

---

## 4. Quality Gates

Quality gates are checked before advancing to the next project phase or releasing the demo.

### Gate 0: Architecture Approval

| Criterion | Status Required | Verified By |
|-----------|---------------|-------------|
| Phase 2 documents 00–11 complete | PASS | Team review of Doc 11 |
| All ADRs approved or conditionally approved | PASS | ADR register in Doc 10 |
| P0 entity-to-API traceability gap = 0 | PASS | Doc 10 matrix |

### Gate 1: Schema Approval (Day 1)

| Criterion | Verification |
|-----------|-------------|
| Alembic migration 007–011 reviewed | `alembic history` |
| All 5 new tables exist in Catalyst Data Store | `SHOW TABLES` or Data Store console |
| Audit log INSERT-only permission confirmed | SQL test: `DELETE FROM gov_AuditLog` → fails |
| Role enum updated from 3 to 4 values | `DESCRIBE auth_User` |

### Gate 2: API Contract Approval (Day 3)

| Criterion | Verification |
|-----------|-------------|
| OpenAPI lint passes | `npx @redocly/cli lint docs/api/openapi.yaml` |
| All 39 P0 endpoints return expected status codes against test fixtures | `make test-api` |
| API contract approved by both team members | Sign-off in this doc |

### Gate 3: Security Approval (Day 6)

| Criterion | Verification |
|-----------|-------------|
| TC-003, TC-006, TC-014, TC-023, TC-026, TC-028 all pass | `make test-security` |
| No secrets in git history | `git-secrets --scan-history` |
| Bandit security scan passes (≤ 3 medium findings) | `bandit -r src/` |

### Gate 4: AI Evaluation Readiness (Day 6)

| Criterion | Threshold | Verification |
|-----------|---------|-------------|
| NER PERSON F1 | ≥ 0.70 | `make evaluate-ai` |
| NER VEHICLE F1 | ≥ 0.85 | `make evaluate-ai` |
| Entity resolution recall | ≥ 0.80 | `make evaluate-ai` |
| Risk fairness check | PASS | `make evaluate-ai` |
| RAG citation rate | ≥ 90% | `make evaluate-ai` |
| Protected-char refusal | 100% | TC-023 |

### Gate 5: Backend Implementation (Day 7)

| Criterion | Verification |
|-----------|-------------|
| All P0 backend services implemented | `make test-unit` ≥ 70% coverage |
| All P0 API endpoints return spec-compliant responses | `make test-api` 100% pass |
| Extraction pipeline writes to int_AIExtractionQueue | DB integration test |
| Merge pipeline writes to int_ERMergeCandidate | DB integration test |

### Gate 6: Frontend Implementation (Day 7)

| Criterion | Verification |
|-----------|-------------|
| All P0 screens implemented | Manual review vs route table |
| SyntheticDataBanner visible on all data screens | Manual visual review |
| AILabel visible on all extraction cards | Manual visual review |
| No authorization decisions in frontend code only | Code review |

### Gate 7: Integration (Day 8)

| Criterion | Verification |
|-----------|-------------|
| FIR create → NER → extraction review → approve end-to-end | TC-001, TC-007, TC-012 |
| Entity resolution → merge queue → merge approve | TC-019, TC-024 |
| Upload → text extract → NER → queue | TC-005, TC-007 |
| All 30 TC-* scenarios passing | `make test-all` |

### Gate 8: Demo Release (Day 10)

| Criterion | Verification |
|-----------|-------------|
| catalyst-demo health check passes | TC-020 |
| Demo seed data fully loaded | TC-021 |
| All 10 demo steps complete in ≤ 12 minutes | Demo rehearsal |
| MockProvider pre-scripted answers verified | Manual review |
| Fallback video prepared | File exists in `docs/demo/` |
| Rollback procedure documented and tested | Section 12 of Doc 08 |

---

## 5. Test Data Strategy

| Data Type | Source | Notes |
|-----------|--------|-------|
| Seed dataset (2000 FIRs) | `scripts/data/generate_synthetic.py --tier demo` | Idempotent; SYNTHETIC label |
| Evaluation dataset (200 FIRs + ground truth) | `scripts/data/generate_synthetic.py --tier eval` | Separate from demo data |
| Auth fixture users | `tests/fixtures/users.py` | One per role; hardcoded for tests |
| FIR fixture (2 districts) | `tests/fixtures/firs.py` | Used for jurisdiction tests |
| Planted patterns | Embedded in seed script | Documented in SYNTHETIC_GROUND_TRUTH |
| MockProvider responses | `src/ai/providers/mock_provider.py` | Pre-scripted for 3 RAG questions |

---

## 6. CI Pipeline Configuration

```yaml
# .github/workflows/ci.yml (design; not yet executed)
name: Berunda CI

on:
  push:
    branches: [main, dev]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install ruff mypy
      - run: ruff check src/
      - run: mypy src/ --ignore-missing-imports

  test-unit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest tests/unit/ --cov=src --cov-report=xml --cov-fail-under=70

  test-api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -r requirements.txt
      - run: pytest tests/api/ -v

  test-security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install bandit
      - run: bandit -r src/ -ll
      - run: pytest tests/security/ -v

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: cd apps/web && npm ci && npm run build
```

---

## 7. Test Coverage Targets

| Module | Line Coverage Target | Blocking? |
|--------|---------------------|---------|
| `services/auth_service.py` | ≥ 80% | Yes |
| `services/fir_service.py` | ≥ 75% | Yes |
| `services/entity_service.py` | ≥ 75% | Yes |
| `ml/entity_resolution.py` | ≥ 85% | Yes |
| `services/rag_service.py` | ≥ 70% | Yes |
| `services/risk_service.py` | ≥ 75% | Yes |
| `services/audit_service.py` | ≥ 80% | Yes |
| `services/guardrails_service.py` | ≥ 90% | Yes |
| `middleware/auth.py` | ≥ 85% | Yes |
| `services/graph_service.py` | ≥ 70% | No |
| `services/hotspot_service.py` | ≥ 60% | No |
| `services/anomaly_service.py` | ≥ 60% | No |

---

*End of 09-TEST-STRATEGY-AND-QUALITY-GATES.md*
