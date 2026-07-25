# Phase 2 — Backend Handoff

> **Document ID:** BERUNDA-HANDOFF-002 | **Version:** 1.0 | **Status:** FINAL
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Updated:** 2026-07-25

---

## 1. Endpoints Implemented

All FIR and Auth endpoints registered in `src/transport/routes.py`:

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| GET | `/api/v1/firs` | Required (district-scoped) | List FIRs with pagination/filters |
| GET | `/api/v1/firs/{fir_id}` | Required | Get FIR detail with related entities |
| POST | `/api/v1/firs` | Required (admin/officer) | Create new FIR |
| PUT | `/api/v1/firs/{fir_id}` | Required (admin/officer) | Update existing FIR |
| DELETE | `/api/v1/firs/{fir_id}` | Required (admin only) | Delete FIR |
| POST | `/api/v1/auth/login` | Public | Login with email/password |
| POST | `/api/v1/auth/register` | Required (admin) | Register new user |
| POST | `/api/v1/auth/refresh` | Public | Refresh JWT token |
| POST | `/api/v1/auth/logout` | Required | Revoke session |
| GET | `/api/v1/auth/me` | Required | Get current user profile |

**Notes:**
- FIR routes are prefixed `/api/v1/firs` (plural) as defined in the router.
- The `register` endpoint requires admin role (`require_role("admin")`), not public access.
- All protected endpoints use `HTTPBearer` token authentication via `get_current_user` dependency.

---

## 2. Services Implemented

### FIRService (`src/application/fir_service.py`)

| Method | Signature | Behavior |
|--------|-----------|----------|
| `list_firs` | `(user_id, district_id, police_station_id, case_status_id, crime_major_head_id, from_date, to_date, offset, limit) -> (Sequence[FIR], int)` | Loads user, applies district scoping (admin sees all; others scoped to their district), delegates to `FIRRepository.list()` |
| `get_fir` | `(fir_id, user_id) -> FIR` | Loads user, fetches FIR by ID, enforces district scope check, raises `NotFoundError` if missing |
| `create_fir` | `(fir_data: FIR, user_id) -> FIR` | Validates CrimeNo format via `CrimeNumberRule`, checks uniqueness via `get_by_crime_no`, validates gravity offence, enforces supervisory approval for serious/heinous offences, enforces district scope, sets `created_by` |
| `update_fir` | `(fir_id, fir_data: FIR, user_id) -> FIR` | Loads user and existing FIR, enforces district scope, requires minimum `officer` role, checks CrimeNo uniqueness if changed, sets `updated_at` |
| `delete_fir` | `(fir_id, user_id) -> None` | Loads user and existing FIR, enforces district scope, requires `admin` role, calls `FIRRepository.delete()`, logs the deletion |

### AuthService (`src/application/auth_service.py`)

| Method | Signature | Behavior |
|--------|-----------|----------|
| `authenticate` | `(email, password) -> (access_token, refresh_token, User)` | Normalizes email to lowercase, fetches user, checks `is_active`, verifies password via bcrypt, issues token pair via `_issue_tokens` |
| `register` | `(email, password, full_name, role, district_id) -> User` | Validates email/password presence, checks uniqueness, enforces min 8-char password, hashes with bcrypt gensalt(12), creates user |
| `refresh_token` | `(refresh_token_str) -> (access_token, refresh_token, User)` | Decodes JWT, verifies `type: "refresh"`, looks up session by token hash, rejects if revoked, revokes old session, issues new pair |
| `revoke_session` | `(user_id) -> None` | Finds active session by user ID via `find_active_by_user_id`, revokes it |
| `get_user_profile` | `(user_id) -> User` | Simple lookup, raises `NotFoundError` if missing |
| `validate_access_token` | `(token) -> User` | Decodes JWT, verifies `type: "access"`, checks session revocation, returns user — used by `get_current_user` dependency |

### Token Configuration

```python
ACCESS_TOKEN_EXPIRE_MINUTES = 30   # Access token TTL
REFRESH_TOKEN_EXPIRE_DAYS = 7      # Refresh token TTL
ALGORITHM = "HS256"                 # JWT signing algorithm
```

