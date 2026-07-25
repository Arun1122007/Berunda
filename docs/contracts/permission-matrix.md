# Permission Matrix

> **Document ID:** BERUNDA-CONTRACT-005 | **Version:** 1.0 | **Status:** APPROVED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## Roles

| Role | Code | Description |
|------|------|-------------|
| Admin | `admin` | Full system access |
| SCRB Analyst | `analyst` | State-level crime analyst |
| Investigating Officer | `officer` | District-level officer |
| Unauthenticated | `anonymous` | No valid token |

## Permission Matrix

| Endpoint | Method | anonymous | officer | analyst | admin |
|----------|--------|-----------|---------|---------|-------|
| /api/v1/auth/login | POST | ✅ | - | - | - |
| /api/v1/auth/register | POST | ✅ | - | - | - |
| /api/v1/auth/refresh | POST | ✅ | - | - | - |
| /api/v1/auth/logout | POST | - | ✅ | ✅ | ✅ |
| /api/v1/auth/me | GET | - | ✅ | ✅ | ✅ |
| /api/v1/fir | GET | - | ✅ (scoped) | ✅ (all) | ✅ (all) |
| /api/v1/fir/{id} | GET | - | ✅ (scoped) | ✅ (all) | ✅ (all) |
| /api/v1/fir | POST | - | ❌ | ✅ | ✅ |
| /api/v1/fir/{id} | PUT | - | ❌ | ✅ (status) | ✅ |
| /api/v1/fir/{id} | DELETE | - | ❌ | ❌ | ✅ |

## Scoping Rules

- `officer` role: `district_id` in JWT must match the case's district
- `analyst` role: No restrictions — all records visible
- `admin` role: No restrictions — full access

## Enforcement Points

| Layer | Mechanism |
|-------|-----------|
| API Gateway | CORS, rate limiting |
| Backend Router | `get_current_user` dependency extracts JWT payload |
| Backend Service | `require_role` decorator checks role against allowed list |
| Database Query | `district_id` filter applied in service layer for officer role |
