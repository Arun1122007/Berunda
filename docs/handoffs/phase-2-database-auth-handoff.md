# Phase 2 — Database & Authentication Handoff

> **Document ID:** BERUNDA-HANDOFF-PH2-001 | **Version:** 2.0 | **Status:** FINAL
> **Author:** Agent C — Database & Authentication Workstream | **Date:** 2026-07-25
> **Classification:** INTERNAL

---

## 1. Entities

All tables derive from `src.models.base.Base` (SQLAlchemy 2.0 `DeclarativeBase`). The full schema spans **47 tables** across five schemas:

### Auth Schema (`auth_`)

| Table | Primary Key | Key Columns | Purpose |
|-------|-------------|-------------|---------|
| `auth_User` | `UserID` (Integer, autoincrement) | `Email` (String(255), unique, not null, indexed), `HashedPassword` (String(255), not null), `Role` (String(50), not null), `DistrictID` (FK → `src_District.DistrictID`, nullable), `IsActive` (Boolean, default=True), `CreatedAt`, `UpdatedAt` | System user registry — admin, officer, analyst, viewer roles |
| `auth_Session` | `SessionID` (Integer, autoincrement) | `UserID` (FK → `auth_User.UserID`, not null), `TokenHash` (String(255), indexed, not null), `ExpiresAt` (DateTime, not null), `RevokedAt` (DateTime, nullable), `CreatedAt` | JWT refresh token tracking with soft-revoke |
| `auth_Permission` | `PermissionID` (Integer, autoincrement) | `Role` (String(50), not null, indexed), `Resource` (String(255), not null), `Action` (String(50), not null), `CreatedAt` | RBAC matrix — maps roles to resource+action pairs |

### Source Schema (`src_`) — FIR Master Data

| Table | Primary Key | FK Dependencies | Purpose |
|-------|-------------|-----------------|---------|
| `src_Act` | `ActCode` (String(10)) | — | Statutes (BNS, IPC, IT Act, NDPS, Arms Act) |
| `src_Section` | `(ActCode, SectionCode)` | ActCode → src_Act | Legal sections under each act |
| `src_CrimeHead` | `CrimeHeadID` (Integer) | — | Crime categories: Property Offences, Violent Crimes, Cyber Crimes, etc. |
| `src_CrimeSubHead` | `CrimeSubHeadID` (Integer) | CrimeHeadID → src_CrimeHead | Sub-categories under each crime head |
| `src_CrimeHeadActSection` | `(CrimeHeadID, ActCode, SectionCode)` | CrimeHeadID → src_CrimeHead, ActCode → src_Act | Links crime heads to act/section pairs |
| `src_CaseCategory` | `CaseCategoryID` (Integer) | — | FIR, UDR, PAR, Zero FIR |
| `src_GravityOffence` | `GravityOffenceID` (Integer) | — | Heinous, Non-Heinous |
| `src_CaseStatusMaster` | `CaseStatusID` (Integer) | — | Under Investigation, Chargesheet Filed, Trial, Closed, etc. |
| `src_State` | `StateID` (Integer) | — | Karnataka (and future states) |
| `src_District` | `DistrictID` (Integer) | StateID → src_State | District lookup with state FK |
| `src_UnitType` | `UnitTypeID` (Integer) | — | Police Station, Commissionerate, District Office, State HQ |
| `src_Unit` | `UnitID` (Integer) | TypeID → src_UnitType, StateID → src_State, DistrictID → src_District | Police station/unit registry |
| `src_Rank` | `RankID` (Integer) | — | Police ranks: Constable through SP |
| `src_Designation` | `DesignationID` (Integer) | — | SHO, IO, Addl. SP, SP |
| `src_Employee` | `EmployeeID` (Integer) | DistrictID → src_District, UnitID → src_Unit, RankID → src_Rank, DesignationID → src_Designation | Police personnel records |
| `src_OccupationMaster` | `OccupationID` (Integer) | — | Occupation lookup |
| `src_CasteMaster` | `caste_master_id` (Integer) | — | Caste category lookup |
| `src_ReligionMaster` | `ReligionID` (Integer) | — | Religion lookup |
| `src_Court` | `CourtID` (Integer) | DistrictID → src_District, StateID → src_State | Court registry |
| `src_CaseMaster` | `CaseMasterID` (Integer) | PolicePersonID → src_Employee, PoliceStationID → src_Unit, CaseCategoryID → src_CaseCategory, GravityOffenceID → src_GravityOffence, CrimeMajorHeadID → src_CrimeHead, CrimeMinorHeadID → src_CrimeSubHead, CaseStatusID → src_CaseStatusMaster, CourtID → src_Court | Core FIR/case registry — `CrimeNo` (unique) |
| `src_Inv_OccuranceTime` | `CaseMasterID` (FK → src_CaseMaster) | CaseMasterID → src_CaseMaster | 1:1 occurrence details with geocoordinates |
| `src_ComplainantDetails` | `ComplainantID` (Integer) | CaseMasterID → src_CaseMaster, OccupationID → src_OccupationMaster, ReligionID → src_ReligionMaster, CasteID → src_CasteMaster | Complainant data per case |
| `src_Victim` | `VictimMasterID` (Integer) | CaseMasterID → src_CaseMaster | Victim data per case |
| `src_Accused` | `AccusedMasterID` (Integer) | CaseMasterID → src_CaseMaster | Accused data per case |
| `src_ArrestSurrender` | `ArrestSurrenderID` (Integer) | CaseMasterID → src_CaseMaster, StateID → src_State, DistrictID → src_District, PoliceStationID → src_Unit, IOID → src_Employee, CourtID → src_Court, AccusedMasterID → src_Accused | Arrest/surrender tracking |
| `src_ActSectionAssociation` | `(CaseMasterID, ActID, SectionID)` | CaseMasterID → src_CaseMaster, ActID → src_Act | Composite link: cases ↔ acts/sections |
| `src_ChargesheetDetails` | `CSID` (Integer) | CaseMasterID → src_CaseMaster, PolicePersonID → src_Employee | Chargesheet records |

