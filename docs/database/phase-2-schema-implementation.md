# Phase 2 — Schema Implementation

> **Document ID:** BERUNDA-DB-002 | **Version:** 1.0 | **Status:** APPROVED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## Schema Overview

The database uses three logical schemas with table prefixes:

| Prefix | Schema | Purpose |
|--------|--------|---------|
| `src_` | Source | FIR ERD tables — core case data |
| `int_` | Intelligence | Berunda extension tables — analytics |
| `gov_` | Governance | Audit, fairness, provenance |
| `auth_` | Authentication | Users, sessions, permissions |

## Core Tables for Vertical Slice

### src_CaseMaster

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| CaseMasterID | INTEGER | PK, AUTOINCREMENT | Primary key |
| CrimeNo | VARCHAR(100) | UNIQUE | Crime/FIR number |
| CaseNo | VARCHAR(100) | | Case number |
| CrimeRegisteredDate | DATETIME | | Date FIR registered |
| PolicePersonID | INTEGER | FK → src_Employee | Investigating officer |
| PoliceStationID | INTEGER | FK → src_Unit | Police station |
| CaseCategoryID | INTEGER | FK → src_CaseCategory | FIR/UDR/PAR type |
| GravityOffenceID | INTEGER | FK → src_GravityOffence | Heinous/Non-heinous |
| CrimeMajorHeadID | INTEGER | FK → src_CrimeHead | Primary crime type |
| CrimeMinorHeadID | INTEGER | FK → src_CrimeSubHead | Sub-type |
| CaseStatusID | INTEGER | FK → src_CaseStatusMaster | Current status |
| CourtID | INTEGER | FK → src_Court | Assigned court |
| IncidentFromDate | DATETIME | | Incident start |
| IncidentToDate | DATETIME | | Incident end |

### src_Inv_OccuranceTime

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| CaseMasterID | INTEGER | PK, FK → src_CaseMaster | Linked case |
| IncidentFromDate | DATETIME | | Start time |
| IncidentToDate | DATETIME | | End time |
| InfoReceivedPSDate | DATETIME | | When police notified |
| Latitude | FLOAT | | Crime location lat |
| Longitude | FLOAT | | Crime location lng |
| BriefFacts | TEXT | | Narrative description |

### auth_User

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| UserID | INTEGER | PK, AUTOINCREMENT | Primary key |
| Email | VARCHAR(255) | UNIQUE, NOT NULL | Login email |
| HashedPassword | VARCHAR(255) | NOT NULL | bcrypt hash |
| Role | VARCHAR(50) | NOT NULL | admin/officer/analyst |
| DistrictID | INTEGER | FK → src_District | Jurisdiction |
| IsActive | BOOLEAN | DEFAULT true | Account enabled |

### auth_Session

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| SessionID | INTEGER | PK, AUTOINCREMENT | Primary key |
| UserID | INTEGER | FK → auth_User | Owning user |
| TokenHash | VARCHAR(255) | UNIQUE, NOT NULL | Refresh token hash |
| ExpiresAt | DATETIME | NOT NULL | Expiry timestamp |
| RevokedAt | DATETIME | NULLABLE | Revocation timestamp |

## Indexes

| Table | Index | Type | Rationale |
|-------|-------|------|-----------|
| CaseMaster | (CrimeMajorHeadID, CrimeRegisteredDate, PoliceStationID) | Composite B-tree | Analytics queries |
| CaseMaster | (CrimeNo) | UNIQUE B-tree | Duplicate detection |
| auth_User | (Email) | UNIQUE B-tree | Login lookup |
| auth_Session | (TokenHash) | UNIQUE B-tree | Refresh validation |

## Migration Chain

| Migration | Description |
|-----------|-------------|
| 001_initial_schema | All model tables |
| 002_seed_demo_data | Reference and demo data |
| 003_add_constraints_and_indexes | FK constraints, indexes |
| 004_auth_tables | User, Session, Permission |
| 005_ai_tables | AI usage tracking |
| 006_seed_users | Admin/analyst seed accounts |

## Transaction Boundaries

| Operation | Scope | Isolation |
|-----------|-------|-----------|
| Create FIR | Single transaction | READ COMMITTED |
| List FIRs | Read-only | READ COMMITTED |
| Get FIR detail | Read-only | READ COMMITTED |
| Login | Single transaction | READ COMMITTED |
| Register | Single transaction | READ COMMITTED |
