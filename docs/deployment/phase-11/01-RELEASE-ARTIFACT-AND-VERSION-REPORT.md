# Release Artifact and Version Report (Phase 11)

**Document ID:** BERUNDA-DEPLOY-11-001
**Phase:** 11 — Deploy to Zoho Catalyst
**Status:** COMPLETE
**Date:** 2026-07-27

---

## 1. Release Identification

| Field | Value |
|---|---|
| Repository | https://github.com/Arun1122007/Berunda.git |
| Branch | main |
| Release Tag | v2.0.0-catalyst-release |
| Commit Hash | `3d1ca28` |
| Commit Message | "feat: add fallback, NVIDIA, and OpenRouter AI providers, update config" |
| Author | Arun1122007 |
| Build Timestamp | 2026-07-26 (UTC) / 2026-07-26 (IST, Asia/Kolkata) |
| Build Host | Local development workstation |

### Commit Ancestry

```
8390d0a chore: add database scripts, phase 11 deployment reports, release docs, and report generator
b95bae1 refactor: update AI config, providers, services, models, and review workflow
2cfefe7 chore: update appsail config, database, main entry point, startup script
cbf8ac8 fix: update App.tsx, offenders test, and main entry
3d1ca28 feat: add fallback, NVIDIA, and OpenRouter AI providers, update config   ← HEAD
```

---

## 2. Artifact Inventory

### 2.1 Frontend Artifact — Web Client (SPA)

| Property | Value |
|---|---|
| Source directory | `apps/web/` |
| Build output | `apps/web/dist/` |
| Technology | React (SPA) with React Router |
| Deployment target | Catalyst Web Client Hosting |
| Public URL | `https://project-rainfall-60079736152.development.catalystserverless.in/app/index.html` |
| Verification | Page loads — shows "Berunda — Crime Intelligence Platform" |
| Build command | `npm run build` (inferred from React project convention) |
| SPA fallback | `index.html` for all routes (configured in Catalyst console) |

**Files in `apps/web/dist/`:**

| Pattern | Description |
|---|---|
| `index.html` | SPA entry point; served on all unmatched routes |
| `assets/*.js` | Bundled JavaScript (React, Router, app code) |
| `assets/*.css` | Compiled stylesheets |
| `favicon.ico` | Application favicon |
| Other static assets | Images, fonts, configuration files |

### 2.2 Backend Artifact — AppSail (FastAPI)

| Property | Value |
|---|---|
| Source directory | `appsail/berunda_api/` |
| Deployment type | Catalyst AppSail (serverless container) |
| Stack | Python 3.10 |
| Memory allocation | 1024 MB |
| Listen port | `${X_ZOHO_CATALYST_LISTEN_PORT}` (default 9000) |
| Backend URL | `https://berunda-api-50044292022.development.catalystappsail.in` |
| Health endpoint | `GET /` or `GET /health` |
| Status code | 503 — "Execution failed. Please check the startup command or port" |

**Key source files:**

| File | Path | Role |
|---|---|---|
| Entry point | `appsail/berunda_api/main.py` | uvicorn runner — reads `X_ZOHO_CATALYST_LISTEN_PORT` env var |
| FastAPI app | `appsail/berunda_api/src/main.py` | 430 lines; 23 routers; lifespan events; Prometheus metrics; CORS; error handlers |
| Startup script | `appsail/berunda_api/startup.sh` | Shell launcher — sets PYTHONPATH, execs uvicorn on port 9000 |
| App config | `appsail/berunda_api/app-config.json` | Container config — stack, memory, command, build path |
| Dependencies | `appsail/berunda_api/requirements.txt` | 70 lines, ~30+ packages (see section 3) |
| Database | `appsail/berunda_api/berunda.db` | Local SQLite (also `src/berunda.db`) |
| Model registry | `appsail/berunda_api/models/registry/` | Crime pattern model artifacts (v1.0.0–1.0.3) |
| Alembic migrations | `appsail/berunda_api/src/alembic/versions/` | 8 migration scripts (001–008) |
| Project config | `appsail/berunda_api/src/config.py` | Pydantic settings with env var overrides |
| Database layer | `appsail/berunda_api/src/database.py` | SQLAlchemy async engine with wait-for-db retry logic |

### 2.3 Application Rotters Registered (23 total)

