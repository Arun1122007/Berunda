# Project Berunda — Investigation Workflow Implementation Report

> **Document ID:** BERUNDA-P4-003  
> **Status:** COMPLETED  
> **Date:** 2026-07-26

---

## 1. Overview

The investigation workflow module implements Workstream A of the Phase 4 MVP. It provides case assignment, investigation notes (append-only/amendment model), case status transitions, supervisor review, and aggregated case timeline. All operations are authorization-gated and produce audit events.

---

## 2. Implementation Details

### 2.1 Case Assignment

- **Assign Officer**: `POST /api/v1/fir/{case_master_id}/assignments` — assigns an investigating officer to a case. Ends any existing active assignment by setting `Status="ended"` and `EndedAt` timestamp before creating a new active assignment.
- **Reassign**: Creating a new assignment automatically ends the prior active assignment.
- **List Assignments**: `GET /api/v1/fir/{case_master_id}/assignments` — returns full assignment history ordered by `AssignedAt` descending.
- **Active Assignment**: `GET /api/v1/fir/{case_master_id}/assignment/active` — returns the single assignment with `Status="active"`, or `null`.

**Implementation files**:
- Router: `src/routers/investigation_router.py:53-91`
- Service: `src/services/fir_service.py:278-319`
- Repository interface: `src/repositories/core.py:77-88`
- SQLite adapter: `src/repositories/sqlite_adapter.py:209-244`

### 2.2 Investigation Notes

- **Create Note**: `POST /api/v1/fir/{case_master_id}/notes` — creates a note with `Content`, `NoteType`, `Visibility`, and `AuthorID`. Supported note types: `general`, `witness_statement`, `forensic`, `field_visit`. Visibility scopes: `station`, `supervisor`, `private`.
- **Amendment Model**: `amend_note()` in the service creates a new note with `IsAmendment=True` and `OriginalNoteID` pointing to the original. Original notes are immutable.
- **List Notes**: `GET /api/v1/fir/{case_master_id}/notes` — returns notes in reverse chronological order.

**Implementation files**:
- Router: `src/routers/investigation_router.py:21-51`
- Service: `src/services/fir_service.py:212-277`
- Repository interface: `src/repositories/core.py:64-76`
- SQLite adapter: `src/repositories/sqlite_adapter.py:182-207`
- Schema: `src/schemas/investigation.py:8-25`

### 2.3 Case Status Transitions

- **Update Status**: `PUT /api/v1/fir/{case_master_id}/status` — updates `CaseMaster.CaseStatusID`. If the new status equals the old status, returns `Changed=False`. Otherwise updates the field, commits, and logs audit event `UPDATE_STATUS`.

**Implementation files**:
- Router: `src/routers/investigation_router.py:94-111`
- Service: `src/services/fir_service.py:321-342`

### 2.4 Supervisor Review

- **Create Review**: `POST /api/v1/fir/{case_master_id}/reviews` — creates a review record with `ReviewType` (`periodic`, `evidence_review`, `progress_review`), `Status` (`pending`, `approved`, `changes_requested`), `Comments`, and `ActionRequested`.
- **List Reviews**: `GET /api/v1/fir/{case_master_id}/reviews` — returns reviews ordered by `ReviewedAt` descending.

**Implementation files**:
- Router: `src/routers/investigation_router.py:124-154`
- Service: `src/services/fir_service.py:344-383`
- Repository interface: `src/repositories/core.py:90-97`
- SQLite adapter: `src/repositories/sqlite_adapter.py:246-267`

### 2.5 Case Timeline

- **Get Timeline**: `GET /api/v1/fir/{case_master_id}/timeline` — aggregates events from four sources:
  1. FIR registration date → `FIR_REGISTERED`
  2. Investigation notes → `INVESTIGATION_NOTE` (with `note_id`)
  3. Case assignments → `ASSIGNMENT` (with `assignment_id`)
  4. Supervisor reviews → `SUPERVISOR_REVIEW` (with `review_id`)
  
  Events are sorted by timestamp ascending.

**Implementation files**:
- Router: `src/routers/investigation_router.py:114-121`
- Repository: `src/repositories/sqlite_adapter.py:309-333`

---

