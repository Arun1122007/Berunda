# Database Audit Report — Project Berunda

> **Document ID:** BERUNDA-DB-AUDIT-001 | **Version:** 1.0
> **Auditor:** Antigravity AI | **Date:** 2026-07-23

---

## 1. Scope
Full audit of the database layer: ORM models (`src/models/`), migrations (`src/alembic/versions/`), database configuration (`src/database.py`), services (`src/services/`), and API routers (`src/routers/`).

---

## 2. Findings

### 🔴 CRITICAL

#### C1 — No Foreign Key Constraints in Migration
- **Problem:** Migration `001_initial_schema.py` creates all tables without `sa.ForeignKey()` references. FK columns exist as plain integers.
- **Impact:** No referential integrity at the database level. Orphaned records can be created freely.
- **Files:** `src/alembic/versions/001_initial_schema.py`
- **Solution:** Create migration `003` adding all FK constraints via `ALTER TABLE`.
- **Status:** 🔧 Fix in Phase 2

#### C2 — Hardcoded Users with Plaintext Passwords
- **Problem:** `auth_router.py` uses an in-memory Python dict with plaintext passwords (`"admin"`, `"analyst"`).
- **Impact:** No persistent user management; passwords exposed in source code.
- **Files:** `src/routers/auth_router.py`
- **Solution:** Create `User` model with bcrypt-hashed passwords; move to database-backed auth.
- **Status:** 🔧 Fix in Phase 5

#### C3 — No Database Indexes
- **Problem:** Neither the ORM models nor migrations define any indexes (not even on FK columns).
- **Impact:** All JOIN and WHERE queries perform full table scans. Catastrophic for production with >100K records.
- **Files:** `src/models/src_models.py`, `int_models.py`, migration `001`
- **Solution:** Add indexes on all FK columns, `CrimeNo`, `CrimeRegisteredDate`, and composite indexes for common query patterns.
- **Status:** 🔧 Fix in Phase 2

---

### 🟠 HIGH

#### H1 — RAG Uses TF-IDF Instead of Vector Embeddings
- **Problem:** `rag_service.py` builds a TF-IDF matrix on every query. No persistent vector storage.
- **Impact:** Poor semantic search quality; no support for Kannada text; O(n) rebuild cost per query.
- **Files:** `src/services/rag_service.py`
- **Solution:** Upgrade to provider-based embeddings with persistent vector storage.
- **Status:** 🔧 Fix in Phase 9

#### H2 — AI Providers Are Stubs
- **Problem:** `CatalystProvider` and `OpenAICompatibleProvider` return hardcoded strings like `"[Catalyst] Response for: ..."`.
- **Impact:** No actual AI inference capability.
- **Files:** `src/ai/providers/__init__.py`, `openai.py`, `catalyst.py`
- **Solution:** Implement real HTTP calls to Groq/OpenAI-compatible APIs.
- **Status:** 🔧 Fix in Phase 7

#### H3 — No AI Usage or Cost Tracking
- **Problem:** No tables or services for tracking AI API calls, token consumption, or costs.
- **Impact:** Uncontrolled API spend; no observability into AI usage.
- **Solution:** Create `AIUsageRecord` model and tracking service.
- **Status:** 🔧 Fix in Phase 8

#### H4 — No District-Scoped Query Isolation
- **Problem:** Service layer queries do not filter by the authenticated user's `DistrictID`.
- **Impact:** Any authenticated user can access any district's data.
- **Files:** All service files in `src/services/`
- **Solution:** Add district scoping to all data-access methods based on JWT claims.
- **Status:** 🔧 Fix in Phase 5

---

### 🟡 MEDIUM

#### M1 — ORM-Migration Type Drift
- **Problem:** ORM models use `BigInteger` for `AuditLog.AuditLogID` but migration uses `Integer`. `Embedding` column is `LargeBinary` in ORM but `Text` in migration.
- **Impact:** Schema inconsistency; potential data truncation.
- **Files:** `src/models/gov_models.py`, `int_models.py`, migration `001`
- **Solution:** Align ORM types with migration types; use `Text` for embedding storage.
- **Status:** 🔧 Fix in Phase 3

#### M2 — No Timestamp Defaults
- **Problem:** `CreatedAt`/`UpdatedAt` columns have no `server_default` or `onupdate` triggers.
- **Impact:** Application code must manually set timestamps; missed timestamps create audit gaps.
- **Files:** All model files
- **Solution:** Add `server_default=func.now()` and `onupdate=func.now()`.
- **Status:** 🔧 Fix in Phase 3

#### M3 — NullPool in Production
- **Problem:** `database.py` uses `NullPool` which creates a new connection for every request.
- **Impact:** Connection exhaustion under concurrent load; high latency.
- **Files:** `src/database.py`
- **Solution:** Use `AsyncAdaptedQueuePool` with configurable pool size.
- **Status:** 🔧 Fix in Phase 4

#### M4 — Seed Data in Migration File
- **Problem:** `002_seed_demo_data.py` inserts demo data as a migration. This runs in production.
- **Impact:** Test data pollutes production databases.
- **Files:** `src/alembic/versions/002_seed_demo_data.py`
- **Solution:** Move seed data to a separate script; gate migration behind `APP_ENV` check.
- **Status:** 📋 Noted for future

---

### 🟢 LOW

#### L1 — No Soft Delete Support
- **Problem:** No `deleted_at` column or soft-delete pattern on any model.
- **Impact:** Deleted records are permanently lost; no recovery possible.
- **Solution:** Add `deleted_at` to key tables in a future phase.
- **Status:** 📋 Deferred

#### L2 — No Database Backup Documentation
- **Problem:** No backup/recovery documentation exists.
- **Solution:** Create `docs/database/BACKUP_AND_RECOVERY.md`.
- **Status:** 🔧 Fix in Phase 12