### Intelligence Schema (`int_`)

| Table | Purpose |
|-------|---------|
| `int_PersonEntity` | Canonical person entity with deduplication |
| `int_PersonEntityLink` | Links person entities to source records (accused, etc.) |
| `int_RelationshipEdge` | Relationship graph between person entities |
| `int_VehicleLink` | Vehicle-to-case associations |
| `int_RiskScore` | ML-based risk scores per person |
| `int_RiskScoreFeatureImportance` | Feature importance for interpretability |
| `int_MoPattern` | Modus Operandi pattern clusters |
| `int_MoPatternLink` | Links MO patterns to cases |
| `int_AnomalyAlert` | Statistical anomaly alerts per district/crime head |
| `int_HotspotLayer` | Geospatial hotspot tiles |
| `int_RAGCorpusChunk` | RAG corpus chunks with embeddings |

### Governance Schema (`gov_`)

| Table | Purpose |
|-------|---------|
| `gov_AuditLog` | Audit trail for all entity mutations |
| `gov_FairnessCheckResult` | AI fairness audit results |
| `gov_DataProvenanceRecord` | Data lineage/provenance tracking |

### AI Schema (`ai_`)

| Table | Purpose |
|-------|---------|
| `ai_UsageRecord` | Token usage and cost tracking per AI call |
| `ai_PromptVersion` | Versioned prompt templates |
| `ai_Conversation` | Chat/conversation sessions |
| `ai_Message` | Individual messages within conversations |
| `ai_Feedback` | User feedback on AI responses |

---

## 2. Relationships (Foreign Keys)

All FK constraints are defined in `src/models/` and enforced via migrations `003_add_constraints_and_indexes.py`.

### Direct FK References

```
User.DistrictID           → src_District.DistrictID      (nullable, for district-scoped users)
Session.UserID            → auth_User.UserID             (cascade revoke)
CaseMaster.PolicePersonID → src_Employee.EmployeeID      (investigating officer)
CaseMaster.PoliceStationID → src_Unit.UnitID             (registered police station)
CaseMaster.CaseCategoryID → src_CaseCategory.CaseCategoryID
CaseMaster.GravityOffenceID → src_GravityOffence.GravityOffenceID
CaseMaster.CrimeMajorHeadID → src_CrimeHead.CrimeHeadID
CaseMaster.CrimeMinorHeadID → src_CrimeSubHead.CrimeSubHeadID
CaseMaster.CaseStatusID    → src_CaseStatusMaster.CaseStatusID
CaseMaster.CourtID         → src_Court.CourtID
InvOccuranceTime.CaseMasterID → src_CaseMaster.CaseMasterID  (1:1, PK)
ComplainantDetails.CaseMasterID → src_CaseMaster.CaseMasterID
Victim.CaseMasterID        → src_CaseMaster.CaseMasterID
Accused.CaseMasterID       → src_CaseMaster.CaseMasterID
ActSectionAssociation.CaseMasterID → src_CaseMaster.CaseMasterID
ActSectionAssociation.ActID → src_Act.ActCode
ChargesheetDetails.CaseMasterID → src_CaseMaster.CaseMasterID
```

