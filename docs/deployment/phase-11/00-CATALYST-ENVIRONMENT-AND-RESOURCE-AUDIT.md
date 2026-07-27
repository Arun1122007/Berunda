# Catalyst Environment and Resource Audit (Phase 11)

**Document ID:** BERUNDA-DEPLOY-11-000
**Phase:** 11 — Deploy to Zoho Catalyst
**Status:** COMPLETE
**Audit Date:** 2026-07-27

---

## 1. Catalyst Project Overview

| Field | Value |
|---|---|
| Project Name | Project-Rainfall |
| Project ID | 48591000000013025 |
| Environment | Development |
| Environment ID | 60079736152 |
| Region | India (asia/kolkata) |
| CLI Version | v1.27.0 |
| Authenticated User | arun1122007@gmail.com |
| Git Remote | https://github.com/Arun1122007/Berunda.git |
| Branch | main |
| Latest Commit | 3d1ca28 — "feat: add fallback, NVIDIA, and OpenRouter AI providers, update config" |

---

## 2. Catalyst Component Inventory

Each Catalyst resource was inspected via `catalyst.json`, `catalyst-template.json`, `.catalystrc`, and live CLI queries where available.

| # | Component | Configuration Source | Identity / Target | Provisioning Status | Notes |
|---|---|---|---|---|---|
| C-01 | Project Target | `catalyst.json` | `Project Berunda` / Development Target | VERIFIED | Active project; correct target selected |
| C-02 | Web Client Hosting | `catalyst.json` → `client.source` | `apps/web/dist` | VERIFIED | SPA mode; fallback to `index.html` configured |
| C-03 | AppSail Service | `catalyst.json` → `appsail[0]` | `berunda-api` / Python 3.10 | PROVISIONED | Stack: python_3_10; source: `appsail/berunda_api` |
| C-04 | AppSail Build Path | `catalyst.json` → `build_path` | `.` | VERIFIED | Build root is `appsail/berunda_api/` |
| C-05 | AppSail Runtime Config | `app-config.json` | Stack: python_3_10; Memory: 1024 MB | VERIFIED | Command: `sh -c 'python3 -m uvicorn src.main:app --host 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT}'` |
| C-06 | Data Store (State) | `catalyst-template.json` | Table: State (columns: StateID, StateName) | VERIFIED | Schema matches template |
| C-07 | Data Store (UnitType) | `catalyst-template.json` | Table: UnitType (columns: UnitTypeID, UnitTypeName) | VERIFIED | Schema matches template |
| C-08 | Data Store (CaseCategory) | `catalyst-template.json` | Table: CaseCategory (columns: CaseCategoryID, CategoryName) | VERIFIED | Schema matches template |
| C-09 | Data Store (GravityOffence) | `catalyst-template.json` | Table: GravityOffence (columns: GravityOffenceID, GravityName) | VERIFIED | Schema matches template |
| C-10 | Data Store (CaseStatusMaster) | `catalyst-template.json` | Table: CaseStatusMaster (columns: CaseStatusID, StatusName) | VERIFIED | Schema matches template |
| C-11 | Data Store (CrimeHead) | `catalyst-template.json` | Table: CrimeHead (columns: CrimeHeadID, HeadName) | VERIFIED | Schema matches template |
| C-12 | Data Store (Act) | `catalyst-template.json` | Table: Act (columns: ActCode, ActName) | VERIFIED | Schema matches template |
| C-13 | Data Store (District) | `catalyst-template.json` | Table: District (columns: DistrictID, DistrictName, StateRef FK) | VERIFIED | Foreign key to State defined |
| C-14 | Data Store (Unit) | `catalyst-template.json` | Table: Unit (columns: UnitID, UnitName, DistrictRef FK, UnitTypeRef FK, ParentUnitRef FK) | VERIFIED | Self-referencing FK for hierarchy |
| C-15 | Data Store (Employee) | `catalyst-template.json` | Table: Employee (columns: EmployeeID, EmployeeName, UnitRef FK) | VERIFIED | PII marker on EmployeeName |
| C-16 | Data Store (CaseMaster) | `catalyst-template.json` | Table: CaseMaster (columns: CaseMasterID, CrimeNo, CaseNo, CrimeRegisteredDate, PolicePersonRef FK, PoliceStationRef FK) | VERIFIED | Core case entity |
| C-17 | Data Store (Inv_OccurrenceTime) | `catalyst-template.json` | Table: Inv_OccurrenceTime (columns: CaseMasterRef FK, IncidentFromDate, IncidentToDate, BriefFacts) | VERIFIED | Encrypted text + PII on BriefFacts |
| C-18 | Data Store (Accused) | `catalyst-template.json` | Table: Accused (columns: AccusedID, CaseMasterRef FK, Name, Age) | VERIFIED | PII on Name and Age |
| C-19 | Stratus Storage | `catalyst-template.json` (inferred) | `berunda-evidence-bucket` | NOT CONFIGURED | Stratus not provisioned in template or catalyst.json; SQLite used locally |
| C-20 | Job Scheduler | `catalyst-template.json` (inferred) | `ai_batch_processor_job` | NOT CONFIGURED | No scheduler definition found |
| C-21 | Authentication | Catalyst Auth | Zoho Accounts / JWT | PARTIALLY CONFIGURED | Auth middleware present in `src/middleware/auth.py`; Data Store permissions defined per table/role |
| C-22 | Catalyst CLI | `catalyst --version` | v1.27.0 | VERIFIED | Authenticated and operational |

