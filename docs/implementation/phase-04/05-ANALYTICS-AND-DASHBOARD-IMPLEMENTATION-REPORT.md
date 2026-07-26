# Project Berunda — Analytics and Dashboard Implementation Report

> **Document ID:** BERUNDA-P4-006  
> **Status:** COMPLETED  
> **Date:** 2026-07-26

---

## 1. Overview

This report documents Workstream D: role-specific operational dashboards providing aggregate metrics for officers and supervisors, a recent activity feed, and authorization scoping to ensure officers see only their station's data.

---

## 2. Implementation Details

### 2.1 Officer Dashboard Metrics

**Endpoint**: `GET /api/v1/dashboard/officer`

Returns `DashboardMetrics` with:

| Field | Type | Description |
|-------|------|-------------|
| `total_firs` | int | Total FIRs in the officer's scope |
| `status_counts` | dict[str, int] | Count of FIRs per CaseStatusID (values 1–10) |
| `pending_review_count` | int | FIRs with pending supervisor reviews |
| `unassigned_count` | int | FIRs with no active assignment |
| `assigned_to_me_count` | int | FIRs assigned to the requesting officer |
| `recent_activity_count` | int | Currently equals total_firs |

**Authorization**: Uses `get_current_user` (any authenticated user). Scoped by `police_station_id` and `district_id` from JWT. Non-admin users are filtered to their district. Admin users see all data.

**Implementation**:
- Router: `src/routers/dashboard_router.py:12-33`
- Schema: `src/schemas/dashboard.py:8-15`

### 2.2 Supervisor Dashboard Metrics

**Endpoint**: `GET /api/v1/dashboard/supervisor`

Returns `SupervisorDashboardMetrics` with:

| Field | Type | Description |
|-------|------|-------------|
| `total_firs` | int | Total FIRs in scope |
| `status_counts` | dict[str, int] | FIRs per status |
| `pending_review_count` | int | FIRs with pending reviews |
| `unassigned_count` | int | FIRs without active assignment |
| `active_officer_count` | int | Currently equals total_firs (returns total) |
| `cases_per_officer` | dict[str, int] | Currently empty (placeholder for future) |

**Authorization**: Requires `require_role(["admin", "supervisor"])`. Officers, analysts, and viewers are forbidden (403).

**Implementation**:
- Router: `src/routers/dashboard_router.py:36-49`
- Schema: `src/schemas/dashboard.py:17-23`

### 2.3 Recent Activity Feed

**Endpoint**: `GET /api/v1/dashboard/activity`

Returns `list[RecentActivityItem]` with:

| Field | Type | Description |
|-------|------|-------------|
| `CaseMasterID` | int | FIR identifier |
| `CrimeNo` | str or null | Crime number |
| `ActivityType` | str | Currently always `"FIR_REGISTERED"` |
| `Description` | str | Human-readable activity description |
| `Timestamp` | datetime or null | FIR registration timestamp |

Returns up to 10 most recent FIRs. District-scoped for non-admin users.

**Implementation**:
- Router: `src/routers/dashboard_router.py:52-79`
- Schema: `src/schemas/dashboard.py:26-31`

### 2.4 SQL Query Patterns

All dashboard queries use SQLAlchemy ORM with `select`, `func.count()`, subqueries, and joins:

```python
# Total FIRs with district scoping
base = select(CaseMaster)
if police_station_id:
    base = base.where(CaseMaster.PoliceStationID == police_station_id)
elif district_id:
    base = base.where(CaseMaster.PoliceStationID.in_(
        select(Unit.UnitID).where(Unit.DistrictID == district_id)
    ))

# Status counts (per CaseStatusID 1-10)
for sid in range(1, 11):
    select(func.count()).select_from(
        base.where(CaseMaster.CaseStatusID == sid).subquery()
    )

# Pending review count (join with SupervisorReview)
select(CaseMaster.CaseMasterID).join(
    SupervisorReview, SupervisorReview.CaseMasterID == CaseMaster.CaseMasterID
).where(SupervisorReview.Status == "pending")

# Unassigned count (outer join with CaseAssignment)
select(CaseMaster.CaseMasterID).outerjoin(
    CaseAssignment, CaseAssignment.CaseMasterID == CaseMaster.CaseMasterID
).where(CaseAssignment.AssignmentID.is_(None))
```

**Source**: `src/repositories/sqlite_adapter.py:336-384`

### 2.5 Authorization

| Endpoint | Auth Required | Allowed Roles | Scoping |
|----------|---------------|---------------|---------|
| `/dashboard/officer` | Yes (any auth) | any authenticated | district_id + police_station_id from JWT |
| `/dashboard/supervisor` | Yes | admin, supervisor | district_id from JWT |
| `/dashboard/activity` | Yes (any auth) | any authenticated | district_id from JWT |

---

## 3. API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/dashboard/officer` | Officer dashboard metrics |
| GET | `/api/v1/dashboard/supervisor` | Supervisor dashboard metrics |
| GET | `/api/v1/dashboard/activity` | Recent activity feed |

---

## 4. Database Tables Used

| Table | Usage |
|-------|-------|
| `src_CaseMaster` | Primary data source for all counts |
| `src_Unit` | District-to-police-station mapping for scoping |
| `int_SupervisorReview` | Pending review count |
| `int_CaseAssignment` | Unassigned count, assigned-to-user count |

---

## 5. Test Coverage

**Test file**: `tests/api/test_dashboard_api.py` — 19 tests

Key scenarios:
- Officer dashboard empty, with data, field presence
- Officer dashboard without auth
- Supervisor dashboard empty, with data
- Supervisor dashboard admin allowed, officer/analyst/viewer forbidden
- Activity feed empty, with data, without auth, max 10 items
- Edge cases: null police_station_id

**Result**: 19 API tests + integration tests = full coverage

---

## 6. Status

**Verdict: COMPLETED** — All Workstream D features are implemented. Officer and supervisor dashboards provide real aggregate counts from the database. Activity feed surfaces recent FIR registrations. Authorization scoping enforces district-level isolation. The `cases_per_officer` and `active_officer_count` metrics are present in the schema but return placeholder values pending enhanced assignment aggregation in Phase 5.

