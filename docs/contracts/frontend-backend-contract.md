# Frontend-Backend Contract

> **Document ID:** BERUNDA-CONTRACT-002 | **Version:** 1.0 | **Status:** APPROVED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## Frontend Configuration

```typescript
// Environment variables
VITE_API_BASE_URL="/api/v1"       // Proxy in dev, same-origin in prod
VITE_API_URL="http://localhost:8000"  // Direct backend URL
```

The Vite dev server proxies `/api` requests to `http://localhost:8000`.

## API Client

Frontend uses a centralized `ApiClient` class in `src/services/api-client.ts`:

```typescript
class ApiClient {
  async get<T>(endpoint: string, config?): Promise<T>
  async post<T>(endpoint: string, body?, config?): Promise<T>
  async put<T>(endpoint: string, body?, config?): Promise<T>
  async delete<T>(endpoint: string, config?): Promise<T>
}
```

## Auth Token Flow

```
1. Login → POST /api/v1/auth/login → { token, refreshToken, expiresIn, user }
2. Token stored in localStorage as "auth_token"
3. Refresh token stored as "refresh_token"
4. All API requests include "Authorization: Bearer {token}" header
5. On 401 → attempt POST /api/v1/auth/refresh → if fails, redirect to /login
```

## Type Sharing Strategy

- Backend schemas (Pydantic) are the source of truth
- Frontend types are manually maintained in `src/types/api.ts`
- A shared schema package is deferred to Phase 3
- Type generation from OpenAPI spec is deferred to Phase 3

## Naming Convention Mapping

| Backend (snake_case) | Frontend (camelCase) |
|---------------------|---------------------|
| CaseMasterID | caseMasterId |
| CrimeNo | crimeNo |
| CrimeRegisteredDate | crimeRegisteredDate |
| PoliceStationID | policeStationId |
| CaseStatusID | caseStatusId |
| CrimeMajorHeadID | crimeMajorHeadId |
| CrimeMinorHeadID | crimeMinorHeadId |
| BriefFacts | briefFacts |
| UserID | userId |
| PersonEntityID | personEntityId |

## Field Mapping Rules

The Pydantic `APIBase` class uses an alias generator that converts `snake_case` to `camelCase` automatically on serialization. The frontend receives camelCase properties and sends them back as camelCase.

## Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "detail": {
      "field": "crimeNo",
      "error": "Field required"
    },
    "requestId": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```
