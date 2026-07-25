# Error Contract

> **Document ID:** BERUNDA-CONTRACT-004 | **Version:** 1.0 | **Status:** APPROVED
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## Error Response Format

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "detail": {},
    "requestId": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

## Error Codes

| HTTP Status | Code | Description | When |
|-------------|------|-------------|------|
| 400 | BAD_REQUEST | Malformed request | Invalid JSON, missing body |
| 401 | AUTHENTICATION_ERROR | Not authenticated | Missing/invalid token |
| 403 | FORBIDDEN | Not authorized | Valid token but insufficient role |
| 404 | NOT_FOUND | Resource not found | Invalid ID in URL |
| 409 | CONFLICT | Resource conflict | Duplicate CrimeNo |
| 422 | VALIDATION_ERROR | Invalid input | Schema validation failure |
| 429 | RATE_LIMIT_EXCEEDED | Too many requests | RAG endpoint rate limit |
| 500 | INTERNAL_ERROR | Unexpected error | Unhandled exception |
| 502 | EXTERNAL_SERVICE_ERROR | External service failed | AI service unavailable |
| 503 | AI_SERVICE_UNAVAILABLE | AI service down | LLM/NER not reachable |

## Safe Response Fields

**Never include:**
- Stack traces
- SQL statements
- Internal file paths
- Secret values
- Database connection strings
- Full query parameters

**Always include:**
- Error code (machine-readable)
- Message (human-readable, safe)
- Optional detail object
- Correlation/Request ID

## Validation Error Detail

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Input validation failed",
    "detail": {
      "fields": {
        "crimeNo": "Field required",
        "briefFacts": "String should have at most 5000 characters"
      }
    },
    "requestId": "550e8400-e29b-41d4-a716-446655440000"
  }
}
```

## Error Handling by Layer

| Layer | Strategy |
|-------|----------|
| Frontend | `ApiError` class with status, message, correlationId |
| Backend Controller | Catch `BerundaError` subclasses, map to HTTP response |
| Backend Middleware | Global exception handler catches all unhandled exceptions |
| Database | SQLAlchemy exceptions caught in service layer |