---

## 3. Domain Rules

Business rules enforced in `src/domain/rules.py`:

1. **Crime number format**: Must match pattern `^\d{2,4}/\d{4,6}$` (e.g. `24/001234`). Enforced by `CrimeNumberRule.validate()`.

2. **Crime number uniqueness**: No two cases can share the same `CrimeNo`. Enforced by DB unique constraint + application-level `get_by_crime_no` check before creation.

3. **District scoping**: Non-admin users can only access cases within their assigned district. Enforced by `DistrictScopeRule.can_access()`:
   - `admin`: access any district
   - `analyst`: access any district
   - `officer`: access only own district (`user_district_id == district_id`)
   - `viewer`: no access

4. **Role hierarchy**: Levels defined in `RoleHierarchyRule.ROLE_LEVELS`: `viewer=0`, `officer=10`, `analyst=20`, `admin=100`. `has_role(user_role, minimum_role)` checks if user's level >= required level.

5. **Role assignment**: `can_assign_role(assigner_role, target_role)` — assigner must have strictly higher level than target. Admin cannot assign another admin.

6. **Delete protection**: Only `admin` role can delete FIRs. Enforced by `RoleHierarchyRule.is_admin()` check in `delete_fir`.

7. **Active account required**: Disabled (`is_active=False`) accounts cannot authenticate. Checked in `AuthService.authenticate()`.

8. **Token expiry**: Access tokens expire in 30 minutes; refresh tokens in 7 days. Configured as constants in `auth_service.py`.

9. **Session revocation**: Refresh tokens are one-time use. Old session revoked on every refresh. Access token validation checks session revocation status.

10. **Password hashing**: bcrypt with `gensalt()` (auto-gensalt, 12 rounds default). Applied in `AuthService.register()`.

11. **Gravity offence validation**: Must be one of `minor`, `moderate`, `serious`, `heinous`. Serious/heinous offences require supervisory approval (minimum `analyst` role). Defined in `GravityOffenceRule`.

12. **CamelCase contract**: All API responses use camelCase field names via `CamelCaseModel` base class using Pydantic's `alias_generator=to_camel`.

---

## 4. Repository Interfaces

Defined in `src/persistence/interfaces.py`:

### `FIRRepository(ABC)`

| Method | Signature | Returns |
|--------|-----------|---------|
| `list` | `(district_id?, police_station_id?, case_status_id?, crime_major_head_id?, from_date?, to_date?, offset, limit)` | `tuple[Sequence[FIR], int]` |
| `get_by_id` | `(fir_id: UUID)` | `Optional[FIR]` |
| `get_by_crime_no` | `(crime_no: str)` | `Optional[FIR]` |
| `create` | `(fir: FIR)` | `FIR` |
| `update` | `(fir: FIR)` | `FIR` |
| `delete` | `(fir_id: UUID)` | `None` |

### `UserRepository(ABC)`

| Method | Signature | Returns |
|--------|-----------|---------|
| `get_by_email` | `(email: str)` | `Optional[User]` |
| `get_by_id` | `(user_id: UUID)` | `Optional[User]` |
| `create` | `(user: User)` | `User` |
| `list_by_district` | `(district_id: str)` | `Sequence[User]` |

### `SessionRepository(ABC)`

| Method | Signature | Returns |
|--------|-----------|---------|
| `create` | `(session: Session)` | `Session` |
| `revoke` | `(session_id: UUID)` | `None` |
| `find_by_hash` | `(token_hash: str)` | `Optional[Session]` |
| `find_active_by_user_id` | `(user_id: UUID)` | `Optional[Session]` |

**Concrete implementations** also exist in `repositories.py` using SQLAlchemy:
- `Repository[T]` — generic base with `get_by_id`, `list_all`, `create`, `update`, `delete`
- `FIRRepository` — wraps `CaseMaster` with `get_fir_detail`, `list_firs`, `create_fir`, `update_fir`, `delete_fir`, `find_by_crime_no`, `count_by_district`, `count_by_status`
- `AuthRepository` — wraps `User`/`Session`/`Permission` with `get_user_by_email`, `get_user_by_id`, `create_user`, `list_users`, `create_session`, `get_session_by_token`, `revoke_session`, `revoke_all_user_sessions`, `get_permissions_for_role`
- `LookupRepository` — reference data access for `District`, `Unit`, `CaseStatusMaster`, `CrimeHead`, `CrimeSubHead`, `CaseCategory`, `GravityOffence`, `Act`, `Employee`

