# risk-scoring

Compute repeat-offender risk scores using QuickML AutoML with explainable features.

## Trigger

**HTTP** — POST | **Cron** — Nightly batch recompute

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/risk/score` | Compute risk score for a person |
| POST | `/risk/score-batch` | Batch score computation |
| GET | `/risk/scores` | List recent risk scores |

## Input Schema

```json
{
  "personId": "string (required)",
  "recompute": "boolean (default: false)"
}
```

## Output Schema

```json
{
  "success": true,
  "data": {
    "personId": "string",
    "score": 0.82,
    "level": "high",
    "features": {
      "priorCases": 5,
      "recencyDays": 30,
      "crimeTypeDiversity": 3,
      "geographicSpread": 2,
      "violenceIndicator": 1,
      "repeatCycleDays": 45
    },
    "explanation": "Subject has 5 prior cases across 3 crime types with 45-day repeat cycle",
    "computedAt": "2026-07-18T10:00:00Z",
    "modelVersion": "v1.2.0"
  }
}
```

## Risk Levels

| Score Range | Level | Action |
|-------------|-------|--------|
| 0.0 - 0.3 | low | Standard monitoring |
| 0.3 - 0.6 | medium | Enhanced monitoring |
| 0.6 - 0.85 | high | Flag for investigation |
| 0.85 - 1.0 | critical | Immediate review required |

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| NOT_FOUND | 404 | Person not found |
| SCORE_FAILED | 500 | Model inference error |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `RISK_MODEL_ID` | — | QuickML AutoML model ID |
| `RISK_CACHE_TTL` | `86400` | Score cache TTL in seconds |

## Processing Flow

```
POST /risk/score
  → Load person profile + case history
  → Extract feature vector
  → Call QuickML AutoML model
  → Generate explanation text
  → Store score in Data Store
  → Return scored result
```
