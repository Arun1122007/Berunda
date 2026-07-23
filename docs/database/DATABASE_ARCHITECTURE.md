# Database Architecture and Design

## Overview
Berunda employs an enterprise-grade async PostgreSQL database architecture partitioned into core schemas: `src_`, `int_`, and `gov_`, alongside `auth_` for access control.

## Schemas

### 1. `src_` (Source Data)
Contains ground-truth tables mirroring KSP FIR schemas (e.g., `src_CaseMaster`, `src_Employee`).
- Hardened with explicit Foreign Key constraints to maintain referential integrity.
- Indexed appropriately for analytical queries on dates, locations, and categorical identifiers.

### 2. `int_` (Intelligence & AI)
Supports AI workflows, embeddings, risk scoring, and geospatial indexing.
- `int_RAGCorpusChunk`: Stores pre-computed embeddings serialized as JSON.
- `int_RiskScore` / `int_AnomalyAlert`: AI model outputs. Range constraints (`0.0 - 1.0`) guarantee valid statistical downstream inputs.

### 3. `gov_` (Governance)
Audit trails, fairness logs, and provenance tracking.
- `gov_AuditLog`: Captures every sensitive action, linking IP, user, action, and correlation IDs.
- `gov_FairnessCheckResult`: Logs AI guardrail failures (e.g., demographic bias detections) with timestamp defaults.

### 4. `auth_` (Authentication)
- `auth_User`: Stores users with bcrypt password hashes and RBAC roles.
- `auth_Session`: Manages stateful token lifecycles and revocation.

## Key Enterprise Enhancements
- **Connection Pooling**: `AsyncAdaptedQueuePool` utilized with `pool_size=5`, `max_overflow=10`, and `pool_pre_ping=True` for high availability.
- **Constraints & Validation**: Server-side defaults (`func.now()`), composite indexes, and value range constraints enforced natively via Alembic migrations.