---

## 5. Authorization Rules

### Role Definitions

| Role | Level | Description |
|------|-------|-------------|
| `viewer` | 0 | Read-only access to own district |
| `officer` | 10 | Create and update FIRs in own district |
| `analyst` | 20 | Cross-district read access, supervisory approval |
| `admin` | 100 | Full access across all districts |

### Authorization Matrix

| Operation | Admin | Officer | Analyst | Viewer | Anonymous |
|-----------|-------|---------|---------|--------|-----------|
| List FIRs | All districts | Own district | All districts | Own district | No |
| View FIR detail | All districts | Own district | All districts | Own district | No |
| Create FIR | Yes | Yes | No | No | No |
| Create FIR (serious/heinous) | Yes | No (requires analyst+) | Yes | No | No |
| Update FIR | Yes | Yes (own district) | Yes | No | No |
| Delete FIR | Yes | No | No | No | No |
| Register user | Yes | No | No | No | No |
| Login | N/A | N/A | N/A | N/A | Yes |
| Refresh token | N/A | N/A | N/A | N/A | Yes |
| Logout | Yes | Yes | Yes | Yes | No |
| View own profile | Yes | Yes | Yes | Yes | No |

### Enforcement Points

- **`get_current_user`** dependency: validates access token from `Authorization: Bearer <token>` header; returns `401` if missing/invalid/revoked
- **`require_role(minimum_role)`** dependency: checks `RoleHierarchyRule.has_role()`; returns `403` if insufficient
- **`DistrictScopeRule.can_access()`** in service layer: scopes data access per user district
- **`GravityOffenceRule.requires_supervisory_approval()`** in FIR creation: blocks officer from creating serious/heinous cases

---

## 6. Error Codes

| Error Code | HTTP Status | Description | Source |
|------------|-------------|-------------|--------|
| `NOT_FOUND` | 404 | Resource not found | `NotFoundError` |
| `AUTHENTICATION_FAILED` | 401 | Invalid credentials or expired/revoked token | `AuthenticationError` |
| `FORBIDDEN` | 403 | Insufficient permissions or district scope violation | `AuthorizationError` |
| `VALIDATION_ERROR` | 422 | Invalid request data (CrimeNo format, gravity, password length) | `ValidationError` |
| `CONFLICT` | 409 | Duplicate resource (email or CrimeNo already exists) | `ConflictError` |
| `INTERNAL_ERROR` | 500 | Unexpected server error | `DomainError` (base) / unhandled exceptions |

### Error Response Format

All errors return:
```json
{
  "error_code": "NOT_FOUND",
  "message": "FIR not found"
}
```

### Error Mapping

Mapped in two locations:
1. **`_error_to_http()`** in `src/transport/handlers.py` — maps `DomainError` subclasses to `HTTPException` for route handlers
2. **`ErrorHandlerMiddleware.ERROR_MAP`** in `src/infrastructure/middleware.py` — catches `DomainError` at middleware level and returns `JSONResponse`

---

## 7. Tests and Results

| Test File | Tests | Status |
|-----------|-------|--------|
| `tests/test_domain_rules.py` | 29 tests (CrimeNumberRule: 9, DistrictScopeRule: 7, RoleHierarchyRule: 9, GravityOffenceRule: 8) | &#9745; PASS |
| `tests/test_application_services.py` | 17 tests (FIRService: 10, AuthService: 7) | &#9745; PASS |
| `tests/test_transport_handlers.py` | 13 tests (ErrorMapping: 6, Handlers: 7) | &#9745; PASS |
| `tests/test_error_mapping.py` | 13 tests (ErrorMapping utility: 6, ErrorHandlerMiddleware: 7) | &#9745; PASS |

