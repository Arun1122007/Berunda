# Test Strategy

[//]: # (Document ID: BERUNDA-QA-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: QA, Developers | Source: SRS + Acceptance Criteria | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Test Levels

| Level | Scope | Tools | Automation | Run Frequency |
|-------|-------|-------|------------|---------------|
| Unit | Individual functions, modules | pytest (Python), Jest (JS) | Full | CI/CD (every commit) |
| Integration | API endpoints, data flow between functions | pytest + requests | Full | CI/CD (every merge) |
| System | End-to-end feature workflows | Playwright + pytest | Full | CI/CD (nightly) |
| Acceptance | Demo flow, planted test cases | Manual + Playwright | Partial | Pre-demo |
| Security | Auth, RBAC, field-level access, injection | OWASP ZAP + pytest | Full | CI/CD (weekly) |
| Performance | Response times, throughput | locust / k6 | Full | CI/CD (weekly) |

## 2. Unit Testing Requirements

| Module | Framework | Minimum Coverage | Key Tests |
|--------|-----------|-----------------|-----------|
| Entity Resolution | pytest | 90% | Blocking, similarity scoring, threshold logic |
| NER Extraction | pytest | 85% | Entity detection, confidence scoring |
| Risk Score | pytest | 90% | Feature engineering, fairness exclusion |
| Anomaly Detection | pytest | 90% | Z-score computation, alert threshold |
| Data Import | pytest | 85% | Validation, duplicate detection, rollback |
| RAG query | pytest | 80% | Template matching, retrieval, insufficient evidence |
| Auth / RBAC | pytest | 90% | JWT validation, role enforcement, jurisdiction scope |

### 1.6 Privacy Tests
| TC ID | Description | Input | Expected Output |
|-------|-------------|-------|-----------------|
| TC-PRIV-001 | CasteID not in any API response for non-Compliance role | Investigator JWT + GET /complainant/{id} | CasteID field absent from response |
| TC-PRIV-002 | ReligionID not in any API response for non-Compliance role | Investigator JWT + GET /complainant/{id} | ReligionID field absent from response |
| TC-PRIV-003 | Synthetic data label present in API response | GET /info | "synthetic": true in response |
| TC-PRIV-004 | No real PII in synthetic data | Scan all generated records against known public PII database | Zero matches |

### 1.7 Fairness Tests
| TC ID | Description | Input | Expected Output |
|-------|-------------|-------|-----------------|
| TC-FAIR-001 | Risk model feature list excludes CasteID/ReligionID | Load model feature list | CasteID, ReligionID, and variants absent |
| TC-FAIR-002 | Risk score distribution by gender is balanced | Compute scores for all PersonEntities | Mean score difference between genders < 0.1 |
| TC-FAIR-003 | Risk score distribution by district is balanced | Compute scores for all PersonEntities | Mean score difference between districts < 0.15 |
| TC-FAIR-004 | Fairness check cron job creates result record | Run CRON-004 | gov_FairnessCheckResult has new entry |

## 3. Integration Testing

| Test Suite | Endpoints Covered | Validation |
|-----------|------------------|------------|
| Case lifecycle | POST /cases/import → GET /cases/{id} | Full CRUD + NER trigger |
| Entity resolution | POST /cases/import → GET /persons | ER triggers and creates PersonEntity |
| Relationship graph | POST /cases/import (with planted links) → GET /persons/{id}/relationships | Link discovery |
| Geospatial | GET /hotspots?district=X&week=Y | Correct density tiles |
| Anomaly detection | GET /anomalies | Alerts generated for planted spike |
| RAG | POST /rag/query (5 demo questions) | Grounded answers with citations |
| Fairness check | GET /fairness-checks (after CRON-004) | Pass result |

## 4. Acceptance Testing (Planted Test Cases)

| Test ID | Feature | Planted Data | Expected Outcome |
|---------|---------|-------------|-----------------|
| AT-001 | Entity resolution | 4 name variants → 1 person | Auto-link + grey zone → manual confirm |
| AT-002 | Entity resolution | 2 similar but different persons | No match (new entities) |
| AT-003 | Hidden link discovery | Co-accused across 3 cases | Relationship graph shows connection |
| AT-004 | Hidden link discovery | Vehicle in 2 unrelated cases | Vehicle link connects cases |
| AT-005 | Risk scoring | Person with 5 prior cases | Score > 0.70, feature importance shows num_prior_cases |
| AT-006 | Anomaly detection | 1 week with 5x spike | Alert created with z-score > 3.0 |
| AT-007 | RAG query | Pre-defined questions | Correct, cited answers |
| AT-008 | Fairness check | Model features scanned | No CasteID/ReligionID in features |
| AT-009 | RBAC | Investigator tries to access outside jurisdiction | 403 response |
| AT-010 | RBAC | Compliance accesses restricted field | 200 response with CasteID visible |

## 5. Security Testing

| Test | Tool | Frequency |
|------|------|-----------|
| SQL injection scan | OWASP ZAP | Weekly |
| XSS scan | OWASP ZAP | Weekly |
| Authentication bypass | Custom pytest suite | Every commit |
| RBAC matrix validation | Custom pytest suite | Every commit |
| Field-level access control | Custom pytest suite | Every commit |
| Rate limit enforcement | locust | Weekly |
| Dependency vulnerability scan | pip-audit / npm audit | Weekly |

## 6. Test Data Management

All tests run against the deterministic synthetic dataset (seed 42). Each test run generates a fresh import of the dataset to ensure reproducibility.

| Property | Value |
|----------|-------|
| Dataset version | v1.0 (synthetic) |
| Faker seed | 42 |
| Test isolation | Each test creates and tears down its own records |
| Parallel execution | Test functions are independent; pytest-xdist for parallel runs |

## 8. Geospatial Testing
| TC ID | Description | Input | Expected Output |
|-------|-------------|-------|-----------------|
| TC-GEO-001 | Hotspot layer computed correctly | Set of coordinates in known district | Density tiles within district bounds only |
| TC-GEO-002 | Drill-down from state to district | Click state boundary | District boundaries rendered |
| TC-GEO-003 | Temporal filter updates map | Select date range | Only incidents in range shown |

## 9. Accessibility Testing
| TC ID | Description | Standard | Verification |
|-------|-------------|----------|-------------|
| TC-A11Y-001 | Keyboard navigation | WCAG 2.1 Level A | All interactive elements reachable via Tab |
| TC-A11Y-002 | Color contrast | WCAG 2.1 AA (4.5:1) | Automated contrast check |
| TC-A11Y-003 | Screen reader labels | WCAG 2.1 Level A | All non-text elements have ARIA labels |
| TC-A11Y-004 | Font scaling | WCAG 2.1 Level AA | UI functional at 200% zoom |