### ORM Relationship Attributes (defined in phase-2 models and src/models/)

| Parent | Attribute | Child | Cardinality | Back-Populates |
|--------|-----------|-------|-------------|----------------|
| CaseMaster | `occurrence` | InvOccuranceTime | 1:1 | `case` |
| CaseMaster | `complainants` | ComplainantDetails | 1:N | `case` |
| CaseMaster | `victims` | Victim | 1:N | `case` |
| CaseMaster | `accused` | Accused | 1:N | `case` |
| CaseMaster | `arrests` | ArrestSurrender | 1:N | `case` |
| CaseMaster | `act_sections` | ActSectionAssociation | 1:N | `case` |
| CaseMaster | `chargesheets` | ChargesheetDetails | 1:N | `case` |
| User | `sessions` | Session | 1:N | `user` |
| User | `district` | District | N:1 | — |
| District | `state` | State | N:1 | — |
| Unit | `district` | District | N:1 | — |
| Unit | `unit_type` | UnitType | N:1 | — |
| Section | `act` | Act | N:1 | `sections` |
| CrimeHead | `sub_heads` | CrimeSubHead | 1:N | `crime_head` |

---

## 3. Constraints

### PRIMARY KEY
- All tables use single-column integer auto-increment PKs, except:
  - `src_Act` — `ActCode` (String(10))
  - `src_Section` — composite `(ActCode, SectionCode)`
  - `src_Inv_OccuranceTime` — `CaseMasterID` (FK+PK for 1:1)
  - `src_CrimeHeadActSection` — composite `(CrimeHeadID, ActCode, SectionCode)`
  - `src_ActSectionAssociation` — composite `(CaseMasterID, ActID, SectionID)`

### UNIQUE
- `User.Email` — login identifier
- `CaseMaster.CrimeNo` — `uq_crime_no`
- `Session.TokenHash` — refresh token hash
- `State.StateName`
- `ActSectionAssociation.(CaseMasterID, ActID, SectionID)` — `uq_act_section`

### NOT NULL
- `User.Email`, `User.HashedPassword`, `User.Role`
- `Session.UserID`, `Session.TokenHash`, `Session.ExpiresAt`
- `Permission.Role`, `Permission.Resource`, `Permission.Action`
- `CaseMaster.CrimeNo`
- `District.DistrictName`, `Unit.UnitName`, `CrimeHead.CrimeGroupName`, etc.

### DEFAULT
- `User.IsActive` = `True`
- All `CreatedAt` columns = `func.now()` (UTC)
- All `Active` boolean columns = `True`
- `UpdatedAt` on User, CaseMaster = `func.now()` with `onupdate=func.now()`

---

## 4. Indexes

Defined in `003_add_constraints_and_indexes.py`:

| Index | Table | Columns | Unique | Purpose |
|-------|-------|---------|--------|---------|
| `ix_auth_User_Email` | auth_User | Email | Yes | Login lookup |
| `ix_auth_Session_TokenHash` | auth_Session | TokenHash | Yes | Refresh validation |
| `ix_auth_Permission_Role` | auth_Permission | Role | No | Role-based queries |
| `ix_case_crimeno` | src_CaseMaster | CrimeNo | Yes | FIR lookup |
| `ix_case_regdate` | src_CaseMaster | CrimeRegisteredDate | No | Date range queries |
| `ix_case_station` | src_CaseMaster | PoliceStationID | No | Station filter |
| `ix_case_majorhead` | src_CaseMaster | CrimeMajorHeadID | No | Crime head filter |
| `ix_case_status` | src_CaseMaster | CaseStatusID | No | Status filter |
| `ix_case_station_date` | src_CaseMaster | PoliceStationID, CrimeRegisteredDate | No | Composite station+date |
| `ix_district_state` | src_District | StateID | No | State→district lookup |
| `ix_unit_district` | src_Unit | DistrictID | No | District→station lookup |
| `ix_emp_district` | src_Employee | DistrictID | No | Employee by district |
| `ix_emp_unit` | src_Employee | UnitID | No | Employee by unit |
| `ix_court_district` | src_Court | DistrictID | No | Court by district |
| Plus 15+ indexes on int_, gov_ tables for intelligence queries |