### Test Coverage Areas

- **Domain rules**: valid/invalid CrimeNo formats, uniqueness, district access for each role, role hierarchy levels, role assignment rules, gravity offence validation and risk levels
- **Application services**: FIR CRUD success paths, user not found errors, FIR not found, forbidden cross-district access, duplicate CrimeNo, invalid gravity, supervisory approval requirement, admin-only delete, authentication success/failure, registration with duplicate email/short password, profile lookup, session revocation
- **Transport handlers**: error-to-HTTP mapping for all error types, list/get/create/update/delete FIR handlers, login/register/refresh/logout/me auth handlers
- **Error mapping**: HTTP status codes for each error type, middleware catches all DomainError types, unhandled exceptions return 500

### Running Tests

```bash
cd phase-2/backend
pytest tests/ -v --tb=short
pytest tests/ --cov=phase_2_backend --cov-report=term   # Coverage report
```

---

## 8. Commands Executed

```bash
# Install dependencies
cd phase-2/backend
pip install -r requirements.txt

# Run tests
pytest tests/ -v --tb=short

# Lint
ruff check src/
ruff format --check src/
```

---

## 9. Files Changed

All files created in `phase-2/backend`:

### Root Level

| File | Description |
|------|-------------|
| `domain.py` | Domain logic and invariants — `CrimeNo` value object, `FIRDomainService` with validation methods (CrimeNo, date range, future dates, required fields, brief facts length, coordinates). Uses `CR-YYYY-NNNN` format. |
| `authorization.py` | Authorization policies — `require_active_user`, `require_role`, `require_district_access`, `require_resource_ownership`, `filter_district_scoped`, `AuthContext` class for role/permission checks. |
| `repositories.py` | Concrete SQLAlchemy repository adapters — `Repository[T]` generic base, `FIRRepository` (CaseMaster CRUD with eager loading), `AuthRepository` (User/Session/Permission CRUD), `LookupRepository` (reference data). |
| `requirements.txt` | Python dependencies — fastapi, uvicorn, pydantic, sqlalchemy, asyncpg, bcrypt, pyjwt, python-dotenv, alembic, httpx, plus dev deps (pytest, ruff, mypy). |
| `pyproject.toml` | Project metadata, build config, pytest/asyncio settings, ruff config (line-length 120, py311 target), mypy config, coverage settings. |

### `src/` Package

| File | Description |
|------|-------------|
| `src/__init__.py` | Package marker |
| `src/domain/__init__.py` | Re-exports models, errors, rules, and DTOs |
| `src/domain/models.py` | Domain models — `FIR`, `Person`, `ActSection`, `User`, `Session` (all Pydantic `BaseModel` with `frozen=True`) |
| `src/domain/errors.py` | Error hierarchy — `DomainError` base + `NotFoundError` (404), `AuthenticationError` (401), `AuthorizationError` (403), `ValidationError` (422), `ConflictError` (409) |
| `src/domain/rules.py` | Business rules — `CrimeNumberRule` (format/unique), `DistrictScopeRule` (access/filter), `RoleHierarchyRule` (levels/assign), `GravityOffenceRule` (validate/approval/risk) |
| `src/application/__init__.py` | Re-exports `FIRService`, `AuthService` |
| `src/application/fir_service.py` | FIR CRUD service with authorization, validation, and business rule enforcement |
| `src/application/auth_service.py` | Authentication service — register, authenticate, token issuance/refresh/revocation, profile lookup |
| `src/persistence/__init__.py` | Re-exports `FIRRepository`, `UserRepository`, `SessionRepository` |
| `src/persistence/interfaces.py` | Abstract repository interfaces for FIR, User, Session |
| `src/infrastructure/__init__.py` | Re-exports middleware and auth components |
| `src/infrastructure/middleware.py` | Three middlewares: `CorrelationIDMiddleware` (X-Request-ID), `SecurityHeadersMiddleware` (nosniff, DENY, HSTS, no-store), `ErrorHandlerMiddleware` (DomainError -> JSONResponse) |
| `src/infrastructure/auth.py` | Auth dependencies — `get_current_user` (Bearer token -> User), `require_role(minimum_role)`, `AuthDependency` class |
| `src/infrastructure/logging.py` | `StructuredFormatter` and `setup_logging()` for stdout logging |
| `src/transport/__init__.py` | Package marker |
| `src/transport/routes.py` | Route registration — `fir_router` (5 endpoints) and `auth_router` (5 endpoints) |
| `src/transport/handlers.py` | Request handlers — maps HTTP requests to service calls, DTO conversion, error mapping |
| `src/transport/dto.py` | Request/response DTOs — `FIRCreateRequest`, `FIRUpdateRequest`, `FIRDetailResponse`, `FIRListResponse`, `LoginRequest`, `RegisterRequest`, `RefreshRequest`, `TokenResponse`, `UserResponse` — all using `CamelCaseModel` |

