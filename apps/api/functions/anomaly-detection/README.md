# anomaly-detection

Detect crime spikes using z-score analysis against historical baselines, grouped by crime type and location.

## Trigger

**HTTP** — POST | **Cron** — Hourly/daily check

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/anomalies/detect` | Run anomaly detection |
| GET | `/anomalies/recent` | Get recent anomaly alerts |
| POST | `/anomalies/acknowledge` | Acknowledge an alert |

## Input Schema

```json
{
  "district": "string",
  "crimeType": "string",
  "period": {
    "start": "ISO-8601",
    "end": "ISO-8601"
  },
  "baselineWindow": "number (default: 90)",
  "zScoreThreshold": 2.0
}
```

## Output Schema

```json
{
  "success": true,
  "data": [
    {
      "alertId": "string",
      "district": "string",
      "crimeType": "theft",
      "observedCount": 28,
      "expectedCount": 12.5,
      "zScore": 3.45,
      "severity": "high",
      "detectedAt": "2026-07-18T10:00:00Z",
      "period": "2026-07-18",
      "acknowledged": false
    }
  ]
}
```

## Severity Levels

| Z-Score | Severity | Action |
|---------|----------|--------|
| 1.5 - 2.0 | low | Monitor |
| 2.0 - 2.5 | medium | Flag |
| 2.5 - 3.0 | high | Investigate |
| > 3.0 | critical | Immediate action |

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| NO_BASELINE | 400 | Insufficient history for baseline |
| DETECTION_FAILED | 500 | Computation error |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `ANOMALY_BASELINE_DAYS` | `90` | Historical baseline window |
| `ANOMALY_Z_THRESHOLD` | `2.0` | Z-score alert threshold |

## Processing Flow

```
POST /anomalies/detect
  → Load current period case counts
  → Compute baseline from historical data
  → Calculate z-scores per group
  → Generate alerts for threshold breaches
  → Store alerts in Data Store
  -> Return anomaly results
```
