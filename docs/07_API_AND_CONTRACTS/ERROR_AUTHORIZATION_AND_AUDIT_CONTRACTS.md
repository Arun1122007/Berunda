# Error, Authorization, and Audit Contracts

[//]: # (Document ID: BERUNDA-API-002 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Error Code Catalog

| Code | HTTP Status | Description | Retryable |
|------|------------|-------------|-----------|
| ERR-0001 | 400 | Validation error — invalid request body | No |
| ERR-0002 | 400 | Invalid cursor format | No |
| ERR-0101 | 401 | Missing or expired authentication token | Yes (refresh token) |
| ERR-0102 | 401 | Invalid authentication token | No |
| ERR-0201 | 403 | Insufficient role permissions | No |
| ERR-0202 | 403 | Jurisdiction restriction — cannot access records outside assigned district | No |
| ERR-0203 | 403 | Restricted field access denied (CasteID/ReligionID) | No |
| ERR-0301 | 404 | Resource not found | No |
| ERR-0302 | 404 | PersonEntity not found | No |
| ERR-0401 | 409 | Duplicate CrimeNo detected | No |
| ERR-0402 | 409 | Entity resolution merge conflict | No |
| ERR-0501 | 422 | Natural language query could not be parsed | Yes (rephrase) |
| ERR-0502 | 422 | RAG insufficient evidence | No (different question) |
| ERR-0601 | 429 | Rate limit exceeded | Yes (wait for window) |
| ERR-0701 | 500 | Internal server error | Yes |
| ERR-0702 | 500 | AI model inference failed | Yes |
| ERR-0703 | 502 | Upstream Catalyst service unavailable | Yes |
| ERR-0704 | 504 | Request timeout (RAG query > 10s) | Yes |

## 2. Authorization Model

### 2.1 Roles and Permissions Matrix

| Permission | Investigator | SCRB Analyst | Compliance Officer | Admin |
|------------|-------------|--------------|-------------------|-------|
| cases:read | Own district | All | All | All |
| cases:create | No | Yes | No | Yes |
| cases:import | No | Yes | No | Yes |
| persons:read | Own district | All | All | All |
| persons:search | Own district | All | All | All |
| persons:merge-review | Own district | No | No | Yes |
| persons:merge-confirm | Own district | No | No | Yes |
| relationships:read | Own district | All | All | All |
| relationships:traverse | No | Yes | No | Yes |
| hotspots:read | Own district | All | All | All |
| anomalies:read | Own district | All | All | All |
| riskscores:read | Own district | All | All | All |
| rag:query | Own district | All | All | All |
| auditlog:read | No | Own actions | All | All |
| fairness:read | No | No | All | All |
| restricted-fields:read | No | No | Yes | No |

### 2.2 Jurisdiction Scoping

Investigator role is scoped to their assigned district (derived from `src_Employee.DistrictID`). All queries implicitly filter by `PoliceStationID IN (user's assigned stations)`. The `X-Jurisdiction-Override` header (Compliance and Admin only) can temporarily bypass this filter for audit/investigation purposes, and its use is always logged.

## 3. Audit Contract

### 3.1 Audit Log Schema

Every API operation that reads or modifies data writes to `gov_AuditLog`:

| Field | Populated By | Always Present? |
|-------|-------------|-----------------|
| AuditLogID | Auto-increment | Always |
| UserID | Extracted from JWT | Always |
| Action | API endpoint handler | Always |
| EntityType | API endpoint handler | Always |
| EntityID | API endpoint handler | Always (except aggregate queries) |
| OldValue | API endpoint handler | Only for UPDATE/MERGE |
| NewValue | API endpoint handler | Always |
| Timestamp | API endpoint handler | Always |
| IPAddress | API Gateway (X-Forwarded-For) | Always |

### 3.2 Operations That Always Log

| Operation | Action Value | EntityType | Notes |
|-----------|-------------|------------|-------|
| GET /cases/{id} | CASE_READ | "CaseMaster" | Per-case read |
| GET /persons/{id} | PERSON_READ | "PersonEntity" | Per-person read |
| POST /cases/import | CASE_IMPORT | "CaseMaster" | Batch import |
| POST /cases | CASE_CREATE | "CaseMaster" | Manual create |
| PUT /persons/{id}/review | MERGE_CONFIRM / MERGE_REJECT | "PersonEntity" | Entity resolution |
| POST /rag/query | RAG_QUERY | "RAGCorpusChunk" | Question + answer logged |
| GET /risk/scores/{id} | RISK_SCORE_VIEW | "RiskScore" | Score view |
| GET /restricted-fields | RESTRICTED_FIELD_ACCESS | "ComplainantDetails" | Compliance role access |
| X-Jurisdiction-Override used | JURISDICTION_OVERRIDE | "AuditLog" | Compliance/Admin override |

### 3.3 Non-Logged Operations

GET list endpoints (without specific ID), health checks, and static metadata reads are not logged individually to avoid noise.