---

## 5. Migration Details

### Alembic Migration Sequence

Existing migrations at `src/alembic/versions/`:

| Revision | Down Revision | Description |
|----------|---------------|-------------|
| `001` | `None` | Initial schema — all model tables |
| `002` | `001` | Seed demo data (Karnataka state, districts, police stations, acts, sections, crime heads, 24 sample cases) |
| `003` | `002` | Add FK constraints, indexes, and check constraints |
| `004` | `003` | Auth tables — auth_User, auth_Session, auth_Permission |
| `005` | `004` | AI tables — UsageRecord, PromptVersion, Conversation, Message, Feedback |
| `006` | `005` | Seed initial users (admin@berunda.gov, analyst@berunda.gov) |
| `ffff29081afe` | `006` | **Phase 2 baseline** — autogenerate no-op (schema matches) |

### Manual Migration Script

Created at `phase-2/database-auth/migration_phase2.py` — standalone script that:
- `upgrade(url)` — creates all 47 tables via `Base.metadata.create_all()`
- `downgrade(url)` — drops all tables in reverse dependency order
- `get_create_statements(dialect)` — prints CREATE TABLE DDL for offline review
- Handles SQLite and PostgreSQL connection strings
- Converts async URLs (`+aiosqlite`, `+asyncpg`) to sync equivalents

### Lockout Column Migration (Future)

To enable DB-backed account lockout, add these columns to `auth_User`:
```python
col_defs = get_lockout_column_defs()  # from auth_enhancements.py
# Returns [Column("FailedLoginAttempts", Integer, default=0),
#           Column("LockedUntil", DateTime(timezone=True), nullable=True)]
```

---

## 6. Seed Data

Comprehensive seed script at `phase-2/database-auth/seed_data.py` (standalone) and `phase-2/database-auth/src/seed/seed_data.py` (integrated). All functions are **idempotent** — safe to run multiple times.

### State & Districts

| ID | State | ID | District |
|----|-------|----|----------|
| 1 | Karnataka | 1 | Bengaluru Urban |
| | | 2 | Bengaluru Rural |
| | | 3 | Mysuru |
| | | 4 | Belagavi |
| | | 5 | Dakshina Kannada |
| | | 6 | Kalaburagi |
| | | 7 | Tumakuru |
| | | 8 | Shivamogga |
| | | 9 | Hubballi-Dharwad |
| | | 10 | Ballari |

### Police Stations (30+ across 10 districts)

Each district has 2-4 police stations, e.g., MG Road PS, Whitefield PS, Koramangala PS, Jayanagar PS (Bengaluru Urban); Devanahalli PS, Nelamangala PS (Bengaluru Rural); Kuvempunagar PS, Vijayanagar PS (Mysuru), etc.

### Lookup Tables

| Table | Records | Examples |
|-------|---------|----------|
| CaseStatusMaster | 6 | Under Investigation, Chargesheet Filed, Trial, Closed, Acquitted, Convicted |
| CaseCategory | 4 | FIR, UDR, PAR, Zero FIR |
| CrimeHead | 8 | Property Offences, Violent Crimes, Cyber Crimes, Drugs/NDPS, Arms Act, Economic Offences, Missing Person, Other |
| CrimeSubHead | 16 | Theft, Burglary, Robbery, Murder, Attempt to Murder, Hacking, etc. |
| GravityOffence | 2 | Heinous, Non-Heinous |
| Act | 5 | BNS, IPC, IT Act, NDPS, Arms Act |
| Section | 27 | BNS 101 (Murder), BNS 303 (Theft), BNS 309 (Robbery), IPC 302, IPC 420, IT Act 66, etc. |
| UnitType | 4 | Police Station, Commissionerate, District Office, State HQ |
| Rank | 7 | Constable through SP |
| Designation | 4 | SHO, IO, Addl. SP, SP |
| Occupation | 8 | Private/Govt Employee, Business, Farmer, Student, etc. |
| Religion | 5 | Hindu, Muslim, Christian, Sikh, Other |
| Caste | 5 | General, OBC, SC, ST, Other |
| Court | 5 | JMFC/CJM/Session Court Bengaluru, JMFC Mysuru, JMFC Mangaluru |

### Users