## 3. API Endpoints

| Method | Endpoint | Auth Required | Allowed Roles | Description |
|--------|----------|---------------|---------------|-------------|
| POST | `/api/v1/fir/{id}/notes` | Yes | admin, officer | Create investigation note |
| GET | `/api/v1/fir/{id}/notes` | Yes | any authenticated | List investigation notes |
| POST | `/api/v1/fir/{id}/assignments` | Yes | admin, supervisor | Assign officer |
| GET | `/api/v1/fir/{id}/assignments` | Yes | any authenticated | List assignment history |
| GET | `/api/v1/fir/{id}/assignment/active` | Yes | any authenticated | Get active assignment |
| PUT | `/api/v1/fir/{id}/status` | Yes | admin, officer, supervisor | Update case status |
| GET | `/api/v1/fir/{id}/timeline` | Yes | any authenticated | Get case timeline |
| POST | `/api/v1/fir/{id}/reviews` | Yes | admin, supervisor | Create supervisor review |
| GET | `/api/v1/fir/{id}/reviews` | Yes | any authenticated | List supervisor reviews |

---

## 4. Database Tables

| Table | Key Fields | Purpose |
|-------|------------|---------|
| `int_InvestigationNote` | NoteID, CaseMasterID, AuthorID, Content, IsAmendment, OriginalNoteID, Visibility, CreatedAt, UpdatedAt | Append-only investigation notes with amendment chain |
| `int_CaseAssignment` | AssignmentID, CaseMasterID, AssignedOfficerID, AssignedByUserID, Status, AssignedAt, EndedAt | Assignment and reassignment history |
| `int_SupervisorReview` | ReviewID, CaseMasterID, SupervisorID, ReviewType, Status, Comments, ActionRequested, ReviewedAt | Supervisor review records |
| `src_CaseMaster` | CaseMasterID, CaseStatusID, CrimeRegisteredDate | Case status transitions (CaseStatusID updated in place) |

---

## 5. Authorization Rules

| Operation | Required Role | Notes |
|-----------|---------------|-------|
| Create note | admin, officer | Viewer and analyst forbidden |
| List notes | Any authenticated | — |
| Assign officer | admin, supervisor | Officer cannot self-assign |
| List assignments | Any authenticated | — |
| Active assignment | Any authenticated | — |
| Update status | admin, officer, supervisor | Viewer and analyst forbidden |
| View timeline | Any authenticated | — |
| Create review | admin, supervisor | Officer and analyst forbidden |
| List reviews | Any authenticated | — |

---

## 6. Test Coverage

**Test file**: `tests/api/test_investigation_api.py` — 32 tests
**Integration test file**: `tests/integration/test_phase4_endpoints.py` — 15 tests (including investigation)

Key test scenarios:
- Note creation, listing, empty list, missing FIR (404), invalid payload (422)
- Note authorization: viewer/analyst forbidden, no auth 401
- Officer assignment, reassignment, list, active assignment, not-found
- Assignment authorization: analyst/viewer forbidden
- Status update, same-status no-op, invalid status ID (422)
- Status authorization: viewer forbidden, analyst forbidden
- Timeline contains FIR_REGISTERED event, returns valid list
- Supervisor review creation, listing, empty list
- Review authorization: officer forbidden, no auth 401
- Admin overrides for assign, review, update-status

**Result**: 32 API tests + 5 integration tests = 37 tests covering investigation workflow

---

## 7. Audit Events

| Action | Audit Event Entity | Logged At |
|--------|--------------------|-----------|
| Note created | `CREATE_NOTE` → InvestigationNote | Service layer |
| Note amended | `AMEND_NOTE` → InvestigationNote | Service layer |
| Officer assigned | `ASSIGN_OFFICER` → CaseAssignment | Service layer |
| Status changed | `UPDATE_STATUS` → CaseMaster | Service layer |
| Supervisor review | `SUPERVISOR_REVIEW` → SupervisorReview | Service layer |

---

## 8. Status

**Verdict: COMPLETED** — All Workstream A features are implemented, tested, and authorization-enforced. The append-only amendment model preserves note integrity. Timeline provides a unified view of case activity. All sensitive actions produce audit events.

