# Dashboards

## Available Dashboards

All dashboards are available in the Catalyst Console > Monitoring > Dashboards.

### 1. API Performance

Tracks:
- Request rate (rpm)
- P50/P95/P99 latency
- Error rate by endpoint
- Active connections
- Top slowest endpoints

### 2. Error Rates

Tracks:
- 4xx and 5xx error counts
- Error breakdown by service
- Unhandled exceptions
- Client vs. server errors
- Error trends (hourly/daily)

### 3. AI/ML Metrics

Tracks:
- Inference count per model
- Token usage (input/output)
- Model latency (P50/P95/P99)
- Model error rate
- Entity resolution match rate
- Embedding generation time

### 4. Data Quality

Tracks:
- Records processed per day
- Data freshness (time since last update)
- Duplicate detection rate
- Validation pass/fail rate
- Missing field percentage

### 5. Cost & Resource Usage

Tracks:
- Catalyst function invocations
- Data Store read/write units
- Stratus cache operations
- QuickML training hours
- AppSail inference time

## Creating Custom Dashboards

1. Go to Catalyst Console > Monitoring > Dashboards.
2. Click **Create Dashboard**.
3. Select metrics and visualize using line/bar/table/gauge.
4. Set auto-refresh interval (30s, 1m, 5m).
5. Share with team members or set as default.