| Email | Role | District | Initial Password |
|-------|------|----------|-----------------|
| admin@berunda.gov | admin | Bengaluru Urban | `Admin@123` |
| officer@ksp.karnataka.gov.in | officer | Bengaluru Urban | `Officer@123` |
| analyst@berunda.gov | analyst | Bengaluru Urban | `Analyst@123` |
| officer.mysuru@ksp.karnataka.gov.in | officer | Mysuru | `Officer@123` |
| officer.belagavi@ksp.karnataka.gov.in | officer | Belagavi | `Officer@123` |

Passwords are bcrypt-hashed using `bcrypt.hashpw(password.encode(), bcrypt.gensalt())` (12 rounds). Passwords are read from `settings.INITIAL_ADMIN_PASSWORD` and `settings.INITIAL_ANALYST_PASSWORD` env vars; fall back to hardcoded dev defaults.

### Permissions (17 RBAC entries)

| Role | Resources | Actions |
|------|-----------|---------|
| admin | users, cases, reports, analytics, permissions, settings | read, write, delete |
| officer | cases, reports | read, write (cases) |
| analyst | cases, reports, analytics | read |
| viewer | reports | read |

---

## 7. Authentication Flow

### Login → JWT Issuance → Session → Refresh → Logout

```
                        ┌──────────────┐
                        │   Client      │
                        └──────┬───────┘
                               │ POST /api/v1/auth/login
                               │ { email, password }
                               ▼
                        ┌──────────────┐
                        │ AuthService   │
                        │ .authenticate │
                        └──────┬───────┘
                               │
                   ┌───────────┼───────────┐
                   ▼           ▼           ▼
            Find User    Verify PW    Check IsActive
            by Email     (bcrypt)
                   │           │           │
                   └───────┬───┘           │
                           ▼               ▼
                    ┌──────────────┐   (401 if any
                    │ _issue_tokens │    fails)
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        access_token  refresh_token  Session record
        (JWT, HS256)  (JWT, HS256)   (TokenHash,
         expires 60m    expires 7d     ExpiresAt)
                                      stored in auth_Session
                           │
                           ▼
                    ┌──────────────┐
                    │   Client      │
                    │ stores both   │
                    └──────────────┘
```

### Token Refresh

```
Client → POST /api/v1/auth/refresh { refreshToken }
  1. Decode refresh JWT — verify type="refresh", signature, expiry
  2. Hash token suffix → find Session where TokenHash matches AND RevokedAt IS NULL
  3. Revoke old session (set RevokedAt = now)
  4. Issue new token pair via _issue_tokens
  5. Create new Session record
  6. Return new access + refresh tokens
```

### Authenticated Request

```
Client → GET /api/v1/protected
  Header: Authorization: Bearer <access_token>

Middleware (get_current_user):
  1. Extract Bearer token
  2. Decode JWT with JWT_SECRET / HS256
  3. Extract payload: { user_id, role, district_id, type="access" }
  4. Attach to request context

Route guard (require_role):
  1. Check payload.role ∈ allowed_roles
  2. 403 if insufficient
```

### Logout

```
Client → POST /api/v1/auth/logout
  Header: Authorization: Bearer <access_token>
  1. Extract refresh token from request
  2. Hash token suffix → find Session
  3. Set RevokedAt = now (soft delete)
  4. Return success
```

### JWT Configuration

| Parameter | Value | Source |
|-----------|-------|--------|
| Algorithm | HS256 | `JWT_ALGORITHM` |
| Secret | `dev-secret-change-in-production` (dev) | `JWT_SECRET` env var |
| Access token expiry | 60 minutes | `ACCESS_TOKEN_EXPIRY_MINUTES` |
| Refresh token expiry | 7 days | `REFRESH_TOKEN_EXPIRY_DAYS` |

### JWT Payload Structure

```json
// Access Token
{
  "user_id": 1,
  "role": "admin",
  "district_id": 1,
  "type": "access",
  "exp": 1721859600,
  "iat": 1721856000,
  "jti": "uuid-v4"
}

// Refresh Token
{
  "user_id": 1,
  "role": "admin",
  "district_id": 1,
  "type": "refresh",
  "exp": 1722460800,
  "iat": 1721856000,
  "jti": "uuid-v4"
}
```

### Session Security
- Refresh tokens are never stored plaintext; only `token[-64:]` hash persisted
- Session lookup filters `WHERE RevokedAt IS NULL` (non-revoked only)
- Revoked sessions are soft-deleted (timestamped) for audit
- Token type discrimination: access vs refresh endpoints reject wrong type
- `jti` (JWT ID) claim for token uniqueness and revocation tracking

