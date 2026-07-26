# Phase 3 Deployment Readiness Report — Project Berunda

> **Document ID:** BERUNDA-VERIF3-DEPLOY-001 | **Version:** 1.0 | **Status:** FINAL  
> **Classification:** INTERNAL | **Owner:** Independent Verification Team  
> **Date:** 2026-07-26  

---

## 1. Executive Summary

This report assesses the deployment readiness of Project Berunda Phase 3 across two target environments: local development (mocked services) and Zoho Catalyst production (serverless AppSail, ZCQL Data Store, Stratus Storage, and Zia AI).

### Deployment Verdict: FAIL (Not Deployable to Zoho Catalyst)
While the frontend compiles cleanly and the backend runs in standalone local development mode over SQLite, **the codebase is not deployable to Zoho Catalyst** in its current state. Severe architectural coupling in the data layer and broken endpoint invocations in the AI provider layer prevent successful execution in the hackathon production environment.

---

## 2. Environment Readiness Matrix

| Environment | Target Technology | Readiness Verdict | Key Blockers / Findings |
|---|---|---|---|
| **Local Development** | Vite + FastAPI + SQLite | **CONDITIONAL PASS** | Requires pre-installed Python wheels; frontend compiles in 24s. |
| **Catalyst AppSail** | Serverless Container | **CONDITIONAL PASS** | `catalyst.json` and Docker configurations exist and are valid. |
| **Catalyst Data Store** | ZCQL / Cloud Relational | **FAIL (BLOCKED)** | Routers bypass Repository Pattern; execute raw SQLAlchemy ORM. |
| **Catalyst Stratus** | Object File Storage | **PARTIALLY READY** | Adapter exists; unintegrated in `FIRService` document creation. |
| **Catalyst Zia / QuickML**| AI / ML Serverless | **FAIL (BLOCKED)** | Provider targets non-existent `/functions/llm-chat/execute` path. |

---

## 3. Detailed Deployment Analysis

### 3.1 Frontend AppSail / Client Hosting
- **Verification**: Executed `npm run build` in `apps/web/`.
- **Result**: Successfully compiled 2,411 modules in 24.07 seconds, generating production-optimized static assets (`dist/index.html`, `dist/assets/`).
- **Verdict**: **READY**. The static bundle is immediately deployable to Zoho Catalyst Client Hosting or an Nginx web container.

### 3.2 Backend Container Deployment (AppSail)
- **Verification**: Inspected `catalyst.json`, `.catalystrc`, and `src/main.py` initialization hooks.
- **Result**: The application correctly inspects `X_ZOHO_CATALYST_LISTEN_PORT` to adjust binding ports dynamically in production.
- **Verdict**: **CONDITIONAL READY**. Container startup logic is valid.

### 3.3 Database Deployment (Catalyst ZCQL Data Store)
- **Verification**: Evaluated router and service data access implementations against Phase 2 ZCQL migration requirements.
- **Result**: All 16 domain routers in `src/routers/` directly inject SQLAlchemy `AsyncSession` and execute raw SQL/ORM queries (`select(CaseMaster)`). Because Zoho Catalyst Data Store uses ZCQL (a proprietary SQL dialect accessed via `zcatalyst-sdk`), raw SQLAlchemy queries will fail at runtime in AppSail.
- **Blocker Reference**: **P3V-BLK-001**.
- **Verdict**: **FAIL**.

### 3.4 Storage Deployment (Catalyst Stratus)
- **Verification**: Evaluated file persistence integration in `FIRService`.
- **Result**: `StratusFileStorage` is implemented in `src/repositories/catalyst_adapter.py`, but `FIRService` and `fir_router.py` lack dependency injection bindings for file uploads, leaving document persistence unintegrated.
- **Defect Reference**: **P3V-MAJ-001**.
- **Verdict**: **FAIL**.

### 3.5 AI Engine Deployment (Catalyst Zia / QuickML)
- **Verification**: Analyzed `src/ai/providers/catalyst.py`.
- **Result**: The provider posts JSON payloads to `/functions/llm-chat/execute`. No corresponding Zoho Catalyst Serverless Function exists in the workspace, nor does Zoho Zia expose AI models at this arbitrary REST path. Deploying this provider will result in 100% AI extraction failure.
- **Blocker Reference**: **P3V-BLK-002**.
- **Verdict**: **FAIL**.

---

## 4. Prerequisites for Catalyst Production Release

Before Phase 3 can receive deployment approval for the Zoho Catalyst hackathon environment, the engineering team must:
1. Complete the Repository Pattern refactoring across `src/routers/` to route database calls through `CatalystFIRRepository` when running in AppSail.
2. Replace hardcoded `/functions/llm-chat/execute` HTTP requests in `CatalystProvider` with official `zcatalyst-sdk` AI model invocations.
3. Bind `StratusFileStorage` to the FIR document ingestion endpoint.
4. Perform an end-to-end smoke test inside a live Zoho Catalyst development sandbox.
