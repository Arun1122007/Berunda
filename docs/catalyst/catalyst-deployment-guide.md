# Zoho Catalyst Guide for Project Berunda

**Karnataka State Police Datathon 2026 — Hackathon-Only Implementation**
*Last verified: 25 July 2026*

**Target stack:** Next.js/React frontend, FastAPI/Python backend, custom Python analytics/AI
**Catalyst data center:** India (in)
**Goal:** Deploy the existing Berunda application on Zoho Catalyst without rewriting the project around unnecessary Catalyst services.

## 1. Final Catalyst Decision for Berunda

Use this architecture:

```text
Users
  |
  v
Catalyst Authentication
  |
  v
AppSail: berunda-web
Next.js / React frontend
  |
  | authenticated API calls
  v
AppSail: berunda-api
FastAPI / Python backend
  |
  +----------------------+----------------------+
  |                      |                      |
  v                      v                      v
Data Store              Stratus          Job Scheduling
Structured records      Files/artifacts  Scheduled processing
```

### Required Catalyst services

*   **AppSail — frontend**
    *   Hosts the Next.js application.
    *   Use Node.js managed runtime.
    *   Use Web Client Hosting only when the frontend is a fully static export.
*   **AppSail — backend**
    *   Hosts FastAPI and all Python analytics APIs.
    *   Use Python managed runtime first.
    *   Use an OCI container only when native geospatial or ML dependencies cannot run in the managed runtime.
*   **Data Store**
    *   Stores structured relational application records.
    *   Use it for cases, incidents, locations, entity links, alerts, model-run metadata, report metadata, and audit records.
*   **Stratus**
    *   Stores raw datasets, processed files, GeoJSON, Parquet, generated reports, model artifacts, exports, and screenshots.
    *   Keep hackathon datasets private unless a file is intentionally public.
*   **Authentication**
    *   Handles login, users, and roles.
    *   Use Hosted Authentication for fastest implementation.
*   **Job Scheduling**
    *   Runs recurring ingestion, analytics refreshes, alert generation, report generation, and cleanup jobs.
    *   Target an AppSail service or a small Job Function.

### Do not make these part of the MVP
*   API Gateway
*   Circuits
*   Old Catalyst Cron
*   QuickML
*   Zia AutoML
*   Zia Services
*   SmartBrowz
*   NoSQL
*   Signals
*   Push Notifications
*   Mail
*   Domain Mapping
*   Cache
*   Pipelines

*They can be added later only when a verified requirement needs them.*

## 2. Why This Fits the Existing Berunda Project

Berunda already has a modern application architecture:
*   Next.js/React frontend.
*   FastAPI/Python backend.
*   Crime analytics and visualization.
*   Geospatial analysis.
*   POLE-style relationship analysis.
*   Modus Operandi similarity.
*   Hotspot and spike detection.
*   Evidence-backed reports.
*   Role-based access.
*   Responsible AI and human review.

Catalyst AppSail supports Python and Node.js web services without requiring a framework rewrite. Therefore:
*   Do not convert FastAPI into many Catalyst functions.
*   Do not rebuild Next.js as a Catalyst-specific frontend.
*   Do not move custom analytics into Zia or QuickML merely to claim Catalyst usage.
*   Use Catalyst for hosting, identity, persistence, object storage, and scheduling.

## 3. Create the Catalyst Project

### 3.1 Use the correct account and data center
*   Use the Zoho account registered for the hackathon.
*   Select the India data center. Keep every team member and Catalyst resource in the same data center.
*   Recommended project name: `berunda-ksp-datathon-2026`
*   Avoid repeatedly creating test projects. Use one main Catalyst project and separate development and production environments.

### 3.2 Console steps
1.  Sign in to the Zoho Catalyst console.
2.  Confirm the selected organization.
3.  Click Create New Project.
4.  Enter the project name.
5.  Create the project.
6.  Open Settings → Project Settings → General.
7.  Set the timezone to Asia/Kolkata.
8.  Copy the generated Project ID.
9.  Open Collaborators and add only required team members.
10. Assign the minimum permissions needed by each collaborator.

### 3.3 Development and production
A newly created Catalyst project starts in the Development environment.
Use Development for:
*   Initial tables and buckets.
*   Test users.
*   AppSail deployments.
*   Local integration.
*   Demo data validation.
*   Repeated bug fixes.

Move to Production only after the complete demo flow works.

## 4. Understand the IDs, Keys, and Tokens

Do not call every Catalyst credential an “API key.” They serve different purposes.