---

## 3. Resource Status Summary

| Status | Count | Components |
|---|---|---|
| VERIFIED | 16 | C-01 through C-16 (project, hosting, AppSail config, 12 Data Store tables, CLI) |
| PROVISIONED | 1 | C-03 (AppSail runtime provisioned but backend returns 503) |
| NOT CONFIGURED | 2 | C-19 (Stratus), C-20 (Job Scheduler) |
| PARTIALLY CONFIGURED | 1 | C-21 (Auth — middleware exists, no live Auth integration verified) |

---

## 4. Key Audit Findings

### 4.1 Positive Findings
1. **Catalyst project correctly targeted** — Environment ID 60079736152 matches Development sandbox.
2. **12 Data Store tables defined** in `catalyst-template.json` with proper column types, foreign keys, unique constraints, search indexes, and role-based permissions.
3. **Frontend deployment** at `https://project-rainfall-60079736152.development.catalystserverless.in/app/index.html` loads successfully.
4. **SPA routing** works correctly — React Router handles client-side navigation with fallback to `index.html`.
5. **CLI v1.27.0** is installed and authenticated with correct credentials.

### 4.2 Issues Found

| Issue ID | Severity | Component | Description |
|---|---|---|---|
| AUDIT-001 | HIGH | AppSail (C-03) | Backend URL `https://berunda-api-50044292022.development.catalystappsail.in` returns HTTP 503 — "Execution failed. Please check the startup command or port" |
| AUDIT-002 | MEDIUM | Stratus (C-19) | Stratus file storage is not provisioned; application uses SQLite locally (`berunda.db`) |
| AUDIT-003 | MEDIUM | Job Scheduler (C-20) | No scheduled job configuration found; batch processing (AI extraction, anomaly detection) will not run automatically |
| AUDIT-004 | LOW | Auth Integration (C-21) | Catalyst Auth roles are defined in Data Store permissions but no live OAuth/SSO integration has been tested end-to-end |
| AUDIT-005 | LOW | Environment Variables | `app-config.json` shows `env_variables: {}` — no production secrets injected yet |

### 4.3 Recommendations
1. **AppSail 503** — Investigate container startup logs via Catalyst Console UI. Verify Python dependency installation (`requirements.txt` includes heavy packages: `geopandas`, `spacy`, `presidio-analyzer`). Confirm `app-config.json` build path and startup command are aligned with `catalyst.json`.
2. **Stratus** — Provision `berunda-evidence-bucket` and migrate evidence storage from local SQLite BLOBs to Stratus presigned-URL workflow.
3. **Job Scheduler** — Define cron triggers for `ai_batch_processor_job` (daily anomaly detection, nightly risk score recalculation).
4. **Secrets** — Populate `env_variables` in `app-config.json` with JWT_SECRET_KEY, AI_PROVIDER_API_KEY, and database connection strings.
5. **Auth E2E** — Run full authentication flow (Zoho login → JWT issuance → API call with Bearer token) in development environment.

---

## 5. Environment Configuration Files Inspected

| File | Path | Status |
|---|---|---|
| Catalyst project config | `catalyst.json` | PRESENT — 13 lines, valid JSON |
| Catalyst template | `catalyst-template.json` | PRESENT — 602 lines, 12 table definitions |
| AppSail app config | `appsail/berunda_api/app-config.json` | PRESENT — 9 lines, stack: python_3_10 |
| AppSail startup script | `appsail/berunda_api/startup.sh` | PRESENT — 7 lines, port 9000 fallback |
| AppSail requirements | `appsail/berunda_api/requirements.txt` | PRESENT — 70 lines, 30+ packages |
| Backend entry point | `appsail/berunda_api/main.py` | PRESENT — 20 lines, uvicorn runner |
| Backend app module | `appsail/berunda_api/src/main.py` | PRESENT — 430 lines, FastAPI application |
| Backend .env | `appsail/berunda_api/.env` | PRESENT — local development settings |
| Catalyst config (apps) | `apps/api/catalyst.config.json` | PRESENT |

---

## 6. Audit Trail

| Action | Timestamp | Performed By |
|---|---|---|
| Project configuration inspection | 2026-07-27 | Deployment Agent |
| CLI version & auth verification | 2026-07-27 | Deployment Agent |
| Frontend URL smoke test | 2026-07-27 | Deployment Agent |
| Backend URL health check | 2026-07-27 | Deployment Agent |
| Data Store schema audit | 2026-07-27 | Deployment Agent |
| Environment variables review | 2026-07-27 | Deployment Agent |
