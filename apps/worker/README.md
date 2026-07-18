# @berunda/worker — Background Job Processor

Background job processor for the Berunda Crime Intelligence Platform, triggered by Catalyst Cron schedules.

## Jobs

| Job | Schedule | Description |
|-----|----------|-------------|
| `nightly-hotspot-recompute` | Daily 02:00 | Recompute hotspot KDE/hexbin data |
| `data-freshness-check` | Hourly | Verify data store sync and freshness |
| `report-generation` | Daily 06:00 | Generate scheduled PDF/CSV reports |
| `anomaly-scan` | Every 4 hours | Run anomaly detection pipeline |
| `risk-batch-update` | Daily 03:00 | Batch recompute risk scores |
| `audit-log-archive` | Weekly | Archive and compress old audit logs |

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Runtime | Zoho Catalyst (Node.js) |
| Triggers | Catalyst Cron |
| Data Store | Catalyst Data Store |
| Logging | Structured JSON logger |

## Prerequisites

- Zoho Catalyst account with project access
- Node.js >= 18
- Catalyst CLI (`npm install -g catalyst-cli`)

## Getting Started

```bash
npm install
```

## Job Definitions

### `nightly-hotspot-recompute`

Runs daily at 02:00. Iterates over all districts and recomputes hotspot data for the past 90 days using the hotspot-analysis function's core logic.

```json
{
  "job": "nightly-hotspot-recompute",
  "schedule": "0 2 * * *",
  "timeout": 600000
}
```

### `data-freshness-check`

Runs hourly. Checks that:
- FIR data is synced from source systems
- NER extraction is complete for recent FIRs
- Entity resolution is up to date
- Scores and alerts are current

### `report-generation`

Runs daily at 06:00. Generates:
- District crime summary reports (PDF)
- Weekly trends report (CSV)
- Risk score change log (CSV)
- Anomaly alert digest (PDF)

## Deployment

```bash
# Deploy cron jobs
catalyst cron:deploy

# List scheduled jobs
catalyst cron:list

# View job logs
catalyst cron:logs --job nightly-hotspot
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKER_MAX_CONCURRENCY` | `5` | Max parallel job execution |
| `WORKER_RETRY_MAX` | `3` | Max retries for failed jobs |
| `WORKER_RETRY_DELAY` | `30000` | Delay between retries (ms) |
| `REPORT_OUTPUT_DIR` | `/tmp/reports` | Generated report output path |

## Job Lifecycle

```
Cron Trigger
  → Worker picks up job
  → Execute job logic
  → Log success/failure
  → Send notification on failure
  → Update job status in Data Store
```
