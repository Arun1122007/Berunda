# audit-logging

Immutable audit trail for sensitive read operations and AI-generated outputs. Provides tamper-evident logging with chain hashing.

## Trigger

**HTTP** — POST | **Event** — Called by other functions via middleware

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/audit/log` | Record an audit event |
| GET | `/audit/logs` | Query audit logs with filters |
| GET | `/audit/verify` | Verify audit log integrity |

## Input Schema

```json
{
  "userId": "string (required)",
  "action": "string (required)",
  "resource": "string (required)",
  "resourceId": "string (required)",
  "details": {},
  "ipAddress": "string",
  "userAgent": "string"
}
```

## Output Schema

```json
{
  "success": true,
  "data": {
    "auditId": "string",
    "previousHash": "string",
    "currentHash": "string",
    "timestamp": "2026-07-18T10:00:00Z"
  }
}
```

## Audit Actions

| Action | Description |
|--------|-------------|
| `case.read` | Case record accessed |
| `person.search` | Person entity searched |
| `risk.score.view` | Risk score viewed |
| `rag.query` | AI query executed |
| `report.generate` | Report generated |
| `admin.config.change` | Configuration modified |
| `user.login` | User authentication |

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 400 | Missing required fields |
| INTEGRITY_ERROR | 500 | Chain hash verification failed |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AUDIT_RETENTION_DAYS` | `365` | Log retention period |
| `AUDIT_HASH_ALGO` | `sha256` | Hashing algorithm for chain |

## Processing Flow

```
POST /audit/log
  → Validate event payload
  → Load previous entry hash
  → Compute current hash (chain)
  → Store immutable log entry
  -> Return audit receipt
```
