# 00 - Repository Baseline

## Canonical Application Structure

**Real Repository Root**: `D:\Hack2Skill\Berunda`

**Active Frontend**: `apps/web` (React + Vite)
- This is the canonical modern web frontend.

**Active Backend**: `src` (FastAPI)
- The canonical backend code lives here. It is configured to be copied and deployed via Catalyst AppSail.

**Duplicate / Obsolete Applications**:
- `Drishti-Crime-Viz`: This directory appears to be an older Replit workspace and contains duplicate or stale code. Currently, `catalyst.json` points to `Drishti-Crime-Viz/dist` as the client source. This is a misconfiguration and must be updated to point to `apps/web/dist` (or wherever the Vite app builds).
- `apps/api`: Contains Node.js functions (e.g. `fir-ingestion`, `ner-extraction`) wrapped for Catalyst CLI. However, the FastAPI backend in `src` seems to be the primary backend target. We must consolidate AI features to ensure they run inside the FastAPI service or are deployed as correct Catalyst functions.

**Database Configuration**:
- Active database configuration is in `src/database.py`, using SQLAlchemy with `sqlite+aiosqlite://` locally and falling back to PostgreSQL/MySQL depending on `DATABASE_URL`. This must be updated to target Catalyst Data Store.

**AI Modules Reachability**:
- AI routes exist in `src/routers/rag_router.py` (and potentially others). They likely rely on `src/ai/providers` which are currently configured using `.env.example` keys for OpenAI.

**Environment Files**:
- `.env` and `.env.example` at the root.

## Next Steps
- Update `catalyst.json` to point `client.source` to the `apps/web` build output.
- Refactor the backend to rely solely on Catalyst Data Store.
