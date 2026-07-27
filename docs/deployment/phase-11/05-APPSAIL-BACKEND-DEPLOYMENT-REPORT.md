# Phase 11: AppSail Backend Deployment Report

**Document ID:** BERUNDA-PHASE11-05
**Status:** DEPLOYED WITH ISSUES
**Date:** 2026-07-27

---

## Deployment Details

| Property | Value |
|---|---|
| Component | `berunda-api` |
| Environment | Catalyst AppSail Development |
| Deployment Status | DEPLOYED WITH ISSUES |
| URL | `https://berunda-api-50044292022.development.catalystappsail.in` |
| Health Check Response | HTTP 503 — "Execution failed. Please check the startup command or port" |
| Latest Attempt | 2026-07-27 |
| Git Commit | `3d1ca28` |

---

## Configuration (from `catalyst.json` + `app-config.json`)

| Setting | Value | Source |
|---|---|---|
| Stack | Python 3.10 | `app-config.json` |
| Build Path | `.` (resolves to `appsail/berunda_api/`) | `app-config.json` |
| Memory | 1024 MB | `app-config.json` |
| Command | `sh -c 'python3 -m uvicorn src.main:app --host 0.0.0.0 --port ${X_ZOHO_CATALYST_LISTEN_PORT}'` | `app-config.json` |
| Listen Port | `X_ZOHO_CATALYST_LISTEN_PORT` env var (default 9000) | Catalyst runtime |
| Env Variables | `{}` (none configured) | `app-config.json` |
| Source | `appsail/berunda_api` | `catalyst.json` |

---

## Root Cause Analysis — 503 Error

### Symptom
```
HTTP GET https://berunda-api-50044292022.development.catalystappsail.in/
→ 503 Service Unavailable
→ Body: "Execution failed. Please check the startup command or port"
```

### Primary Suspects (ranked by likelihood)

| Rank | Suspect | Reasoning | Investigation Method |
|---|---|---|---|
| 1 | **Heavy dependency installation timeout** | `requirements.txt` includes `geopandas` (~50 MB), `spacy` (~100 MB), `presidio-analyzer` (~400 MB), `scikit-learn` (~30 MB), `shapely` (~10 MB) — total estimated ~600–800 MB. AppSail build phase may time out or exceed container startup window. | Review AppSail build logs via Console UI |
| 2 | **Port mismatch** | `app-config.json` uses `${X_ZOHO_CATALYST_LISTEN_PORT}` (Catalyst default). `startup.sh` hardcodes `PORT=9000` as fallback. `main.py` reads `X_ZOHO_CATALYST_LISTEN_PORT` then `PORT` then defaults to 9000. If Catalyst runtime injects a different port variable name, binding fails. | Check Catalyst AppSail runtime documentation for port injection variable name |
| 3 | **Entry point mismatch** | `catalyst.json` declares no explicit `command` for `appsail[0]`. `app-config.json` sets `command` to `sh -c 'python3 -m uvicorn src.main:app ...'`. However, Catalyst CLI may use `main.py` (the file at root) as default entry. The root `main.py` does `from src.main import app` then `uvicorn.run(app)`. If CLI calls `main.py` directly, but `app-config.json` overrides with inline command, there could be confusion. | Verify which entry Catalyst actually invokes |
| 4 | **Missing native system dependencies** | `geopandas` requires GDAL/Fiona C libraries; `spacy` requires C++ build tools; `psycopg2-binary` requires libpq. AppSail's Python 3.10 base image may lack these. | Check if Catalyst AppSail Python 3.10 image includes system libs for geospatial processing |
| 5 | **Memory exhaustion during startup** | 1024 MB memory limit. Loading `spacy` model + `presidio-analyzer` + `scikit-learn` + `pandas` simultaneously may exceed available memory during `import` phase. | Monitor memory metrics during startup |
| 6 | **Alembic migration failure** | The `lifespan` handler in `src/main.py` calls `wait_for_db()` which attempts to connect to Catalyst Data Store via `asyncpg` or `aiosqlite`. If the database connection string is not configured (no env vars), the app may crash during startup. | Check if Catalyst Data Store requires a specific connection string |
| 7 | **Python version incompatibility** | `app-config.json` specifies `python_3_10`. Some packages (e.g., `pydantic-settings>=2.6.0`, `fastapi>=0.115.0`) may require Python 3.11+ features. | Verify minimum Python version for each package |

