# 03 Database Migration Plan

The Berunda project is abandoning SQLAlchemy's automated Alembic migrations for production Catalyst deployments because Catalyst Data Store does not support standard external Data Definition Language (DDL) execution via standard JDBC/ODBC or SQLAlchemy dialects.

## Migration Strategy

### 1. Schema Definition & Generation
- The schema is managed declaratively via `CATALYST_DATASTORE_SCHEMA_MAPPING.md`.
- Migrations (adding tables, dropping columns) are executed via internal Catalyst APIs using the script `scripts/database/deploy_schema_all.py` injected through an authenticated session or headless browser to bypass CLI DDL constraints.

### 2. Data Seeding & Synthetic Data Import
- The repository contains synthetic CSV records inside `data/seed/` and JSON records in `data/synthetic/`.
- **Import Strategy**: We will utilize a Python script running locally that acts as a bridge. It parses the CSVs, validates their structure against the Pydantic schemas, and iteratively calls the `POST /baas/v1/project/{project}/table/{table}/row` endpoint using the `zcatalyst_sdk` to insert the records.
- **Idempotency**: Import scripts will check for existing records (e.g., querying `CrimeNo`) before insertion to prevent duplicate data issues during retries.
- **Relationships**: Parent tables (e.g. `CaseMaster`) must be seeded before child tables (e.g. `Accused`). The bridge script caches the Catalyst `ROWID` responses of parent records and injects them into the dependent child records.

### 3. Local Development Parity
- Local development will continue to use SQLite via `src/repositories/local_adapter.py`. 
- An Alembic environment (`src/alembic/`) exists exclusively for bootstrapping the local SQLite database.

## Rollback Plan
- Since Catalyst Data Store does not support atomic DDL transactions, schema rollbacks require explicit `DELETE` or `DROP COLUMN` API calls.
- Deletion of records during failed seed processes should be handled by truncating the table or selectively deleting the failed batch.