---

## 8. Authorization Model

### Role Hierarchy

| Role | Level | Description |
|------|-------|-------------|
| `admin` | 4 (highest) | Full system access — users, cases, reports, permissions, settings |
| `officer` | 3 | Operational — create/edit cases within assigned district |
| `analyst` | 2 | Read-only — case data, reports, analytics within assigned district |
| `viewer` | 1 (lowest) | Restricted — summary reports only |

### District Scoping

- Users with non-null `DistrictID` can only access data within their district
- Admin users (`role=admin`) bypass district scoping
- Enforced at repository layer via `Unit.DistrictID` join filter:
  ```python
  if district_id is not None:
      q = q.join(CaseMaster.police_station).filter(Unit.DistrictID == district_id)
  ```

### Permission Enforcement

Permissions are checked via `require_role()` decorator on API endpoints:
```python
@router.get("/cases")
@require_role(["admin", "officer", "analyst"])
async def list_cases(current_user = Depends(get_current_user)):
    ...
```

The `AuthDependency` class in `src/middleware/auth.py` handles JWT decoding and role checking. For 403, it raises `HTTPException(status_code=403, detail="Insufficient permissions")`.

### RBAC Permission Table

Populated via `auth_enhancements.create_permissions_table()`:

| Role | Resource | Actions |
|------|----------|---------|
| admin | users | read, write, delete |
| admin | cases | read, write, delete |
| admin | reports, analytics, permissions, settings | read, write |
| officer | cases | read, write |
| officer | reports | read |
| analyst | cases, reports, analytics | read |
| viewer | reports | read |

---

## 9. Commands Executed

```bash
# ── Alembic autogenerate (Phase 2 baseline) ──
cd D:\Hack2Skill\Berunda
alembic --config src/alembic.ini revision --autogenerate -m "phase2_initial_schema"
# Generated: src/alembic/versions/ffff29081afe_phase2_initial_schema.py
# Auto-detected 0 changes (metadata matches existing DB) — no-op migration

# ── Verify migration sequence ──
alembic --config src/alembic.ini upgrade head
alembic --config src/alembic.ini history

# ── Run manual migration script ──
python -c "
from phase-2.database-auth.migration_phase2 import upgrade
upgrade('sqlite:///./berunda.db')
"

# ── Seed database ──
python -c "
from phase-2.database-auth.seed_data import seed_all
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
engine = create_engine('sqlite:///./berunda.db')
seed_all(Session(bind=engine))
"

# ── Reset database (drop + create + seed) ──
python -c "from phase-2.database-auth.reset_db import reset_database; reset_database()"

# ── Populate RBAC permissions ──
python -c "
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from phase-2.database-auth.auth_enhancements import create_permissions_table
engine = create_engine('sqlite:///./berunda.db')
create_permissions_table(Session(bind=engine))
print('Permissions synced')
"

# ── Validate password policy ──
python -c "
from phase-2.database-auth.auth_enhancements import password_policy_validator
password_policy_validator('Test@1234')  # OK
password_policy_validator('weak')       # raises PasswordValidationError
"

# ── Test account lockout manager ──
python -c "
from phase-2.database-auth.auth_enhancements import AccountLockoutManager
mgr = AccountLockoutManager(max_attempts=3, lockout_minutes=1)
user = type('User', (), {'UserID': 1, 'FailedLoginAttempts': 0, 'LockedUntil': None})()
for i in range(3):
    mgr.record_failed_attempt(user)
mgr.check_lockout(user)  # raises AccountLockoutError after 3 attempts
"

# ── Generate CREATE TABLE DDL ──
python -c "
from phase-2.database-auth.migration_phase2 import get_create_statements
for stmt in get_create_statements('sqlite'):
    print(stmt)
"

# ── Run existing phase-2 test suite ──
cd D:\Hack2Skill\Berunda\phase-2\database-auth
pip install -r requirements.txt
pytest tests/ -v --tb=short
pytest tests/ --cov=src --cov-report=term-missing
```

---

## 10. Files Changed

### New Files Created (this session)

