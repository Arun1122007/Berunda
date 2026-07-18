# Monitoring and Observability

## Overview

Berunda uses a three-pillar observability strategy: logging, metrics, and tracing. All telemetry is shipped to Catalyst's built-in monitoring tools.

## Architecture

```
┌─────────────┐   ┌──────────────┐   ┌────────────────┐
│ Application │──▶│ Structured   │──▶│ Catalyst Logs  │
│ (Functions) │   │ Log (JSON)   │   │ (Console)      │
├─────────────┤   ├──────────────┤   ├────────────────┤
│ Metrics     │──▶│ StatsD/      │──▶│ Catalyst       │
│ (Invocations)│   │ Prometheus   │   │ Metrics        │
├─────────────┤   ├──────────────┤   ├────────────────┤
│ Distributed │──▶│ OpenTelemetry│──▶│ Catalyst Trace │
│ Tracing     │   │ (W3C Trace)  │   │ (AppSail)      │
├─────────────┤   ├──────────────┤   ├────────────────┤
│ Alerts      │──▶│ Alert Rules  │──▶│ Slack / Email  │
└─────────────┘   └──────────────┘   └────────────────┘
```

## Pillars

### 1. Logging (Structured JSON)

Every log entry includes:
- `timestamp`, `level`, `message`, `logger`
- `request_id` (correlation ID)
- `service`, `environment`
- `function_name`, `duration_ms`
- `user_id`, `entity_id` (if applicable)

See `monitoring/logging/README.md` for standards.

### 2. Metrics

| Metric | Type | Labels |
|--------|------|--------|
| `http_requests_total` | Counter | method, path, status, service |
| `http_request_duration_ms` | Histogram | method, path, service |
| `http_requests_in_flight` | Gauge | service |
| `entity_resolutions_total` | Counter | status (match/non-match) |
| `entity_resolution_duration_ms` | Histogram | — |
| `ai_inference_total` | Counter | model, status |
| `ai_inference_duration_ms` | Histogram | model |
| `ai_token_usage_total` | Counter | model |
| `database_query_duration_ms` | Histogram | operation, table |
| `cache_hit_ratio` | Gauge | cache_name |

### 3. Tracing (Distributed)

- Trace context propagated via `W3C Trace-Context` headers.
- Spans for: HTTP request, database query, cache access, AI inference, entity resolution.
- Traces sampled at rates per environment (dev: 100%, staging: 50%, prod: 10%).

## Dashboards

Available dashboards are documented in `monitoring/dashboards/README.md`.

## Alerts

Alert rules are documented in `monitoring/alerts/README.md`.
