# Project Berunda — Deployment Discovery & Architecture Audit

> **Document ID:** BERUNDA-DEP-001 | **Version:** 1.0  
> **Classification:** Internal | **Owner:** DevOps / Platform Lead  
> **Last Updated:** 2026-07-27  

---

## 1. Discovered System Architecture

| Component | Framework / Technology | Source Directory | Build Output | Catalyst Resource |
| :--- | :--- | :--- | :--- | :--- |
| **Frontend Web App** | React 18, Vite 5, TypeScript | `apps/web/` | `apps/web/dist/` | **Catalyst Web Client** (Static CDN) |
| **Backend API** | FastAPI 0.115, Python 3.10, Uvicorn | `appsail/berunda_api/` | `appsail/berunda_api/` | **Catalyst AppSail** (Python Runtime) |
| **Database Storage** | SQLite Async (`berunda.db`), SQLAlchemy 2.0 | `src/database.py` | `appsail/berunda_api/berunda.db` | **Catalyst Data Store / Bundled Storage** |
| **File Storage** | Private File System / Stratus SDK | `src/services/` | Stratus Buckets | **Catalyst Stratus** |
| **Background Processing** | Async Job Handlers | `src/tasks/` | AppSail Workers | **Catalyst Job Scheduling** |

---

## 2. Identified Environment & Config Baseline

- **Catalyst Project Name:** `Project-Rainfall`
- **Catalyst Project ID:** `48591000000013025`
- **Catalyst Environment:** `Development` (ID: `60079736152`)
- **Frontend Live URL:** `https://project-rainfall-60079736152.development.catalystserverless.in/app/index.html`
- **Backend AppSail URL:** `https://berunda-api-50044292022.development.catalystappsail.in`

---

## 3. Discovered & Remediated Deployment Blockers

1. **Frontend Blank White Screen:**
   - **Root Cause:** Missing `base: "./"` in `vite.config.ts` and missing `basename="/app"` in React Router `<BrowserRouter>`.
   - **Fix Applied:** Configured `base: "./"` in Vite config and dynamic `/app` detection in `main.tsx`. Rebuilt and redeployed.

2. **Missing `client-package.json` in Build Pipeline:**
   - **Root Cause:** `vite build` wiped `dist/` folder, removing `client-package.json` required by Catalyst CLI.
   - **Fix Applied:** Added `"postbuild"` hook in `package.json` to auto-generate `dist/client-package.json` after every build.

3. **Backend AppSail Heavy Native Dependencies:**
   - **Root Cause:** Native C-extension packages (`geopandas`, `spacy`, `presidio`) failing during AppSail container build.
   - **Fix Applied:** Replaced with pure-Python lightweight equivalents in `appsail/berunda_api/requirements.txt`.

4. **Celery Dependency Import Crash:**
   - **Root Cause:** `src/tasks/__init__.py` attempted module-level import of `celery` which is not available in cloud AppSail containers.
   - **Fix Applied:** Refactored `src/tasks/__init__.py` to use optional import fallback with no-op task stubs.
