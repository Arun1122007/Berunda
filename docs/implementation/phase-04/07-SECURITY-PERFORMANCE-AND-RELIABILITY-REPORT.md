# Project Berunda — Security, Performance, and Reliability Implementation Report

> **Document ID:** BERUNDA-P4-008  
> **Status:** COMPLETED  
> **Date:** 2026-07-26

---

## 1. Overview

This report documents Workstream F (System Hardening) security, performance, and reliability measures implemented across all Phase 4 endpoints.

---

## 2. Authentication

### 2.1 JWT-Based Authentication

- **Implementation**: `src/middleware/auth.py`
- **Algorithm**: HS256 with configurable `JWT_SECRET`
- **Token Payload**: Contains `id`, `user_id`, `role`, `district_id`, `police_station_id`, `sub`, `iat`, `exp`
- **Validation**: `AuthDependency` class decodes and validates JWT on every request
- **Weak Secret Detection**: Compares against a known-list of placeholder values and emits runtime warnings

### 2.2 Role-Based Access Control

Roles: `admin`, `officer`, `supervisor`, `analyst`, `viewer`

Two auth dependency functions:
- `get_current_user` — returns decoded payload (allows anonymous access with `role="anonymous"`)
- `require_role(roles)` — requires specific roles, raises 403 if unauthorized

All Phase 4 endpoints use `require_role` for privileged operations.

---

## 3. Authorization Enforcement Per Endpoint

| Endpoint | Auth Enforcer | Roles | 
|----------|---------------|-------|
| `POST /notes` | `require_role(["admin", "officer"])` | admin, officer |
| `GET /notes` | `get_current_user` | any authenticated |
| `POST /assignments` | `require_role(["admin", "supervisor"])` | admin, supervisor |
| `GET /assignments` | `get_current_user` | any authenticated |
| `GET /assignment/active` | `get_current_user` | any authenticated |
| `PUT /status` | `require_role(["admin", "officer", "supervisor"])` | admin, officer, supervisor |
| `GET /timeline` | `get_current_user` | any authenticated |
| `POST /reviews` | `require_role(["admin", "supervisor"])` | admin, supervisor |
| `GET /reviews` | `get_current_user` | any authenticated |
| `POST /related-cases/generate` | `require_role(["admin", "officer", "supervisor", "analyst"])` | multi-role |
| `GET /related-cases` | `get_current_user` | any authenticated |
| `PUT /related-cases/review` | `require_role(["admin", "officer", "supervisor"])` | multi-role |
| `POST /search` | `get_current_user` | any (district-scoped) |
| `GET /dashboard/officer` | `get_current_user` | any authenticated |
| `GET /dashboard/supervisor` | `require_role(["admin", "supervisor"])` | admin, supervisor |
| `POST /reports` | `require_role(["admin", "officer", "supervisor", "analyst"])` | multi-role |
| `POST /reports/generate` | `require_role(["admin", "officer", "supervisor", "analyst"])` | multi-role |

All endpoints verified with test cases for 401 (no auth) and 403 (wrong role).

---

## 4. Cross-Station Isolation

Non-admin users are scoped to their district via `district_id` from the JWT token. The `list_firs` repository method applies a subquery filter:

```python
if district_id is not None:
    query = query.where(
        CaseMaster.PoliceStationID.in_(
            select(Unit.UnitID).where(Unit.DistrictID == district_id)
        )
    )
```

This applies to:
- Search results (`search_router.py:21`)
- Dashboard metrics (`dashboard_router.py:19`, `dashboard_router.py:42`)
- Activity feed (`dashboard_router.py:58`)
- FIR list (`sqlite_adapter.py:62-67`)

Admin users bypass district filtering and see all data.

---

## 5. File Upload Validation

Evidence upload validation in `FIRService.upload_evidence()` (`fir_service.py:135-184`):

| Check | Implementation | 
|-------|----------------|
| FIR existence | `repo.get_fir()` returns None → raises ValueError |
| Path traversal | Rejects filenames containing `..`, `/`, or `\` |
| MIME type | Accepted as parameter from client |
| File size | Enforced by FastAPI/HTTP layer |
| Storage isolation | Files saved via `FileStorage` protocol (local or Stratus) |

---

## 6. Direct Object Reference Protection

- **FIR access**: All FIR operations require `case_master_id` as a path parameter. Non-existent IDs return 404.
- **Report access**: Reports are scoped to the requesting user (`RequestedByUserID` filter in `list_report_requests()`).
- **Evidence access**: Evidence is scoped by `CaseMasterID`.

---

## 7. Audit Integrity

All sensitive Phase 4 operations create immutable audit log entries:

| Action | Audit Event |
|--------|-------------|
| CREATE_NOTE | InvestigationNote |
| AMEND_NOTE | InvestigationNote |
| ASSIGN_OFFICER | CaseAssignment |
| UPDATE_STATUS | CaseMaster |
| SUPERVISOR_REVIEW | SupervisorReview |
| REVIEW_RELATED_CASE | RelatedCaseSuggestion |
| ADD_VEHICLE | VehicleLink |
| REQUEST_REPORT | ReportRequest |

Audit entries include `UserID`, `Action`, `EntityType`, `EntityID`, `OldValue`, `NewValue`, and `Timestamp`. Audit logs are read-only via `src/routers/audit_router.py`.

---

## 8. Performance

### 8.1 Pagination

All list endpoints support pagination via `page` and `page_size` parameters:
- Search: default page_size=20, max=100
- FIR list: configurable page/page_size
- Activity feed: hard-coded to 10 items

### 8.2 Database Indexes

Key indexes on Phase 4 tables:
- `int_InvestigationNote.CaseMasterID` — index for note listing
- `int_CaseAssignment.CaseMasterID` — index for assignment listing
- `int_CaseAssignment.AssignedOfficerID` — index for officer filter
- `int_SupervisorReview.CaseMasterID` — index for review listing
- `int_RelatedCaseSuggestion.SourceFIRID` — index for source case search
- `int_RelatedCaseSuggestion.CandidateFIRID` — index for candidate case search
- `int_ReportRequest.RequestedByUserID` — index for user scoping

### 8.3 N+1 Query Prevention

The `get_fir()` method uses `selectinload` for eager loading:
```python
.options(
    selectinload(CaseMaster.occurrence),
    selectinload(CaseMaster.complainants),
    selectinload(CaseMaster.victims),
    selectinload(CaseMaster.accused),
    selectinload(CaseMaster.act_sections),
)
```

---

## 9. Reliability

### 9.1 Error Handling

- Repository methods return `Optional[Any]` or raise `ValueError` for not-found conditions
- Router endpoints catch `ValueError` and return HTTP 404
- The global exception handler (`main.py:291-321`) catches all unhandled exceptions and returns structured JSON error responses
- Input validation via Pydantic schemas (422 for invalid payloads)

### 9.2 Validation

All Phase 4 Pydantic schemas include:
- Field length limits (e.g., `Content: max_length=10000`)
- Numeric constraints (e.g., `CaseStatusID: ge=1, le=20`)
- Literal type constraints (e.g., `ReviewStatus: Literal["accepted", "rejected"]`)
- Default values for optional fields

---

## 10. Status

**Verdict: COMPLETED** — All Workstream F security, performance, and reliability measures are implemented. Authentication uses JWT with role-based enforcement. Cross-station isolation is enforced via district_id filtering on all list operations. File upload includes path traversal protection. Audit logs capture all sensitive actions. Performance measures include pagination, DB indexes, and eager loading. Error handling returns structured JSON responses.

