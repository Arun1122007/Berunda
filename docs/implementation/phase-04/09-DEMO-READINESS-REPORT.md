# Project Berunda — Demo Readiness Report

> **Document ID:** BERUNDA-P4-010  
> **Status:** COMPLETED  
> **Date:** 2026-07-26

---

## 1. Overview

This report documents the Phase 4 demo flow, demo data availability, frontend routes, fallback behavior, and prerequisites for running the demonstration of all six workstreams.

---

## 2. Demo Flow (16 Steps)

The Phase 4 demo follows the complete investigation workflow from start to finish:

| Step | Action | Endpoint/Frontend | Workstream |
|------|--------|-------------------|------------|
| 1 | Login as officer | `/api/v1/auth/login` → `/` dashboard | Auth |
| 2 | View officer dashboard | `GET /dashboard/officer` | D |
| 3 | Search for an FIR | `POST /api/v1/search` with filters | C |
| 4 | View case detail | `/cases/:id` | A |
| 5 | Assign investigating officer | `POST /fir/{id}/assignments` | A |
| 6 | Add investigation note | `POST /fir/{id}/notes` | A |
| 7 | Update case status | `PUT /fir/{id}/status` | A |
| 8 | View case timeline | `GET /fir/{id}/timeline` | A |
| 9 | Create supervisor review | `POST /fir/{id}/reviews` | A |
| 10 | Generate related-case suggestions | `POST /fir/{id}/related-cases/generate` | C |
| 11 | Review and accept a suggestion | `PUT /related-cases/{id}/review` | C |
| 12 | Upload evidence file | `POST /fir/{id}/evidence` (via EvidencePanel) | B |
| 13 | View evidence inventory | `GET /fir/{id}/evidence` (via EvidencePanel) | B |
| 14 | Request a report | `POST /api/v1/reports` | E |
| 15 | Generate the report | `POST /reports/{id}/generate` | E |
| 16 | View supervisor dashboard | `GET /dashboard/supervisor` | D |

---

## 3. Demo Data Availability

### 3.1 Database Seeding

The Phase 3 foundation created synthetic data:
- 2 tiers: smoke (200 records) and demo (2,000 records)
- 8 entity types: CaseMaster, PersonEntity, VehicleLink, etc.
- 8 planted patterns: hotspot, serial-mo, linked-cases, anomaly-spike

The database (`src/berunda.db`) is pre-populated with Demo Data Pack (2,000 records tier) including:
- Multiple FIRs across police stations and crime categories
- Person entities with links to cases
- Vehicle links for vehicle number search testing
- Case assignments and investigation notes (if created during demo prep)

### 3.2 Synthetic Data Sources

- `data/synthetic/SYNTHETIC_GROUND_TRUTH_*.json` — ground truth tracking files
- `scripts/data/generate_synthetic.py` — synthetic data generator
- `scripts/data/synthetic_config.json` — district codes, crime heads, MO patterns

---

## 4. Frontend Routes for Demo

| Route | Page | Phase 4 Features Demonstrated |
|-------|------|-------------------------------|
| `/` | DashboardPage | Officer metrics, assigned count, recent activity, quick actions |
| `/cases/:id` | CaseDetailPage | Notes tab, evidence tab, timeline tab, related-cases tab |
| `/search` | SearchPage | Filter by crime number, date range, status, station, officer, crime head |
| `/reports` | ReportsPage | Request report, list reports, generate report |

### 4.1 Case Detail Page Tabs

The CaseDetailPage integrates 4 new Phase 4 components:
- **InvestigationNotes** — create and list notes with type/visibility
- **EvidencePanel** — upload and list evidence files
- **CaseTimeline** — chronological event view
- **RelatedCasesPanel** — generate, list, and review suggestions

---

## 5. Fallback Behavior

| Scenario | Behavior |
|----------|----------|
| No database connection | Health endpoint returns `degraded`; API operations return 500 |
| Empty database | Search returns 0 results; dashboards show zeros; related-cases returns empty |
| Missing FIR ID (404) | All FIR-scoped endpoints return 404 with descriptive message |
| No auth token | `get_current_user` returns `anonymous` role; district-scoped operations work |
| Invalid token | Auth dependency raises 401 |
| Insufficient role | `require_role` raises 403 |
| Invalid input payload | Pydantic validation returns 422 with field-level errors |
| Duplicate suggestion generation | Second call returns cached suggestions (idempotent) |
| Same-status update | Returns `Changed=False` with no audit event |

---

## 6. Demo Prerequisites

### 6.1 Environment

- Python 3.11+ virtual environment activated
- Dependencies installed: `pip install -r requirements.txt`
- `.env` file with `JWT_SECRET` set (development default works)
- SQLite database initialized and migrated to head

### 6.2 Starting the Application

```bash
# Start backend
cd src
python -m uvicorn main:app --reload --port 9000

# Start frontend (separate terminal)
cd apps/web
npm run dev
```

### 6.3 Authentication Tokens

Pre-generated JWT tokens for demo roles (using `JWT_SECRET=dev-secret-change-in-production`):

```python
# Officer token (district_id=1, police_station_id=5)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Supervisor token (district_id=1)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Admin token (no district restriction)
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Tokens can be generated via `POST /api/v1/auth/login` or the test helper `_make_token(role)`.

### 6.4 Verification Checklist

Before demo:
1. [ ] Backend running on port 9000
2. [ ] Frontend running on dev server
3. [ ] Database seeded with demo data
4. [ ] Login works for officer/supervisor/admin roles
5. [ ] Dashboard loads with non-zero metrics
6. [ ] At least one FIR exists for case detail navigation

---

## 7. Demo Script

A formal demo script is not yet created as a standalone file. The 16-step workflow above serves as the canonical demo sequence. Each step maps to a working backend endpoint and frontend component.

For a quick demo walkthrough:

```bash
# 1. Health check
curl http://localhost:9000/health

# 2. Login
TOKEN=$(curl -s -X POST http://localhost:9000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"officer@berunda.gov.in","password":"demo1234"}' | python -c "import sys,json;print(json.load(sys.stdin)['access_token'])")

# 3. Search FIRs
curl -s -X POST http://localhost:9000/api/v1/search \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"page":1,"pageSize":5}' | python -m json.tool

# 4. Create investigation note (replace FIR_ID)
curl -s -X POST http://localhost:9000/api/v1/fir/FIR_ID/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"Content":"Demo note","NoteType":"general"}'

# 5. View dashboard
curl -s http://localhost:9000/api/v1/dashboard/officer \
  -H "Authorization: Bearer $TOKEN" | python -m json.tool
```

---

## 8. Status

**Verdict: COMPLETED** — All 16 demo steps are fully implemented with working backend endpoints and frontend components. Demo data is available via the seeded database. Fallback behaviors handle all common error conditions. The application can be started with standard development commands and demonstrated end-to-end.

