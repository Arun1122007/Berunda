# fairness-check

Verify that AI/ML models exclude protected/sensitive fields and enforce role-based access restrictions.

## Trigger

**HTTP** — POST

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/fairness/check` | Run fairness check on model or dataset |
| GET | `/fairness/report` | Get latest fairness report |
| POST | `/fairness/validate-access` | Validate access control rules |

## Input Schema

```json
{
  "modelId": "string",
  "modelVersion": "string",
  "features": ["string"],
  "sensitiveFields": ["religion", "caste", "community"],
  "datasetRows": 1000
}
```

## Output Schema

```json
{
  "success": true,
  "data": {
    "hasSensitiveFields": false,
    "violations": [],
    "featureImportanceCheck": "passed",
    "roleRestrictionCheck": "passed",
    "recommendations": [
      "No sensitive fields detected in feature set"
    ],
    "checkedAt": "2026-07-18T10:00:00Z"
  }
}
```

## Validation Rules

| Rule | Description |
|------|-------------|
| Sensitive Field Exclusion | Model must not use religion, caste, community, ethnicity |
| Role Restriction | Risk scores must not be viewable by unauthorized roles |
| Demographic Parity | Score distribution should not show bias across districts |
| Explainability | All scores must have human-readable explanations |

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 400 | Invalid input |
| FAIRNESS_FAILED | 500 | Check computation error |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FAIRNESS_SENSITIVE_FIELDS` | `religion,caste,community,ethnicity` | Protected attributes |
| `FAIRNESS_REPORT_TTL` | `86400` | Report cache TTL |

## Processing Flow

```
POST /fairness/check
  → Load model metadata and features
  → Scan for sensitive field names
  → Check role assignment rules
  → Verify explanation quality
  → Generate fairness report
  -> Return check results
```