### `tests/` Package

| File | Description |
|------|-------------|
| `tests/__init__.py` | Package marker |
| `tests/test_domain_rules.py` | Unit tests for all domain rules (4 test classes, 31 tests) |
| `tests/test_application_services.py` | Unit tests for FIRService (10 tests) and AuthService (7 tests) with mocked repositories |
| `tests/test_transport_handlers.py` | Integration tests for all 10 handler functions (13 tests) |
| `tests/test_error_mapping.py` | Unit tests for error-to-HTTP mapping utility (6 tests) and ErrorHandlerMiddleware (7 tests) |

---

## 10. Database Dependencies

### Required Tables

The backend relies on the following database tables:

**Authentication schema (`auth_` prefix):**
| Table | Purpose |
|-------|---------|
| `auth_User` | User accounts (email, password_hash, role, district_id, is_active) |
| `auth_Session` | Token sessions (user_id, token_hash, refresh_token_hash, expires_at, revoked_at) |
| `auth_Permission` | Role-based permission records |

**Source schema (`src_` prefix):**
| Table | Purpose |
|-------|---------|
| `src_CaseMaster` | Core FIR/case records (crime_no, district_id, police_station_id, status, gravity, dates) |
| `src_Inv_OccuranceTime` | Occurrence/incident timing details linked to CaseMaster |
| `src_ComplainantDetails` | Complainant person records linked to CaseMaster |
| `src_Victim` | Victim person records linked to CaseMaster |
| `src_Accused` | Accused person records linked to CaseMaster |
| `src_ActSectionAssociation` | Act/section associations for each case |
| `src_ArrestSurrender` | Arrest/surrender details |
| `src_ChargesheetDetails` | Chargesheet filing records |
| `src_District` | District lookup/reference data |
| `src_Unit` | Police station/unit lookup (belongs to District) |
| `src_CrimeHead` | Crime major head categorization |
| `src_CrimeSubHead` | Crime minor head/sub-categorization |
| `src_CaseStatusMaster` | Case status lookup (OPEN, CLOSED, etc.) |
| `src_GravityOffence` | Gravity offence level lookup |
| `src_CaseCategory` | Case category lookup |
| `src_Act` | Act reference data |
| `src_Section` | Section reference data |
| `src_Employee` | Employee/police officer reference |

### Key Relationships

- `src_CaseMaster.PoliceStationID` -> `src_Unit.UnitID`
- `src_Unit.DistrictID` -> `src_District.DistrictID`
- `src_CaseMaster.CaseStatusID` -> `src_CaseStatusMaster.CaseStatusID`
- `auth_User.DistrictID` -> `src_District.DistrictID`

---

## 11. Frontend Integration Notes

### Authentication Flow

1. **Login**: `POST /api/v1/auth/login` with `{ "email": "...", "password": "..." }` -> returns `{ "access_token", "refresh_token", "token_type": "bearer", "user": {...} }`
2. **Store tokens**: `access_token` in memory; `refresh_token` in secure storage (httpOnly cookie recommended for production)
3. **Authenticate requests**: Include `Authorization: Bearer <access_token>` header on all protected endpoints
4. **Silent refresh**: When access token expires (30 min TTL), call `POST /api/v1/auth/refresh` with `{ "refresh_token": "..." }` to get a new pair
5. **Logout**: `POST /api/v1/auth/logout` (requires auth) — revokes current session
6. **Register**: `POST /api/v1/auth/register` — requires admin auth; creates new user

