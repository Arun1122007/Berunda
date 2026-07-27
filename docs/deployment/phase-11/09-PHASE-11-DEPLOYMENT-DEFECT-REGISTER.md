# Phase 11: Deployment Defect Register

**Document ID:** BERUNDA-PHASE11-09
**Phase:** 11 — Deploy to Zoho Catalyst
**Last Updated:** 2026-07-27
**Status:** ACTIVE

---

## Defect Index

| Defect ID | Severity | Component | Title | Status |
|---|---|---|---|---|
| P11DEP-BLK-001 | BLOCKER | AppSail Backend | AppSail container startup failure (HTTP 503) | OPEN |
| P11DEP-MAJ-002 | MAJOR | Stratus Storage | Stratus file storage not provisioned | OPEN |
| P11DEP-MAJ-003 | MAJOR | Job Scheduler | Batch processing jobs not configured | OPEN |
| P11DEP-MIN-004 | MINOR | Auth Integration | Catalyst Auth end-to-end flow not verified | OPEN |
| P11DEP-MIN-005 | MINOR | Environment Variables | No production secrets injected (`env_variables: {}`) | OPEN |
| P11DEP-MIN-006 | MINOR | Frontend SPA | Initial SPA 404 on `/app/index.html` | CLOSED |

---

## Defect Details

### P11DEP-BLK-001 — AppSail Container Startup Failure (HTTP 503)

| Field | Value |
|---|---|
| **Status** | OPEN |
| **Severity** | BLOCKER |
| **Component** | AppSail Backend (`berunda-api`) |
| **Reported** | 2026-07-27 |
| **Detected by** | Deployment smoke test (HTTP GET to backend URL) |
| **Affected URL** | `https://berunda-api-50044292022.development.catalystappsail.in/` |
| **HTTP Response** | `503 Service Unavailable` |
| **Error Body** | `"Execution failed. Please check the startup command or port"` |

#### Symptom
The backend AppSail container fails to start and returns HTTP 503 for all endpoints (`/`, `/health`, `/ready`, `/api/v1/status`).

#### Root Cause (Hypothesized)
Multiple potential causes ranked by likelihood:

1. **Dependency installation timeout** — `requirements.txt` includes large packages (`geopandas`, `spacy`, `presidio-analyzer`) totaling ~600–800 MB. AppSail build phase may exceed time limit or memory ceiling.
2. **Port binding mismatch** — The Catalyst runtime injects `X_ZOHO_CATALYST_LISTEN_PORT` but the actual environment variable name or default value may differ.
3. **Incorrect entry point invocation** — `catalyst.json` delegates to `app-config.json` which uses `sh -c 'python3 -m uvicorn ...'`. The CLI may attempt a different default entry.
4. **Missing system libraries** — Native dependencies (GDAL, libpq, GEOS) required by `geopandas`, `psycopg2-binary`, and `shapely` may not be present in the AppSail Python 3.10 image.
5. **Memory exhaustion during startup** — Loading large ML/NLP libraries at import time may exceed 1024 MB container memory.
6. **Database connection failure** — `wait_for_db()` in the lifespan handler may crash the app if `DATABASE_URL` is not set (no env variables configured).

#### Troubleshooting Steps Attempted

| # | Date | Action | Result |
|---|---|---|---|
| 1 | 2026-07-27 | Verified Catalyst CLI auth (`catalyst --version`) | v1.27.0 authenticated as arun1122007@gmail.com |
| 2 | 2026-07-27 | Validated `catalyst.json` and `app-config.json` JSON syntax | Both valid |
| 3 | 2026-07-27 | Tested local uvicorn startup from `appsail/berunda_api/` | Starts successfully on localhost:9000 |
| 4 | 2026-07-27 | Reviewed port binding logic in `main.py` (lines 7–17) | Falls back to 9000 correctly |
| 5 | 2026-07-27 | Reviewed `startup.sh` port logic (line 3) | Defaults to 9000 |
| 6 | 2026-07-27 | `pip install --dry-run -r requirements.txt` | All packages resolvable |
| 7 | 2026-07-27 | Cross-referenced Catalyst AppSail port documentation | `X_ZOHO_CATALYST_LISTEN_PORT` is the documented variable |
| 8 | 2026-07-27 | Tested backend URL with curl | Confirmed 503 |
| 9 | 2026-07-27 | Inspected `app-config.json` command field | Uses correct `sh -c '...'` wrapper with variable substitution |
| 10 | 2026-07-27 | Estimated total dependency size | ~665–800 MB (may exceed build phase limits) |

#### Action Items