### Dependency Size Breakdown

| Package | Approximate Size | Native Extensions |
|---|---|---|
| `geopandas` | ~50 MB | GDAL, Fiona, pyproj |
| `spacy` | ~100 MB | Thinc, blis |
| `presidio-analyzer` | ~400 MB | spaCy model, regex, NLP |
| `scikit-learn` | ~30 MB | Cython extensions |
| `shapely` | ~10 MB | GEOS C library |
| `pandas` | ~20 MB | Cython extensions |
| `numpy` | ~30 MB | C/Fortran extensions |
| `psycopg2-binary` | ~5 MB | libpq |
| `aiosqlite` | ~0.5 MB | Pure Python |
| All others | ~20 MB | Pure Python |
| **Total** | **~665–800 MB** | |

---

## Troubleshooting Steps Attempted

| # | Step | Command / Action | Outcome |
|---|---|---|---|
| T-01 | Verified Catalyst CLI auth | `catalyst --version` | v1.27.0, authenticated as arun1122007@gmail.com |
| T-02 | Checked `catalyst.json` syntax | JSON parse | Valid |
| T-03 | Checked `app-config.json` syntax | JSON parse | Valid |
| T-04 | Verified Python entry point syntax | `python3 -c "import ast; ast.parse(open('appsail/berunda_api/main.py').read())"` | Valid |
| T-05 | Verified `requirements.txt` format | `pip install --dry-run -r requirements.txt` | All packages resolvable |
| T-06 | Tested local uvicorn startup | `cd appsail/berunda_api && python3 main.py` | Starts on localhost:9000 |
| T-07 | Inspected root `main.py` port logic | Lines 7-17 | Falls back to 9000 if no env var set |
| T-08 | Inspected `startup.sh` port logic | Line 3 | Defaults to 9000 |
| T-09 | Cross-checked `app-config.json` command | Uses `${X_ZOHO_CATALYST_LISTEN_PORT}` | Matches Catalyst convention |
| T-10 | Checked Catalyst Data Store connectivity | N/A (no direct CLI test) | Requires live env |
| T-11 | Tested backend URL via browser | `curl https://berunda-api-50044292022.development.catalystappsail.in/` | 503 |
| T-12 | Checked if alternative port (8000) needed | Reviewed Catalyst docs | Default Catalyst port is 9000 via `X_ZOHO_CATALYST_LISTEN_PORT` |

---

## Next Steps

1. **Access Catalyst Console UI** — Navigate to AppSail → berunda-api → Logs / Monitoring to view container startup logs and pinpoint the exact failure (dependency install timeout, command not found, import error, or port bind failure).
2. **Right-size dependencies** — Remove `geopandas` (currently unused — no GeoDataFrame operations in codebase), `presidio-analyzer`/`presidio-anonymizer` (PII redaction not called in critical path), `neo4j` driver (Neo4j not provisioned), and `spacy` (model not downloaded) to reduce build payload.
3. **Simplify startup command** — Use `python3 main.py` in `app-config.json` instead of `sh -c '...'` wrapper for simpler debugging.
4. **Add health check endpoint** — Verify `GET /` and `GET /health` return 200 with proper response.
5. **Configure environment variables** — Set `APP_ENV=production`, `DATABASE_URL`, and other required variables in `app-config.json`.
6. **Consider pip `--no-deps` or pre-built wheels** — If AppSail build environment lacks system libraries for geospatial dependencies, replace with lightweight alternatives or use pre-compiled wheels.

---

## Rollback Instructions

If the 503 cannot be resolved:

1. **Revert `catalyst.json` / `app-config.json`** to last known good configuration.
2. **Downgrade commit** — `git reset --hard <previous-working-commit>` (e.g., `cbf8ac8`) and redeploy.
3. **Use local development** — Run backend on localhost:9000 and reconfigure frontend to proxy API calls.
4. **File defect** — Log issue in `09-PHASE-11-DEPLOYMENT-DEFECT-REGISTER.md` as P11DEP-BLK-001.
