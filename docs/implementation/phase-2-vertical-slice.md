# Phase 2 — Vertical Slice: FIR Case Management

> **Document ID:** BERUNDA-IMPL-002 | **Version:** 1.0 | **Status:** APPROVED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## Selected User Journey

**FIR Case Management — Full CRUD (List, View, Create)**

A user authenticates, views the list of FIR cases, inspects a case detail, and creates a new FIR record. This is the primary data-entry and review workflow for the crime intelligence platform.

## Reason for Selection

1. **Core product value** — FIR records are the fundamental data entity; all analytics (entity resolution, hotspot, risk scoring) depend on FIR data
2. **Full-stack exercise** — touches frontend UI, API, business logic, database, and auth
3. **Hackathon-demonstrable** — clear before/after states visible in the UI
4. **Completable** — no external AI services required for this slice
5. **Extensible** — serves as foundation for Phase 3+ features (NER, entity resolution, graph)

## Actors

| Actor | Role | Description |
|-------|------|-------------|
| Investigating Officer | `officer` | Can view cases in own district, cannot create |
| SCRB Analyst | `analyst` | Can view all cases, can create cases |
| Admin | `admin` | Full access — create, read, update, delete |

## Preconditions

1. Database is running with migrations applied
2. At least one user exists (seeded admin/officer/analyst)
3. Reference data seeded (districts, crime heads, case statuses, police stations)
4. Frontend and backend services are running

## Main Flow

```
1. User navigates to /login
2. User enters email + password → POST /api/v1/auth/login
3. System returns JWT access token + refresh token
4. User is redirected to dashboard (/) or /cases
5. User navigates to /cases → GET /api/v1/fir?page=1&page_size=20
6. System returns paginated case list with CrimeNo, date, status
7. User clicks a case → GET /api/v1/fir/{id}
8. System returns case detail with complainants, victims, accused
9. User clicks "Create Case" → sees form with required fields
10. User fills form → POST /api/v1/fir
11. System validates and persists the case
12. User is redirected to the new case detail
```

## Alternative Flows

| Condition | Flow |
|-----------|------|
| User has `officer` role | Case list filtered to own district |
| Invalid form data | Validation errors displayed inline |
| Network error | Error message with retry option |
| Token expired | Auto-refresh or redirect to login |

## Error Flows

| Error | HTTP Status | Response Code | UI Behavior |
|-------|-------------|---------------|-------------|
| Invalid credentials | 401 | AUTHENTICATION_ERROR | "Invalid email or password" |
| Expired token | 401 | AUTHENTICATION_ERROR | Redirect to login |
| Missing required field | 422 | VALIDATION_ERROR | Inline field errors |
| FIR not found | 404 | NOT_FOUND | "Case not found" message |
| Duplicate CrimeNo | 409 | CONFLICT | "CrimeNo already exists" |
| Forbidden | 403 | FORBIDDEN | "Access denied" message |
| Server error | 500 | INTERNAL_ERROR | "Something went wrong" with correlation ID |

## Acceptance Criteria

1. ✅ User can log in with valid credentials
2. ✅ Invalid login shows error message
3. ✅ Authenticated user sees paginated case list
4. ✅ Case list respects district scoping for officer role
5. ✅ User can view case detail with all related entities
6. ✅ Authorized user can create a new case
7. ✅ Unauthorized create returns 403
8. ✅ Invalid form data shows validation errors
9. ✅ Loading state shown during API calls
10. ✅ Empty state shown when no cases exist
11. ✅ Error state shown on API failure with retry
12. ✅ Token refresh works transparently

## UI Screens

| Screen | Route | Description |
|--------|-------|-------------|
| Login | `/login` | Email + password form with demo mode |
| Case List | `/cases` | Paginated table with search and filters |
| Case Detail | `/cases/{id}` | Full case record with related persons |
| Create Case | `/cases/new` | Form with validated fields |

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | /api/v1/auth/login | None | Authenticate and get tokens |
| POST | /api/v1/auth/register | None | Register new user |
| POST | /api/v1/auth/refresh | Token | Refresh access token |
| POST | /api/v1/auth/logout | Token | Revoke session |
| GET | /api/v1/auth/me | Token | Get current user profile |
| GET | /api/v1/fir | Token | List cases (paginated) |
| GET | /api/v1/fir/{id} | Token | Get case detail |
| POST | /api/v1/fir | Token (admin, analyst) | Create new case |
| PUT | /api/v1/fir/{id} | Token (admin, analyst) | Update case |
| DELETE | /api/v1/fir/{id} | Token (admin) | Delete case |

## Database Entities

| Entity | Schema | Description |
|--------|--------|-------------|
| CaseMaster | src | Core case record |
| InvOccuranceTime | src | Occurrence details + BriefFacts |
| District | src | Reference district data |
| Unit | src | Police station data |
| CrimeHead | src | Crime type reference |
| CaseStatusMaster | src | Case status reference |
| User | auth | User account with role |
| Session | auth | Refresh token session |

## Security Requirements

| Requirement | Implementation |
|-------------|----------------|
| Password hashing | bcrypt with gensalt |
| JWT signing | HS256 with configurable secret |
| Token expiry | Access: 60 min, Refresh: 7 days |
| Role-based access | Backend `require_role` middleware |
| District scoping | Officer role filtered to own district |
| Input validation | Pydantic schemas on backend, form validation on frontend |
| CORS | Configured for frontend origins |
| CSRF | JWT bearer tokens (no cookies for web) |

## Test Scenarios

| Type | Scenario |
|------|----------|
| Unit | AuthService.authenticate — valid credentials return tokens |
| Unit | AuthService.authenticate — invalid credentials raise AuthenticationError |
| Unit | FIRService.list_firs — returns paginated results |
| Unit | FIRService.create_fir — creates case with occurrence |
| Integration | POST /api/v1/auth/login → 200 with token |
| Integration | POST /api/v1/fir → 201 with valid data |
| Integration | GET /api/v1/fir → 200 with paginated list |
| Integration | GET /api/v1/fir/{id} → 200 with detail |
| Integration | POST /api/v1/fir without auth → 401 |
| Integration | POST /api/v1/fir with officer role → 403 |
| E2E | Login → List cases → View detail → Create case → Verify |

## Deferred Capabilities

| Capability | Reason |
|------------|--------|
| Bulk CSV import | Requires file upload and async processing |
| Edit/delete case | Requires ownership/deletion policies |
| Filter by date/crime type | Additional query params |
| Full-text search | Requires FTS index and separate endpoint |
| Related entity editing | Requires nested form components |
