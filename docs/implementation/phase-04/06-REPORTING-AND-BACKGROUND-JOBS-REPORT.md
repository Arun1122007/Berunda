# Project Berunda — Reporting and Background Jobs Implementation Report

> **Document ID:** BERUNDA-P4-007  
> **Status:** COMPLETED  
> **Date:** 2026-07-26

---

## 1. Overview

This report documents Workstream E: protected report generation with request/generation workflow, multiple report types, status lifecycle management, background job tracking schema, and audit event logging for reporting actions.

---

## 2. Implementation Details

### 2.1 Report Request Workflow

**Request Report**: `POST /api/v1/reports`

Accepts `ReportRequestCreate` with:
- `ReportType` — string: `fir_summary`, `investigation_progress`, `evidence_inventory`, `case_timeline`
- `Parameters` — optional JSON string (e.g., `{"case_master_id": 1, "include_evidence": true}`)
- `FileFormat` — string: `pdf`, `csv`, `json`

Generates a unique report ID with format `RPT-{12 hex chars}` and creates a `ReportRequest` record with `Status="requested"`. Logs `REQUEST_REPORT` audit event.

**List Reports**: `GET /api/v1/reports` — returns all reports for the requesting user (filtered by `RequestedByUserID`).

**Get Report**: `GET /api/v1/reports/{report_id}` — returns a single report request by ID.

**Generate Report**: `POST /api/v1/reports/{report_id}/generate` — generates report content synchronously:

| Report Type | Content |
|-------------|---------|
| `fir_summary` | Crime number, status ID, station ID from CaseMaster |
| `investigation_progress` | Notes count and latest note content |
| `evidence_inventory` | Evidence count, items with ID, type, status |

After generation, updates status to `"completed"` and sets `StorageObjectRef` to `reports/{report_id}.{file_format}`.

**Implementation files**:
- Router: `src/routers/report_router.py:1-61`
- Service: `src/services/fir_service.py:539-622`
- Schema: `src/schemas/report.py:8-34`
- Repository interface: `src/repositories/core.py:122-137`
- SQLite adapter: `src/repositories/sqlite_adapter.py:386-422`

### 2.2 Report Status Lifecycle

```
requested → (generate called) → completed
                                failed
```

- `requested` — initial state after creation
- `completed` — set after successful generation
- `failed` — set if generation encounters an error

The `ErrorMessage` field captures failure details. `StorageObjectRef` is populated on completion.

### 2.3 Background Job Schema

The `int_BackgroundJob` table (`src/models/int_models.py:349-366`) provides a generic background job tracking mechanism:

| Field | Type | Description |
|-------|------|-------------|
| JobID | String(50) PK | Unique job identifier |
| JobType | String(100) | Job classification (e.g., `ai_extraction`, `related_case_computation`, `report_generation`, `orphan_cleanup`) |
| Payload | Text | JSON payload with job parameters |
| IdempotencyKey | String(100) UNIQUE | Ensures idempotent job submission |
| RequestedByUserID | Integer FK | User who requested the job |
| Status | String(50) | `queued`, `running`, `completed`, `failed` |
| AttemptCount | Integer | Current retry attempt (default: 0) |
| MaxAttempts | Integer | Maximum retry attempts (default: 3) |
| ResultRef | String(500) | Reference to job output |
| ErrorMessage | Text | Error details on failure |
| CreatedAt | DateTime | Creation timestamp |
| StartedAt | DateTime | First execution timestamp |
| CompletedAt | DateTime | Completion/failure timestamp |

**Schema**: `src/schemas/job.py:8-27` defines `BackgroundJobCreate` and `BackgroundJobResponse`.

### 2.4 Audit Events

| Action | Audit Event Entity | Source |
|--------|--------------------|--------|
| Report requested | `REQUEST_REPORT` → ReportRequest | `fir_service.py:551-558` |

---

## 3. API Endpoints

| Method | Endpoint | Auth Required | Allowed Roles | Description |
|--------|----------|---------------|---------------|-------------|
| POST | `/api/v1/reports` | Yes | admin, officer, supervisor, analyst | Request report generation |
| GET | `/api/v1/reports` | Yes (any auth) | any authenticated | List user's reports |
| GET | `/api/v1/reports/{id}` | Yes (any auth) | any authenticated | Get report status |
| POST | `/api/v1/reports/{id}/generate` | Yes | admin, officer, supervisor, analyst | Generate report content |

---

## 4. Database Tables

| Table | Key Fields | Purpose |
|-------|------------|---------|
| `int_ReportRequest` | ReportID, RequestedByUserID, ReportType, Parameters, Status, StorageObjectRef, FileFormat, ErrorMessage, CreatedAt, CompletedAt, ExpiresAt | Asynchronous report generation tracking |
| `int_BackgroundJob` | JobID, JobType, Payload, IdempotencyKey, RequestedByUserID, Status, AttemptCount, MaxAttempts, ResultRef, ErrorMessage | Generic background job tracking |

---

## 5. Authorization Rules

| Operation | Required Role | Notes |
|-----------|---------------|-------|
| Request report | admin, officer, supervisor, analyst | Viewer forbidden |
| List reports | Any authenticated | Scoped to requesting user |
| Get report | Any authenticated | — |
| Generate report | admin, officer, supervisor, analyst | Viewer forbidden |

---

## 6. Test Coverage

**Test file**: `tests/api/test_report_api.py` — 20 tests

Key scenarios:
- Request all 4 report types (fir_summary, investigation_progress, evidence_inventory, case_timeline)
- Request with different file formats (pdf, csv, json)
- Supervisor and analyst role allowed
- Viewer forbidden, no auth 401, invalid payload 422
- List reports empty, after create, without auth
- Get report by ID, not found 404, without auth
- Generate report, not found 404, analyst allowed, viewer forbidden
- Admin can request reports
- User isolation: reports from user1 not visible to user2

**Result**: 20 API tests = full coverage

---

## 7. Status

**Verdict: COMPLETED** — All Workstream E features are implemented. The report workflow supports request, status tracking, and synchronous generation for three core report types. The `int_BackgroundJob` table is defined and ready for Phase 5 asynchronous worker integration. All report operations are authorization-gated and produce audit events.