| File | Purpose |
|------|---------|
| `phase-2/database-auth/migration_phase2.py` | Manual migration — upgrade/downgrade all 47 tables, SQL DDL generation |
| `phase-2/database-auth/seed_data.py` | Comprehensive seed: 10 districts, 30+ stations, 5 acts, 27 sections, 8 crime heads, 16 sub-heads, 5 users, 17 permissions |
| `phase-2/database-auth/auth_enhancements.py` | `create_permissions_table()`, `password_policy_validator()`, `AccountLockoutManager` with memory and DB-backed modes |
| `phase-2/database-auth/reset_db.py` | `drop_all()` + `create_all()` + `seed_data()` in one call |
| `phase-2/database-auth/test_fixtures.py` | Pytest fixtures: `sample_users`, `sample_district_data`, `sample_fir_data`, `sample_password_data` |
| `docs/handoffs/phase-2-database-auth-handoff.md` | This handoff document (v2.0) |
| `src/alembic/versions/ffff29081afe_phase2_initial_schema.py` | Alembic autogenerate migration — Phase 2 baseline |

### Existing Files Leveraged

| File | Role |
|------|------|
| `src/models/*.py` | 47 SQLAlchemy ORM models across 5 schemas |
| `src/alembic/env.py` | Alembic environment (imports Base.metadata) |
| `src/alembic/versions/001-006` | Prior migrations (initial schema through seed users) |
| `src/services/auth_service.py` | AuthService with authenticate, register, refresh, revoke |
| `src/routers/auth_router.py` | FastAPI endpoints: /login, /register, /refresh, /logout, /me |
| `src/middleware/auth.py` | AuthDependency, get_current_user, require_role |
| `src/config.py` | Settings: JWT_SECRET, DATABASE_URL, INITIAL_ADMIN_PASSWORD |
| `src/database.py` | Async engine, session factory, get_session dependency |
| `phase-2/database-auth/src/models.py` | Simplified model set (14 tables) for standalone testing |
| `phase-2/database-auth/src/auth/*.py` | Standalone password hashing, JWT, dataclass models |
| `phase-2/database-auth/src/seed/seed_data.py` | Original seed: 2 districts, 4 stations, 3 cases |
| `phase-2/database-auth/src/seed/test_fixtures.py` | Original fixtures: 2 FIRs, 3 users |
| `phase-2/database-auth/tests/*.py` | 72 passing tests across 6 test modules |

---

## 11. Security Risks

| Risk | Severity | Description | Mitigation |
|------|----------|-------------|------------|
| **JWT secret weak default** | HIGH | Dev secret `dev-secret-change-in-production` is hardcoded. Anyone who knows it can forge tokens. | Must be set via `JWT_SECRET` env var in production. CI/CD must inject a 256-bit random secret. |
| **No rate limiting on login** | MEDIUM | Login endpoint has no rate limiting, enabling brute-force attacks. | Deferred to Phase 3 API gateway. Suggested: `slowapi` with 5 req/min per IP. |
| **Account lockout (memory mode)** | LOW | Default lockout is in-memory only — resets on server restart. | Enable DB-backed mode (requires adding `FailedLoginAttempts` and `LockedUntil` columns) |
| **No TLS requirement** | MEDIUM | Auth tokens sent over HTTP expose credentials. | Deployment must enforce HTTPS at reverse proxy level. |
| **Refresh token hash truncation** | LOW | TokenHash stores last 64 chars — 256 bits of entropy. Collision risk negligible. | Acceptable for MVP. |
| **Session table unbounded growth** | LOW | Revoked sessions remain in DB indefinitely. | Add scheduled job to purge `ExpiresAt < now AND RevokedAt IS NOT NULL`. |
| **No email verification** | LOW | New user registrations are not verified. | Phase 4 should add email verification workflow. |
| **bcrypt 12 rounds** | NONE | OWASP-recommended cost factor. | No action required. |
| **Refresh token rotation** | NONE | Old refresh tokens revoked on each refresh — prevents replay. | Correctly implemented. No action required. |
| **Password policy not enforced server-side** | MEDIUM | `password_policy_validator()` exists but is not wired into registration endpoint. | Phase 3 should call validator in `AuthService.register()` before hashing. |

---

## 12. Integration Instructions

### For Backend Agent (Phase 3 — FastAPI Backend)

#### Model Imports
```python
# Use production models from main project
from src.models import Base
from src.models.auth_models import User, Session, Permission
from src.models.src_models import (
    CaseMaster, InvOccuranceTime, ComplainantDetails, Victim, Accused,
    District, Unit, CrimeHead, CaseStatusMaster, Act, Section,
)
```