| Item | Where to obtain it | Berunda usage | Secret? |
| :--- | :--- | :--- | :--- |
| Project ID | Settings → Project Settings → General | CLI, SDK, deployment identification | No |
| Organization ID | Organization portal/settings | Only when using a non-default organization | Usually no |
| AppSail endpoint | AppSail service details after deployment | Frontend and backend URLs | No |
| Authentication user token | Generated after a user signs in | Frontend-to-backend authorization | Yes, temporary |
| CLI token | `catalyst token:generate` | CI/CD or remote CLI execution | Yes |
| API Gateway API key | API Gateway API details | Only for APIs created for supported function targets | Yes |
| OAuth Client ID/Secret/Refresh Token | Zoho API Console self-client | Only when an application outside Catalyst accesses Catalyst SDK/APIs | Yes |
| ZAID | Catalyst environment/project information | Mainly external SDK initialization | Treat as configuration |
| Internal job secret | Your AppSail environment variables | Protect internal scheduled endpoints when required | Yes |

### 4.1 What you actually need now
For normal development:
*   Project ID
*   Catalyst CLI login
*   AppSail service endpoints
*   Catalyst Authentication session/token

For CI/CD later:
*   CATALYST_TOKEN
*   PROJECT_ID

For an application hosted entirely inside the same Catalyst project, do not generate OAuth self-client credentials unless the SDK integration specifically requires external access.

### 4.2 API Gateway key warning
The API Gateway API key is not the main project credential. It is generated for APIs configured through API Gateway for supported function or client targets. Berunda’s FastAPI backend is an AppSail service, so do not enable API Gateway only to obtain an API key.

### 4.3 Secret-handling rules
Never commit these values:
*   CATALYST_TOKEN
*   CLIENT_SECRET
*   REFRESH_TOKEN
*   API_GATEWAY_KEY
*   INTERNAL_JOB_SECRET
*   third-party AI keys
*   database credentials

Use:
*   `.env.local` # local development only
*   `.env.example` # variable names without values
*   AppSail environment variables
*   CI/CD secret storage

Add local secret files to `.gitignore`.

## 5. Install and Configure Catalyst CLI

### 5.1 Prerequisites
Install: Node.js LTS, npm, Python matching a currently supported AppSail Python runtime, Git, Catalyst CLI.
Install or update Catalyst CLI: `npm install -g zcatalyst-cli`
Verify: `catalyst --version`

### 5.2 Login to India data center
```bash
catalyst login --dc in
catalyst whoami --dc in
catalyst project:list --dc in
catalyst project:use <PROJECT_ID> --dc in
```

### 5.3 Initialize the existing repository
Run this from the repository root: `catalyst init`
Choose the existing Berunda Catalyst project.
Do not allow the CLI to replace the current enterprise folder structure. Keep Catalyst configuration files at the repository root and associate the existing frontend/backend directories with AppSail.

## 6. Deploy the FastAPI Backend to AppSail

### 6.1 Recommended runtime choice
Start with a Catalyst-managed Python runtime. Use an OCI container only when the project requires native packages that fail in the managed runtime (GDAL, GEOS, PROJ). Container images must be Linux AMD64 compatible.

### 6.2 Backend requirements
The backend should contain: `requirements.txt`, application source, health endpoint, startup command, Catalyst SDK integration. Retain the project’s real dependency versions and lock file.

### 6.3 Required listening behavior
AppSail supplies the port using: `X_ZOHO_CATALYST_LISTEN_PORT`.
The service must listen on: `host = 0.0.0.0` and `port = X_ZOHO_CATALYST_LISTEN_PORT`.
Recommended startup command:
`sh -c 'uvicorn app.main:app --host 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT:-9000}'`

### 6.4 Required endpoints
At minimum:
*   `GET /health/live`: process is running.
*   `GET /health/ready`: required Catalyst services can be accessed.
*   `GET /api/v1/system/info`: application version, environment, and non-secret build metadata.
Never return credentials or environment variable values.

### 6.5 Add the backend AppSail service
From the existing Catalyst project directory: `catalyst appsail:add`.
Configure memory, env_variables, build path, and runtime in `app-config.json`.

### 6.6 Catalyst Python SDK
Initialize the Catalyst SDK from the incoming request when the backend accesses Data Store, Stratus, Authentication. Business logic should not directly depend on Catalyst SDK calls throughout the codebase. Use an adapter layer.

## 7. Deploy the Next.js Frontend to AppSail

### 7.1 Choose the hosting mode
Use AppSail when the frontend uses: SSR, Server Components, Server Actions, Next.js API routes, Runtime authentication handling, Dynamic rendering. (AppSail is the safer default for Berunda).

### 7.2 Node startup command
Ensure `package.json` contains a production start script.
Recommended AppSail command:
`sh -c 'npm run start -- --hostname 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT:-9000}'`

### 7.3 Add frontend AppSail
Run: `catalyst appsail:add`.

### 7.4 Frontend environment variables
Development:
`NEXT_PUBLIC_API_BASE_URL=<development backend AppSail URL>`
Production:
`NEXT_PUBLIC_API_BASE_URL=<production backend AppSail URL>`
Do not place server secrets in variables prefixed with `NEXT_PUBLIC_`.

## 8. Configure Catalyst Authentication

### 8.1 Recommended mode
Use Hosted Authentication for the hackathon (Fastest setup, handles login UI).

