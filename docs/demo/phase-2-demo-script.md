# Phase 2 — Demo Script

> **Document ID:** BERUNDA-DEMO-001 | **Version:** 1.0 | **Status:** APPROVED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## Problem Statement

Police investigators and crime analysts need a unified platform to manage FIR cases, review case details, and record new incidents. Currently, FIR data is scattered across disconnected systems and paper records.

## User Persona

**Rajesh Kumar** — SCRB Analyst at Karnataka State Police, Bengaluru
- Needs to review all filed FIRs across the state
- Must be able to drill into case details including involved persons
- Responsible for entering new cases into the system

## Starting State

1. Backend running on `http://localhost:8000`
2. Frontend running on `http://localhost:5173`
3. Database seeded with reference data and 24 demo cases
4. Demo user: `analyst@berunda.gov` / password from migration output

## Exact Steps

### Step 1: Login
1. Open browser to `http://localhost:5173`
2. **Expected**: Redirected to `/login`
3. Enter email: `analyst@berunda.gov`
4. Enter password: (from migration output)
5. Click "Sign In"
6. **Expected**: Redirected to dashboard showing crime statistics

### Step 2: View FIR Case List
7. Click "FIR Cases" in sidebar
8. **Expected**: Table showing 24 cases with Crime No, Date, Status
9. Note pagination at bottom (2 pages)
10. **Expected**: Status badges show correct colors

### Step 3: View Case Detail
11. Click on first case in list
12. **Expected**: Detail view showing:
    - Case information (Crime No, Case No, Date)
    - Crime details (Major Head, Minor Head)
    - Location (Latitude, Longitude) if available
    - Brief Facts narrative
    - Related persons (Complainants, Victims, Accused)
13. Click "Back" to return to list

### Step 4: Create New Case
14. Click "New Case" button
15. **Expected**: Form page with sections
16. Fill Crime No: `CR-2026-DEMO-001`
17. Fill Case No: `DEMO/2026`
18. Set Crime Major Head ID: `1`
19. Add Brief Facts: "Demo case for hackathon presentation"
20. Click "Create Case"
21. **Expected**: Success message, then redirect to new case detail

## Expected Backend Behavior

| Step | Backend Action |
|------|---------------|
| Login | Verify credentials → issue JWT tokens → log session |
| List | Query CaseMaster with district scoping → return paginated |
| Detail | Query CaseMaster JOIN related tables → return full detail |
| Create | Validate → insert CaseMaster + InvOccuranceTime → return created |

## Expected Persisted Data

```sql
-- After creating a case:
SELECT * FROM src_CaseMaster WHERE CrimeNo = 'CR-2026-DEMO-001';
-- Returns 1 row with the new case
```

## Failure Scenario

1. Enter invalid password during login
2. **Expected**: "Invalid credentials" error message
3. Navigate directly to `/cases/new` as officer user
4. **Expected**: 403 FORBIDDEN — cannot create cases

## Recovery Scenario

1. If token expires during session:
2. Backend returns 401
3. Frontend calls `/auth/refresh` with refresh token
4. On success: tokens updated, original request retried
5. On failure: redirect to `/login`

## Talking Points

- **Full-stack vertical slice**: Authentication → API → Database → UI
- **Security**: bcrypt passwords, JWT tokens with expiry, role-based access
- **Data integrity**: Input validation on both frontend and backend
- **User experience**: Loading states, error handling, empty states, success feedback
- **Extensibility**: Same patterns can add entity resolution, graph, RAG features

## Known Limitations

1. No real-time updates — page refresh required for new data
2. No file upload — CSV/Excel import deferred
3. No advanced filters — basic pagination only
4. No edit/delete from UI — only create and view

## Reset Instructions

```bash
# Reset database to clean state
rm berunda.db
alembic upgrade head

# Or use the Makefile if available
make reset-db
```
