# Alert Rules

## Alert Channels

Alerts are routed to:
- **Slack**: #berunda-alerts channel (immediate)
- **Email**: Distribution list (digest)
- **PagerDuty** (optional, for critical production alerts)

## Alert Rules

### 1. High Error Rate

| Field | Value |
|-------|-------|
| Condition | `http_requests_total{status=~"5.."} / http_requests_total > 0.05` |
| Duration | 5 minutes |
| Severity | Critical |
| Action | Slack + Email + PagerDuty |

### 2. High Latency

| Field | Value |
|-------|-------|
| Condition | `p99(http_request_duration_ms) > 5000` |
| Duration | 5 minutes |
| Severity | Warning |
| Action | Slack |

### 3. Service Down

| Field | Value |
|-------|-------|
| Condition | `up{service="api"} == 0` OR `up{service="worker"} == 0` |
| Duration | 1 minute |
| Severity | Critical |
| Action | Slack + Email + PagerDuty |

### 4. Model Drift

| Field | Value |
|-------|-------|
| Condition | `ai_accuracy < 0.80` (compared to 7-day rolling average) |
| Duration | 30 minutes |
| Severity | Warning |
| Action | Slack |

### 5. Data Freshness

| Field | Value |
|-------|-------|
| Condition | `time_since_last_update > 3600` (1 hour without new records) |
| Duration | 10 minutes |
| Severity | Warning |
| Action | Slack |

### 6. Cost Spike

| Field | Value |
|-------|-------|
| Condition | `daily_cost > budget_daily_limit * 1.5` |
| Duration | Immediate |
| Severity | Info |
| Action | Slack (digest) |

### 7. Rate Limit Exceeded

| Field | Value |
|-------|-------|
| Condition | `rate_limit_exceeded_total > 0` |
| Duration | 1 minute |
| Severity | Warning |
| Action | Slack |

### 8. Dependency Failure

| Field | Value |
|-------|-------|
| Condition | `external_api_errors_total > 10` (in 5 min window) |
| Duration | 5 minutes |
| Severity | Warning |
| Action | Slack |

## Alert Response

1. **Acknowledge** within 5 minutes (Critical) / 15 minutes (Warning).
2. **Investigate** using logs and traces.
3. **Resolve** with fix or workaround.
4. **Document** post-incident summary in the runbook.
