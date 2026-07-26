# Phase 6 — Authentication and Authorization Report

## 1. Authentication

**Mechanism:** JWT (HS256) with access + refresh tokens

**Implementation:** `src/middleware/auth.py`

**Flow:**
1. User registers via `POST /api/v1/auth/register`
2. User logs in via `POST /api/v1/auth/login` → receives access token (15min) + refresh token (1 day)
3. All protected routes extract JWT from `Authorization: Bearer <token>` header
4. Token refresh via `POST /api/v1/auth/refresh`

**Protections:**
- Missing credentials → 401
- Invalid/expired credentials → 401
- Disabled users rejected at login
- Weak JWT secrets detected at startup with warnings

## 2. Authorization

**Mechanism:** Role-Based Access Control (RBAC) via `require_role()` decorator

**Roles:**
| Role | Description |
|------|-------------|
| `admin` | Full system access |
| `officer` | FIR CRUD, notes, evidence |
| `supervisor` | Review, assignment, oversight |
| `analyst` | Search, dashboard, audit read |

**Authorization Matrix:**

| Resource | Create | View | List | Update | Delete | Assign | Review |
|----------|--------|------|------|--------|--------|--------|--------|
| FIR | admin/officer | All auth | All auth | admin/officer | admin | - | - |
| Notes | admin/officer | All auth | All auth | - | - | - | - |
| Assignments | admin/supervisor | All auth | All auth | - | - | - | - |
| Reviews | admin/supervisor | All auth | All auth | - | - | - | - |
| Evidence | admin/officer | All auth | All auth | - | - | - | - |
| Audit | admin/analyst | - | admin/analyst | - | - | - | - |
| Reports | admin/officer/supervisor/analyst | All auth | All auth | - | - | - | - |
| Admin | admin | - | - | admin | admin | - | - |
| AI Review | - | All auth | - | - | - | - | supervisor/admin |

**District Scoping:**
Non-admin users are scoped to their assigned district via `district_id` in JWT payload. All list/search queries filter by district automatically.

## 3. New Authorization Features (Phase 6)

- FIR lifecycle state machine enforced status transitions
- Police stations and persons routes use standard RBAC
- All existing authorization tests pass (246 tests)
