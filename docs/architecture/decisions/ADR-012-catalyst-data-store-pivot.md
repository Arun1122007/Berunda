# ADR 012: Pivot to Zoho Catalyst Data Store

## Context

Project Berunda initially designed its database architecture around a standalone PostgreSQL database with SQLAlchemy as the ORM, optimized with Connection Pools and Alembic migrations. However, a strict requirement of the Hack2Skill Datathon is to utilize **Zoho Catalyst** as the mandatory hosting and backend platform.

Catalyst provides its own relational database service known as **Catalyst Data Store**. Retaining a standalone PostgreSQL database would violate the core platform constraint and risk disqualification.

## Decision

We will pivot the entire data persistence layer to **Zoho Catalyst Data Store**.

1.  **Schema Design**: The tables designed for PostgreSQL (e.g., `CaseMaster`, `PersonEntity`, `RiskScore`) will be mapped 1:1 to Catalyst Data Store tables.
2.  **Query Language**: We will replace SQLAlchemy ORM with Zoho Catalyst Query Language (ZCQL) executed via the `zcatalyst-sdk-node` in our API functions.
3.  **Authentication**: We will drop the custom `auth_User` and `auth_Session` tables and rely natively on Catalyst Authentication.
4.  **Migrations**: Catalyst Data Store schemas will be provisioned directly via the Catalyst CLI or console, dropping the need for Alembic.

## Consequences

### Positive
- **Compliance**: Ensures full compliance with the Hack2Skill Catalyst mandate.
- **Simplicity**: Removes the need to manage database infrastructure, connection pools, and migration scripts.
- **Integration**: Seamlessly integrates with Catalyst Functions and Authentication.

### Negative
- **ORM Loss**: We lose the strict compile-time safety and advanced features of SQLAlchemy.
- **Refactoring**: All backend API endpoints must be rewritten from Python/SQLAlchemy to Node.js/ZCQL.
- **Transaction Limits**: We must manage complex distributed transactions at the application level as ZCQL does not natively support long-running, multi-statement transactions in the same way PostgreSQL does.

## Status

**APPROVED**

## References

- `docs/database/DATABASE_ARCHITECTURE.md` (Updated)
- `docs/restructuring-report.md` (Refactoring roadmap)
