# 03 - Database Migration Plan

## Context and Current State
The application currently uses SQLAlchemy ORM and direct SQL database URLs (`aiosqlite`, `asyncpg`, `aiomysql`). 
Per current Zoho Catalyst documentation, **Catalyst Data Store** is a fully managed, serverless relational database that uses **ZCQL (Zoho Catalyst Query Language)** and is accessed via the Catalyst SDK, not via standard MySQL/PostgreSQL connection strings.

Therefore, the use of `aiomysql`, `asyncpg`, and a traditional `DATABASE_URL` is **Unsupported** and **Unnecessary** for production deployment on Catalyst Data Store.

## Migration Strategy

### 1. Abstracting the Data Layer
We will implement a Repository pattern to decouple the FastAPI routes from the underlying database implementation.

```text
API Route
    ↓
Application Service
    ↓
Repository Interface (Abstract Base Class)
    ├── CatalystDataStoreAdapter (Production)
    └── LocalMemoryAdapter (Local/Testing)
```

### 2. Catalyst Data Store Schema Provisioning
Catalyst Data Store tables are typically created via the Catalyst Console, CLI, or API, rather than traditional Alembic migrations.

**Migration Automation**:
We will create a script `scripts/deploy_catalyst_schema.py` that uses the Catalyst Python SDK to automate the creation of tables and columns defined in our target data model (`02-target-data-model.md`).

### 3. Data Ingestion (Legacy SQLite to Catalyst)
We will create `scripts/import_legacy_data.py` to:
1. Read existing `.db` (SQLite) or CSV data.
2. Validate the data (handle nulls, dates to IST).
3. Insert into Catalyst Data Store using the SDK in batch operations.
4. Support `--dry-run` and provide reconciliation reporting.

## Action Plan
1. **Remove Unsupported Dependencies**: Remove `aiomysql`, `asyncpg`, `alembic`, and `SQLAlchemy` from `requirements.txt` (or keep SQLAlchemy only if we use it for a local SQLite testing adapter, but a LocalMemoryAdapter or explicit Catalyst Mock is safer to ensure ZCQL parity).
2. **Implement Repositories**: Create `src/repositories/base.py`, `src/repositories/catalyst_adapter.py`.
3. **Refactor Routes**: Update `src/routers/*.py` to use the injected repository instances instead of SQLAlchemy `AsyncSession`.
4. **Data Import Pipeline**: Implement the import scripts to migrate any existing local SQLite data to Catalyst.
