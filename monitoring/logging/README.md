# Logging Standards

## Log Levels

| Level | Usage |
|-------|-------|
| `ERROR` | Unhandled exceptions, service failures, data corruption |
| `WARN` | Recoverable errors, degraded performance, rate limiting |
| `INFO` | Significant lifecycle events: startup, shutdown, deploy, user actions |
| `DEBUG` | Detailed diagnostic information (development only) |
| `TRACE` | Very fine-grained tracing (rarely used) |

## Required Fields

Every log entry MUST include:

```json
{
  "timestamp": "2024-01-15T10:00:00.000Z",
  "level": "INFO",
  "message": "FIR record processed",
  "logger": "berunda.api.fir",
  "request_id": "req-abc123def456",
  "service": "api",
  "environment": "production",
  "function_name": "process_fir",
  "duration_ms": 245
}
```

## PII Handling

**Never log the following fields in plain text:**
- Aadhaar numbers
- Phone numbers
- Full addresses (street-level)
- Email addresses
- Biometric data
- Authentication tokens
- Session IDs

If these must be logged for debugging, use **masked** format:
- Phone: `+91-98765*****`
- Aadhaar: `XXXX-XXXX-1234`
- Email: `u***@example.com`

## Log Retention

| Environment | Retention | Shipped To |
|-------------|-----------|------------|
| Development | 7 days | Local files |
| Staging | 30 days | Catalyst Logs |
| Production | 90 days | Catalyst Logs + Cold storage |

## Log Shipping

Logs are shipped to Catalyst via:
1. **Stdout** — Catalyst Functions automatically capture stdout as logs.
2. **File** — Rotating file handler for local debugging.
3. **Sentry** — Error events sent to Sentry for aggregation.

## Structured Logging Format

Use the following Go-style structured logging pattern:

```python
# Python example
logger.info("fir_record_processed",
    fir_id="FIR2024001",
    crime_type="burglary",
    officer_id="OFF001",
    duration_ms=145
)
```

Outputs:
```json
{
  "timestamp": "2024-01-15T10:00:00.000Z",
  "level": "INFO",
  "message": "fir_record_processed",
  "fir_id": "FIR2024001",
  "crime_type": "burglary",
  "officer_id": "OFF001",
  "duration_ms": 145
}
```