| # | Action | Owner | Target Date | Status |
|---|---|---|---|---|
| A-01 | Access Catalyst Console UI → AppSail → Logs to view container startup logs | Deployment Team | 2026-07-28 | PENDING |
| A-02 | Remove heavyweight unused deps: `geopandas`, `presidio-analyzer`, `presidio-anonymizer`, `neo4j`, `spacy` | Dev Team | 2026-07-28 | PENDING |
| A-03 | Simplify `app-config.json` command to `python3 main.py` | Dev Team | 2026-07-28 | PENDING |
| A-04 | Add `APP_ENV=production` and `DATABASE_URL` to `env_variables` | Dev Team | 2026-07-28 | PENDING |
| A-05 | Test with minimal `requirements.txt` (core only) to isolate dep issue | Dev Team | 2026-07-28 | PENDING |
| A-06 | Verify Catalyst AppSail Python 3.10 base image system libraries | Dev Team | 2026-07-28 | PENDING |
| A-07 | Implement health check endpoint that returns 200 without DB | Dev Team | 2026-07-28 | PENDING |
| A-08 | File support ticket with Zoho Catalyst if cause is platform-side | PM | 2026-07-29 | PENDING |

---

### P11DEP-MAJ-002 — Stratus File Storage Not Provisioned

| Field | Value |
|---|---|
| **Status** | OPEN |
| **Severity** | MAJOR |
| **Component** | Stratus Storage |
| **Description** | No Stratus bucket configured. Evidence upload/presigned-URL workflows will not function. Application currently uses local SQLite BLOBs via `repositories/local_adapter.py`. |
| **Impact** | File attachments, evidence images, and document uploads in production will fail. |
| **Resolution** | Provision `berunda-evidence-bucket` via Catalyst Console or CLI. Update `catalyst-template.json` with Stratus definition. Wire `repositories/catalyst_adapter.py` to use Stratus SDK. |

---

### P11DEP-MAJ-003 — Batch Processing Jobs Not Configured

| Field | Value |
|---|---|
| **Status** | OPEN |
| **Severity** | MAJOR |
| **Component** | Job Scheduler |
| **Description** | No Catalyst Job Scheduler definitions found. Background tasks (`anomaly.py`, `risk_scoring.py`, `ai_extraction.py`) will not execute. |
| **Impact** | AI-powered features (anomaly detection, risk score recalculation, automated FIR extraction) will not run without manual trigger. |
| **Resolution** | Define cron/scheduled triggers in `catalyst-template.json` or via Catalyst Console → Scheduler. |

---

### P11DEP-MIN-004 — Catalyst Auth End-to-End Flow Not Verified

| Field | Value |
|---|---|
| **Status** | OPEN |
| **Severity** | MINOR |
| **Component** | Authentication / Authorization |
| **Description** | Auth middleware (`src/middleware/auth.py`) and Data Store role-based permissions are defined, but no full OAuth login → JWT → API call flow has been tested. |
| **Impact** | Login, registration, and protected API routes may fail in deployment. |
| **Resolution** | Perform end-to-end auth test: Zoho login → token issuance → authenticated API call. |

---

### P11DEP-MIN-005 — No Production Secrets Configured

| Field | Value |
|---|---|
| **Status** | OPEN |
| **Severity** | MINOR |
| **Component** | Environment Configuration |
| **Description** | `app-config.json` has `"env_variables": {}`. Required variables (`JWT_SECRET_KEY`, `AI_PROVIDER_API_KEY`, `DATABASE_URL`, `APP_ENV`) are not set. |
| **Impact** | Backend may crash on startup if required env vars are missing. AI provider calls will fail. JWT signing will use an insecure fallback. |
| **Resolution** | Populate `env_variables` in `app-config.json` with production values. Use Catalyst Secrets for sensitive values. |

---

### P11DEP-MIN-006 — Frontend SPA 404 on `/app/index.html`

| Field | Value |
|---|---|
| **Status** | CLOSED |
| **Severity** | MINOR |
| **Component** | Frontend Web Client |
| **Description** | Initial deployment returned 404 for SPA routes. Fixed by configuring Catalyst Web Client to serve `index.html` as SPA fallback for all unmatched routes. |
| **Resolution** | Route mapping updated in Catalyst Console web client settings. React Router now handles client-side navigation correctly. |
| **Verified** | Frontend URL loads and displays "Berunda — Crime Intelligence Platform". SPA routing works. |

---

## Defect Summary Statistics

| Metric | Value |
|---|---|
| Total Defects | 6 |
| Open (BLOCKER) | 1 |
| Open (MAJOR) | 2 |
| Open (MINOR) | 2 |
| Closed | 1 |
| Closure Rate | 16.7% |
| Blocker Count | 1 (P11DEP-BLK-001) |

---

## Escalation Path

| Defect | Escalation Level | Contact |
|---|---|---|
| P11DEP-BLK-001 | Level 2 — Deployment Lead + Catalyst Support | Team Lead + Zoho Catalyst Help |
| P11DEP-MAJ-002 | Level 1 — Infrastructure Team | DevOps |
| P11DEP-MAJ-003 | Level 1 — Infrastructure Team | DevOps |
| All MINOR defects | Level 0 — Assigned Team Member | Developer |