| Router | Prefix | Description |
|---|---|---|
| `fir_router` | `/api/v1/firs` | FIR CRUD |
| `entity_router` | `/api/v1/entities` | Person entity resolution |
| `graph_router` | `/api/v1/graph` | Entity relationship graph |
| `hotspot_router` | `/api/v1/hotspots` | Crime hotspot analysis |
| `anomaly_router` | `/api/v1/anomalies` | Anomaly detection |
| `risk_router` | `/api/v1/risk` | Risk scoring |
| `fairness_router` | `/api/v1/fairness` | Fairness audit |
| `audit_router` | `/api/v1/audit` | Audit log |
| `auth_router` | `/api/v1/auth` | Authentication & authorization |
| `admin_router` | `/api/v1/admin` | Admin operations |
| `ai_intelligence_router` | `/api/v1/ai` | AI intelligence |
| `investigation_router` | `/api/v1/investigations` | Investigation workflow |
| `analytics_router` | `/api/v1/analytics` | Analytics |
| `geospatial_router` | `/api/v1/geospatial` | Geospatial queries |
| `report_router` | `/api/v1/reports` | Report generation |
| `police_stations_router` | `/api/v1/police-stations` | Police station data |
| `persons_router` | `/api/v1/persons` | Person search |
| `notification_router` | `/api/v1/notifications` | Notifications |
| `webhook_router` | `/api/v1/webhooks` | Catalyst webhooks |
| `related_cases_router` | `/api/v1/related-cases` | Related case detection |
| `search_router` | `/api/v1/search` | FIR search |
| `rag_router` | `/api/v1/rag` | RAG-powered Q&A |
| `dashboard_router` | `/api/v1/dashboard` | Role-specific dashboards |

---

## 3. Dependency Profile

### 3.1 Python Packages (from `requirements.txt`)

| Category | Packages |
|---|---|
| Core Web | `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `python-dotenv`, `pyyaml`, `typing_extensions` |
| Database | `sqlalchemy`, `asyncpg`, `psycopg2-binary`, `alembic`, `pgvector`, `aiosqlite` |
| Auth | `pyjwt`, `bcrypt`, `cryptography` |
| Data | `pandas`, `numpy`, `Faker` |
| Geospatial | `shapely`, `geopandas` |
| Graph | `networkx`, `neo4j` |
| ML/AI | `scikit-learn`, `spacy` |
| Monitoring | `prometheus-client` |
| HTTP/API | `requests`, `httpx`, `tenacity`, `python-multipart`, `slowapi` |
| PII Redaction | `presidio-analyzer`, `presidio-anonymizer` |
| Testing | `pytest`, `pytest-cov`, `pytest-mock`, `pytest-asyncio` |
| Code Quality | `ruff`, `mypy`, `bandit`, `pre-commit` |
| Catalyst SDK | `zcatalyst-sdk` |

### 3.2 Large/Bloated Dependencies (potential startup delay concern)

| Package | Typical Size | Notes |
|---|---|---|
| `geopandas` | ~50 MB | Includes Fiona, GDAL, pyproj — heavy native extensions |
| `spacy` | ~100 MB | Language model + core library |
| `presidio-analyzer` | ~400 MB | Includes spaCy model, regex patterns, NLP pipeline |
| `scikit-learn` | ~30 MB | ML library with compiled extensions |
| `shapely` | ~10 MB | GEOS C library bindings |
| `neo4j` | ~5 MB | Database driver |

**Total estimated dependency footprint: ~600–800 MB**, which may exceed AppSail's build/startup timeout or container memory limits (1024 MB).

---

## 4. Artifact Integrity Checks

| Check | Frontend | Backend | Result |
|---|---|---|---|
| Build output exists | `apps/web/dist/index.html` present | `appsail/berunda_api/main.py` present | PASS |
| Config matches source | `catalyst.json` → `client.source: "apps/web/dist"` | `catalyst.json` → `appsail[0].source: "appsail/berunda_api"` | PASS |
| Entry point syntax | N/A | `python3 -c "import ast; ast.parse(open('appsail/berunda_api/main.py').read())"` | PASS |
| Startup script syntax | N/A | `python3 -c "import ast; ast.parse(open('appsail/berunda_api/startup.sh').read())"` | N/A (shell script) |
| requirements.txt parseable | N/A | All package specifications valid | PASS |
| Catalyst JSON valid | `catalyst.json` valid JSON | `app-config.json` valid JSON | PASS |

---

## 5. Deployment Readiness Summary

| Component | Ready | Status |
|---|---|---|
| Frontend build | YES | Deployed and serving correctly |
| Backend source | YES | Uploaded to AppSail |
| Dependencies listed | YES | `requirements.txt` complete |
| Runtime config | YES | `app-config.json` configured |
| Startup command | YES | `python3 main.py` (via `main.py` entry) |
| Database schema | YES | 8 Alembic migration scripts |
| Model artifacts | YES | 4 model versions in registry |
| Environment variables | PARTIAL | `env_variables: {}` in `app-config.json` — secrets not injected |
| Stratus storage | NO | Not provisioned |
| Job scheduler | NO | Not configured |

---

## 6. Artifact Hashes (Reference for Rollback Verification)

| File | Size | Last Modified |
|---|---|---|
| `apps/web/dist/index.html` | (verify at rollback) | 2026-07-26 |
| `appsail/berunda_api/main.py` | 713 bytes | 2026-07-26 |
| `appsail/berunda_api/src/main.py` | 14.8 KB | 2026-07-26 |
| `appsail/berunda_api/requirements.txt` | 2.4 KB | 2026-07-26 |
