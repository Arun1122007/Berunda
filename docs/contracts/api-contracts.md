# API Contracts

> **Document ID:** BERUNDA-CONTRACT-001 | **Version:** 1.0 | **Status:** APPROVED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## API Versioning

- Header-based: `Accept: application/vnd.berunda.v1+json`
- Default version: `v1` (when header absent)
- URL prefix: `/api/v1/`

## Base URL

- Development: `http://localhost:8000/api/v1`
- Production: `https://api.berunda.example.com/api/v1`

## Standard Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | For protected routes | `Bearer {jwt_token}` |
| Content-Type | For requests with body | `application/json` |
| X-Correlation-ID | Recommended | UUID v4 for request tracing |

## Date and Time Formats

- Dates: `YYYY-MM-DD` (ISO 8601)
- Datetimes: `YYYY-MM-DDTHH:mm:ssZ` (ISO 8601 UTC)
- Timezone: IST (Asia/Kolkata) for display, UTC for storage

## Identifier Formats

| Entity | Format | Example |
|--------|--------|---------|
| UserID | Auto-increment integer | 1 |
| CaseMasterID | Auto-increment integer | 42 |
| CrimeNo | String: `CR-{year}-{number}` | CR-2026-0421 |
| CaseNo | String: `{number}/{year}` | 42/2026 |
| PersonEntityID | Auto-increment integer | 101 |

## Nullability Rules

- All fields in response may be null unless marked as required
- Create requests: required fields must be non-null
- Update requests: null fields are ignored (partial update)
- Boolean defaults to `false`
- Numeric defaults to `null`
- String defaults to `null`

## Pagination Rules

| Parameter | Default | Max | Description |
|-----------|---------|-----|-------------|
| page | 1 | - | Page number (1-indexed) |
| page_size | 20 | 100 | Items per page |

Response includes: `items`, `total`, `page`, `page_size`

## Sorting Rules

- Default: `CaseMasterID DESC` (newest first)
- Custom sorting deferred to Phase 3

## Filtering Rules

Filters passed as query parameters:
- `district_id` — filter by district
- `police_station_id` — filter by police station
- `status_id` — filter by case status

## Correlation IDs

- Generated client-side via `crypto.randomUUID()`
- Passed via `X-Correlation-ID` header
- Included in error responses as `requestId`
- Logged in backend logs for traceability