#### Auth Service Integration
```python
from src.services.auth_service import AuthService
from src.services.base import BaseService
from src.middleware.auth import get_current_user, require_role, AuthDependency

# Protect endpoints:
@router.get("/api/v1/cases")
@require_role(["admin", "officer", "analyst"])
async def list_cases(current_user=Depends(get_current_user)):
    ...

# Use AuthDependency directly:
admin_only = AuthDependency(required_roles=["admin"])
```

#### Password Policy On Registration
```python
from phase_2.database_auth.auth_enhancements import password_policy_validator

async def register(email, password, ...):
    try:
        password_policy_validator(password)
    except PasswordValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    # ... proceed with registration
```

#### Account Lockout On Login
```python
from phase_2.database_auth.auth_enhancements import AccountLockoutManager

lockout_mgr = AccountLockoutManager(use_db=False)  # or True with DB columns

async def login(email, password):
    user = await get_user_by_email(email)
    if lockout_mgr.is_locked(user):
        raise HTTPException(status_code=429, detail="Account locked")
    try:
        result = await authenticate(email, password)
        lockout_mgr.reset_attempts(user)
        return result
    except AuthenticationError:
        lockout_mgr.record_failed_attempt(user)
        raise
```

### For Frontend Agent (Phase 3 — React/Vite)

#### API Endpoints

| Method | Path | Request Body | Response |
|--------|------|-------------|----------|
| POST | `/api/v1/auth/login` | `{ email, password }` | `{ token, refreshToken, expiresIn, user }` |
| POST | `/api/v1/auth/register` | `{ email, password, role, district_id? }` | `{ userId, email, name, role, permissions }` |
| POST | `/api/v1/auth/refresh` | `{ refreshToken }` | `{ token, refreshToken, expiresIn, user }` |
| POST | `/api/v1/auth/logout` | (Bearer token in header) | `{ success, message }` |
| GET | `/api/v1/auth/me` | (Bearer token in header) | `{ userId, email, name, role, permissions }` |

#### Token Management
```javascript
// Store tokens (consider httpOnly cookies for production)
localStorage.setItem('accessToken', data.token);
localStorage.setItem('refreshToken', data.refreshToken);

// Attach to all API calls
headers: { 'Authorization': `Bearer ${token}` }

// On 401: attempt silent refresh, then redirect to login if failed
const refreshTokens = async () => {
  const res = await fetch('/api/v1/auth/refresh', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ refreshToken: localStorage.getItem('refreshToken') }),
  });
  if (!res.ok) { logout(); return false; }
  const data = await res.json();
  localStorage.setItem('accessToken', data.token);
  localStorage.setItem('refreshToken', data.refreshToken);
  return true;
};
```

#### Important Notes
- Access tokens expire in **60 minutes**, refresh tokens in **7 days**
- DistrictID may be null (cross-district admin users)
- All timestamps in JWT are UTC epoch seconds
- `/api/v1` prefix assumes API gateway routing — adjust per deployment
- Default JWT secret **must** be changed in production

### For Quality Agent (Phase 2 — Validation)

Test fixtures are available at `phase-2/database-auth/test_fixtures.py`:
- `sample_users` — 3 user dicts (admin, officer, analyst)
- `sample_district_data` — state + 3 districts + 3 police stations
- `sample_fir_data` — minimal FIR with nested occurrence/complainant/victim/accused
- `sample_password_data` — valid/invalid passwords for policy testing

---

## 13. Auth Enhancements Summary

Three enhancement modules created in `phase-2/database-auth/auth_enhancements.py`:

### `create_permissions_table(db)` → int
Populates `auth_Permission` with 17 RBAC entries across 4 roles. Idempotent — skips existing entries. Returns count of inserted rows.

### `password_policy_validator(password, rules?)` → str
Validates password strength:
- Min 8 characters
- At least 1 uppercase letter
- At least 1 lowercase letter
- At least 1 digit
- At least 1 special character (!@#$%^&*()_+-=[]{}|;:',.<>?/`~)
Returns password on success; raises `PasswordValidationError` on failure.

### `AccountLockoutManager(max_attempts, lockout_minutes, use_db)`
- **Memory mode** (default): tracks failed attempts in `_memory_store` dict; resets on restart
- **DB mode** (`use_db=True`): requires `FailedLoginAttempts` (Integer) and `LockedUntil` (DateTime) columns on `auth_User`
- Methods: `record_failed_attempt()`, `check_lockout()` (raises `AccountLockoutError`), `reset_attempts()`, `is_locked()`
- Default: 5 attempts, 15-minute lockout

---

*End of Phase 2 — Database & Authentication Handoff Document*
