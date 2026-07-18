# Test Case Catalog

[//]: # (Document ID: BERUNDA-QA-002 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: QA, Developers | Source: SRS + Acceptance Criteria | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Unit Tests

### 1.1 Entity Resolution

| TC ID | Description | Input | Expected Output |
|-------|-------------|-------|-----------------|
| TC-ER-001 | Exact match auto-link | Same name, district, age | Score > 0.85, auto-link |
| TC-ER-002 | Phonetic match grey zone | "Venkatesh" vs "Venkatesha" | Score 0.75-0.85, grey zone |
| TC-ER-003 | Typo match grey zone | "Ramesh" vs "Rames" | Score 0.70-0.80, grey zone |
| TC-ER-004 | No match (different person) | "Ramesh Kumar", Bangalore vs "Ramesh Gupta", Mysuru | Score < 0.50, new entity |
| TC-ER-005 | Age discrepancy filter | Same name/district, age differs by 8 years | Blocking removes from candidates |
| TC-ER-006 | Four name variants | "Venkatesh", "Venkatesha", "Venkat", "V." | All resolve to single PersonEntity |
| TC-ER-007 | Similarity score bounds | All possible input combinations | Score always in [0.0, 1.0] |
| TC-ER-008 | Threshold configuration | Load custom thresholds from config | Thresholds applied correctly |

### 1.2 NER Extraction

| TC ID | Description | Input | Expected Output |
|-------|-------------|-------|-----------------|
| TC-NER-001 | Extract single person name | "Ramesh Kumar reported..." | PERSON: "Ramesh Kumar" with confidence |
| TC-NER-002 | Extract vehicle number | "...vehicle KA-01-AB-1234..." | VEHICLE: "KA-01-AB-1234" |
| TC-NER-003 | Extract multiple persons | "Ramesh and Suresh assaulted..." | 2 PERSON entities |
| TC-NER-004 | No entities | "Nothing unusual to report" | Empty extraction list |
| TC-NER-005 | Phone number extraction | "...call 9876543210..." | PHONE: "9876543210" |

### 1.3 Risk Scoring

| TC ID | Description | Input | Expected Output |
|-------|-------------|-------|-----------------|
| TC-RS-001 | 5 prior cases → high risk | PersonEntity with 5 prior cases | Score > 0.70 |
| TC-RS-002 | 0 prior cases → low risk | PersonEntity with 0 prior cases | Score < 0.30 |
| TC-RS-003 | Feature importance matches input | Known feature values | Importance sums to ~1.0 |
| TC-RS-004 | CasteID/ReligionID exclusion | Model features | Restricted fields absent |
| TC-RS-005 | District balance | Equal persons from multiple districts | No single district dominates |

### 1.4 Anomaly Detection

| TC ID | Description | Input | Expected Output |
|-------|-------------|-------|-----------------|
| TC-AD-001 | Normal week, no alert | Baseline distribution + normal count | Z-score < 2.0, no alert |
| TC-AD-002 | Spike week, alert triggered | 5x baseline count | Z-score > 3.0, alert created |
| TC-AD-003 | Empty district, no data | District with zero cases | No alert (insufficient data) |

### 1.5 Auth / RBAC

| TC ID | Description | Input | Expected Output |
|-------|-------------|-------|-----------------|
| TC-AUTH-001 | Valid token | Valid JWT | 200, correct user identity |
| TC-AUTH-002 | Expired token | Expired JWT | 401 |
| TC-AUTH-003 | Missing token | No Authorization header | 401 |
| TC-AUTH-004 | Invalid token | Malformed JWT | 401 |
| TC-RBAC-001 | Investigator reads own district | Investigator JWT + same district case | 200 |
| TC-RBAC-002 | Investigator reads other district | Investigator JWT + different district case | 403 |
| TC-RBAC-003 | Compliance reads restricted field | Compliance JWT + CasteID | 200 with CasteID |
| TC-RBAC-004 | Investigator reads restricted field | Investigator JWT + CasteID | 403 |

## 2. Integration Tests

| TC ID | Description | Steps | Expected |
|-------|-------------|-------|----------|
| TC-INT-001 | Full import flow | POST /cases/import → verify CaseMaster + NER + ER triggered | All three tables populated |
| TC-INT-002 | Import with duplicate | POST /cases/import with duplicate CrimeNo | Duplicate detected, row skipped |
| TC-INT-003 | Person search | POST /persons/search "Venkatesh" | PersonEntity found with linked cases |
| TC-INT-004 | Relationship graph | GET /relationships/network/{personId} | Network graph with edges |
| TC-INT-005 | Hotspot layer | GET /hotspots?districtId=1&weekStart=2024-01-01 | Density tiles returned |
| TC-INT-006 | RAG query | POST /rag/query "How many FIRs in Bengaluru Urban?" | Answer with citations |
| TC-INT-007 | Risk score computation | GET /risk/scores/{personEntityId} | Score + feature importance |
| TC-INT-008 | Audit trail | GET /audit-log?userId=X | All actions by user returned |
| TC-INT-009 | Fairness check | GET /fairness-checks (latest) | Pass result |

## 3. Acceptance Tests

| TC ID | Feature | Planted Data | Verification |
|-------|---------|-------------|-------------|
| TC-AT-001 | Entity resolution | "One Person, Four Names" setup | All 4 resolve to 1 PersonEntity |
| TC-AT-002 | Hidden link discovery | Co-accused cluster | Relationship graph shows cluster |
| TC-AT-003 | Vehicle link | Vehicle in 2 unrelated cases | VehicleLink connects cases |
| TC-AT-004 | Anomaly spike | Planted 5x spike week | AnomalyAlert created |
| TC-AT-005 | Fairness exclusion | Model feature scan | No restricted fields found |
| TC-AT-006 | RBAC boundary test | Cross-jurisdiction attempt | 403 response |

## 4. Security Tests

| TC ID | Description | Attack Vector | Expected |
|-------|-------------|--------------|----------|
| TC-SEC-001 | SQL injection in RAG | "DROP TABLE" in question | Query rejected; parameterized query prevents execution |
| TC-SEC-002 | SQL injection in search | "' OR 1=1 --" in name search | No injection; empty result |
| TC-SEC-003 | XSS in BriefFacts | Script tag in narrative | Sanitized output |
| TC-SEC-004 | Token replay | Reuse captured token | Rejected due to short expiry |
| TC-SEC-005 | CasteID field injection | Direct API call to restricted field with non-Compliance role | 403 |
