# Architectural Assumptions — Project Berunda

> **Document ID:** BERUNDA-ASSUMPTIONS-001 | **Version:** 1.0
> **Last Updated:** 2026-07-23

## Purpose
This document records assumptions made during the enterprise database and AI implementation where project documentation was silent or ambiguous.

---

## A1 — Database Engine
**Assumption:** PostgreSQL 16 is the production database. SQLite may be used for local development with feature parity maintained via dialect-agnostic SQLAlchemy.
**Rationale:** `docker-compose.yml` specifies `postgres:16-alpine`; `requirements.txt` includes `asyncpg` and `psycopg2-binary`.

## A2 — Single-Tenant with District Scoping
**Assumption:** The platform is single-tenant (one KSP deployment) but data access is scoped by `DistrictID` for jurisdiction isolation. There is no multi-organization tenant model.
**Rationale:** The KSP schema uses `District` and `Unit` hierarchies, not organization-level separation.

## A3 — No Real PII in Development
**Assumption:** All development and testing uses synthetic data only. Real PII is never stored in development databases.
**Rationale:** AGENTS.md safety rule #4 explicitly prohibits real PII.

## A4 — Caste/Religion Fields Exist but Are Excluded from ML
**Assumption:** `CasteID` and `ReligionID` columns exist in the schema for statutory reporting compliance (SC/ST Act) but are hard-excluded from all predictive models, risk scoring, and entity resolution features.
**Rationale:** NotebookLM research and AGENTS.md both mandate this constraint.

## A5 — AI Provider Strategy
**Assumption:** The platform supports multiple LLM providers via a common provider abstraction (`src/ai/providers/`). OpenAI is the primary configured provider; Groq is an optional alternative. MockProvider is the fallback for offline/testing with no API key. Sarvam AI for Kannada NLP is a Phase 2 addition.
**Rationale:** Provider abstraction allows switching between OpenAI, Groq, and Mock without code changes. OpenAI is listed first in `.env.example` as the most widely available; Groq offers a free OpenAI-compatible alternative.

## A6 — Embedding Strategy
**Assumption:** Embeddings use a lightweight model compatible with the chosen provider. For the MVP, we use deterministic TF-IDF with an upgrade path to dense embeddings.
**Rationale:** Dense embedding providers require API keys; TF-IDF works offline.

## A7 — Authentication
**Assumption:** JWT-based authentication with bcrypt password hashing. No SSO or OAuth in MVP. Users are created via seed scripts or admin API.
**Rationale:** Current implementation uses JWT; no SSO infrastructure exists.

## A8 — Connection Pooling
**Assumption:** Production uses connection pooling with `pool_size=5`, `max_overflow=10`. Development may use `NullPool` or smaller pools.
**Rationale:** `NullPool` in current code is unsuitable for production load.

## A9 — Audit Log Immutability
**Assumption:** Audit log records are append-only. No UPDATE or DELETE operations are permitted on `gov_AuditLog`.
**Rationale:** Enterprise audit compliance requires immutable audit trails.

## A10 — Migration Safety
**Assumption:** All migrations are forward-only in production. Rollback scripts exist for emergency use but are not part of normal deployment.
**Rationale:** Standard enterprise migration practice for data-bearing tables.
