# API Design Specification

[//]: # (Document ID: BERUNDA-API-001 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, QA | Source: Architecture docs + SRS | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. API Style

RESTful JSON over HTTPS. All requests route through Catalyst API Gateway.

## 2. Base URL

```
https://{project}.catalystapps.io/api/v1
```

## 3. Authentication

All endpoints except public health check require a bearer token obtained from Catalyst Authentication.

```
Authorization: Bearer {token}
```

## 4. Standard Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token |
| Content-Type | Yes | application/json |
| X-Request-ID | No | Idempotency key for POST/PUT |
| X-Jurisdiction-Override | No | Compliance/Admin only: override jurisdiction filter |

## 5. Endpoints

### 5.1 Cases

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /cases | List cases (paginated, filterable) | Any authenticated |
| GET | /cases/{caseMasterID} | Get case details | Any authenticated |
| POST | /cases/import | Import FIR from CSV/JSON | SCRB Analyst, Admin |
| POST | /cases | Create case manually | SCRB Analyst, Admin |
| GET | /cases/{caseMasterID}/timeline | Case event timeline | Any authenticated |

### 5.2 Persons

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /persons | List PersonEntities (paginated) | Any authenticated |
| GET | /persons/{personEntityID} | Get person details + risk score | Any authenticated |
| GET | /persons/{personEntityID}/cases | Get all cases for this person | Any authenticated |
| GET | /persons/{personEntityID}/relationships | Get relationship graph for person | Any authenticated |
| GET | /persons/pending-review | Get grey-zone ER decisions | Investigator |
| PUT | /persons/{personEntityID}/review | Confirm/reject person merge | Investigator |
| POST | /persons/search | Search persons by name or criteria | Any authenticated |

### 5.3 Relationships

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /relationships | List relationship edges | Any authenticated |
| GET | /relationships/shortest-path | Compute shortest path between two persons | SCRB Analyst |
| GET | /relationships/network/{personEntityID} | Get ego network for a person | SCRB Analyst |

### 5.4 Geospatial

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /hotspots | Get hotspot layers (filterable by district, date) | Any authenticated |
| GET | /anomalies | Get anomaly alerts | Any authenticated |
| GET | /anomalies/{anomalyAlertID} | Get anomaly details | Any authenticated |

### 5.5 Risk

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /risk/scores | List risk scores (paginated) | Any authenticated |
| GET | /risk/scores/{personEntityID} | Get risk score + feature importance | Any authenticated |

### 5.6 RAG

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| POST | /rag/query | Submit natural language question | Any authenticated |
| GET | /rag/history | Get user's query history | Any authenticated |

### 5.7 Analytics

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /analytics/case-summary | Aggregate case statistics | Any authenticated |
| GET | /analytics/crime-distribution | Crime head breakdown | Any authenticated |
| GET | /analytics/temporal-trends | Time-series crime counts | Any authenticated |

### 5.8 Governance

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /audit-log | Search audit log | Compliance, Admin |
| GET | /fairness-checks | Get fairness check results | Compliance, Admin |

### 5.9 System

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | /health | Health check (no auth) | Public |
| GET | /info | System version, synthetic tag | Any authenticated |

## 6. Pagination

All list endpoints use cursor-based pagination:

**Request:**
```
GET /cases?cursor=eyJpZCI6MTAwfQ==&limit=50
```

**Response:**
```json
{
  "data": [...],
  "next_cursor": "eyJpZCI6MTUwfQ==",
  "has_more": true,
  "total_estimate": 5000
}
```

## 7. Error Response Format

```json
{
  "error": {
    "code": "ERR-0403",
    "message": "Insufficient permissions",
    "details": {
      "required_role": "SCRB_ANALYST",
      "current_role": "INVESTIGATOR"
    },
    "request_id": "req-abc-123"
  }
}
```

## 8. Rate Limiting

| Tier | Limit | Window |
|------|-------|--------|
| Public (health) | 60 requests | 1 minute |
| Authenticated | 300 requests | 1 minute |
| RAG queries | 20 requests | 1 minute |
| Administrative | 600 requests | 1 minute |

## 9. Versioning

API version is in the URL path (`/api/v1/`). Breaking changes increment the version number. Backward-compatible additions do not.