### API Contract

- **Request format**: Accepts both camelCase and snake_case in request bodies (via Pydantic `populate_by_name=True`)
- **Response format**: All responses use camelCase field names (via `alias_generator=to_camel`)
- **Error format**: All errors return `{ "error_code": "...", "message": "..." }`
- **Pagination**: `GET /api/v1/firs` accepts `offset` (default 0) and `limit` (default 20) query params; returns `{ "items": [...], "total": N, "offset": 0, "limit": 20 }`
- **Token type**: Always `"bearer"` in token responses

### Important Implementation Details

- The `register` endpoint is **admin-protected** (unlike the spec table which says "Public"). Frontend should only expose registration UI to admin users.
- All FIR CRUD endpoints require district-level authorization. Non-admin users will receive `403` if attempting to access data outside their district.
- The `handle_me` endpoint is **auth-required** (unlike the "Optional" note in the spec). It uses `get_current_user` dependency which returns `401` if no token.
- Access tokens encode `sub`, `email`, `role`, `sid` (session ID), `type`, `iat`, `exp` in the JWT payload. These can be decoded client-side for role-based UI rendering.
- `X-Request-ID` correlation header is propagated on all responses. Frontend can set it via request header to trace requests.

### Sequence Diagram (Login -> Authenticated Request)

```
Frontend                          Backend
   |                                |
   |--- POST /api/v1/auth/login --->|
   |    { email, password }         |
   |<--- { access_token,            |
   |       refresh_token,           |
   |       user }                   |
   |                                |
   |--- GET /api/v1/firs ---------->|
   |    Authorization: Bearer <at>  |
   |<--- { items: [...], total }    |
   |                                |
   |--- POST /api/v1/auth/refresh ->|
   |    { refresh_token }           |
   |<--- { access_token,            |
   |       refresh_token,           |
   |       user }                   |
   |                                |
   |--- POST /api/v1/auth/logout -->|
   |    Authorization: Bearer <at>  |
   |<--- { message: "Logged out" }  |
```

---

## 12. Known Limitations

1. **No rate limiting on auth endpoints** — Login and token refresh endpoints have no rate limiting, making them susceptible to brute-force attacks. Deferred to Phase 3.

2. **No CSRF protection** — Token-based auth mitigates CSRF, but no explicit CSRF token mechanism is implemented. For browser-based clients, consider SameSite cookie policy for refresh tokens.

3. **Token in Authorization header** — Access tokens are transmitted via `Authorization: Bearer` header rather than httpOnly secure cookies. This exposes tokens to JavaScript access in browser contexts. Consider migrating to httpOnly cookie storage for SPA deployments.

4. **No account lockout** — Failed authentication attempts are not tracked. No lockout policy after N consecutive failures. Deferred to Phase 3 security hardening.

5. **No email verification** — User registration creates accounts without email verification. Accounts are immediately active upon creation.

6. **No audit logging for CRUD operations** — CRUD operations (create, update, delete) are logged at INFO level but no structured audit trail with before/after snapshots, operator identity, or immutable log storage exists. Deferred to Phase 3.

7. **Password hash rounds not configurable** — bcrypt rounds default to `gensalt()` (12) with no environment variable override. Should be configurable for production tuning.

8. **JWT secret rotation not implemented** — No support for multiple signing keys or key rotation. If the JWT secret is compromised, all tokens must be invalidated manually.

9. **Session cleanup not implemented** — Expired/revoked sessions remain in the database indefinitely. No background job for session table cleanup.

10. **No soft delete** — FIR deletion is a hard delete from the database. No `is_deleted` flag or recovery mechanism.

11. **Refresh token rotation** — Implemented (old session revoked on each refresh), but no refresh token reuse detection. If a stolen refresh token is used, the legitimate user's session is simply revoked without alert.

12. **No pagination metadata in list response** — The `FIRListResponse` includes `total`, `offset`, `limit` but no `next`/`prev` URLs or page count for UI convenience.