### 8.2 Setup
Open Cloud Scale → Authentication. Select Native Catalyst Authentication → Hosted Authentication. Create demo accounts and roles.

### 8.3 Recommended roles
*   **APP_ADMIN**: Configuration, user management, all demo data
*   **INTELLIGENCE_ANALYST**: Analytics, searches, cases, reports
*   **SUPERVISOR**: Analytics, review, approval, report access
*   **READ_ONLY_VIEWER**: Dashboards and approved reports only

### 8.4 Frontend-to-backend authentication
Frontend obtains the Catalyst authentication token and sends it in the Authorization header to the FastAPI backend. Backend validates the user through Catalyst SDK/authentication support and performs application-level role checks.

## 9. Configure Data Store

### 9.1 What belongs in Data Store
Store structured, queryable, relational records: incidents, cases, locations, entities, case_entity_links, mo_features, analytics_alerts, model_runs, generated_reports, review_decisions, audit_events.

### 9.2 What does not belong in Data Store
Do not store large binary or analytical files directly in relational rows. Put these in Stratus and store metadata in Data Store.

### 9.3 Data Store setup procedure
Create tables in Cloud Scale → Data Store based on the approved ERD. Configure fields and permissions.

### 9.4 Bulk import and export
Use Catalyst CLI bulk operations for seed datasets: `catalyst ds:import <CSV_FILE_PATH>`

### 9.5 Graph and relationship analysis
Store POLE entities and edges in relational tables. Load relevant subsets into Python for graph computation to avoid introducing a separate graph database during the prototype.

## 10. Configure Stratus

### 10.1 Recommended bucket design
*   `berunda-data` (raw/processed datasets)
*   `berunda-artifacts` (models, indexes)
*   `berunda-reports`
*   `berunda-exports`

### 10.2 Permissions
Default to private. Enable encryption.

### 10.3 Every stored object should have metadata
Record object path, source, ingestion date, checksum, content type, size, version in `dataset_registry`.

### 10.4 Do not rely on AppSail local disk
Authoritative copies of every important dataset, report, model, or index must be persisted to Data Store or Stratus.

## 11. Configure Job Scheduling

Use Catalyst Job Scheduling, not the deprecated old Cron component.

### 11.1 Recommended jobs
*   Dataset validation refresh (AppSail backend)
*   Aggregate dashboard refresh (AppSail backend)
*   Hotspot/spike calculation (AppSail backend)
*   MO similarity index refresh (AppSail backend)

### 11.2 Setup procedure
Create an AppSail Job Pool for backend processing. Select `berunda-api`.

### 11.3 Internal job endpoints
Recommend `POST /internal/jobs/*`. Reject normal browser users, authenticate the scheduler, make idempotent, persist outputs.

### 11.4 India data-center constraint
Do not design workflows around Catalyst Circuits (unavailable in India DC for Job Scheduling).

## 12. Environment Variables
Use separate Development and Production values. Never expose private keys with `NEXT_PUBLIC_`. Rotate tokens.

## 13. Local Testing and Development Deployment
Run `npm test`, `npm run lint`, `pytest`. Then `catalyst serve`. Verify frontend/backend integration. Deploy to Dev: `catalyst deploy appsail`.

## 14. Production Deployment
Verify data, roles, and secrets. Open Catalyst console → Settings → Environments → Deployments. Switch to Production, run smoke test.

## 15. Services to Skip
Skip API Gateway, Functions (mostly), Web Client Hosting, NoSQL, Cache, QuickML, Zia, SmartBrowz, Signals, Circuits, Old Cron, Mail, Domain Mapping, Pipelines.

## 16. Recommended Berunda-to-Catalyst Mapping
*   **User login**: Catalyst Hosted Authentication
*   **User roles**: Catalyst Auth + Backend Auth
*   **Next.js dashboard**: AppSail Node.js
*   **FastAPI APIs**: AppSail Python
*   **Records/POLE/Alerts**: Data Store
*   **Datasets/Models/Reports**: Stratus
*   **Scheduled tasks**: Job Scheduling → AppSail

## 17. Minimum Demo Flow
User signs in via Catalyst -> Dashboard loads from Catalyst Data Store via FastAPI -> User runs hotspot analysis -> User generates report -> Saved to Stratus & Data Store.

## 18. Verification Checklist
(Follow standard checklist to ensure DC, CLI, Backend, Frontend, Data Store, and Stratus rules are met.)

## 19. Implementation Order
Follow exact order: Project -> Auth/CLI -> AppSail Health -> AppSail Frontend -> Hosted Auth -> Data Store -> Stratus -> Connect APIs -> Import Demo Data -> Job Scheduling -> Smoke Test -> Production.

## 20. Final Architecture Rule
The winning implementation is:
Existing Berunda product architecture + Catalyst AppSail + Catalyst Authentication + Catalyst Data Store + Catalyst Stratus + Catalyst Job Scheduling.
