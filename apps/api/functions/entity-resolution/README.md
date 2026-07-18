# entity-resolution

Resolve person entities across cases using blocking and weighted scoring to identify repeat offenders and connected individuals.

## Trigger

**HTTP** — POST | **Event** — Triggered by ner-extraction

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/entities/resolve` | Resolve a new entity against existing records |
| POST | `/entities/resolve-batch` | Batch resolution |

## Input Schema

```json
{
  "entity": {
    "name": "string (required)",
    "aliases": ["string"],
    "age": "number",
    "gender": "string",
    "addresses": ["string"],
    "phoneNumbers": ["string"],
    "idMarks": ["string"],
    "firId": "string",
    "caseNumber": "string"
  },
  "threshold": "number (default: 0.75)"
}
```

## Output Schema

```json
{
  "success": true,
  "data": {
    "resolvedTo": {
      "entityId": "string",
      "name": "string",
      "matchScore": 0.89
    },
    "isNew": false,
    "candidates": [
      {
        "entityId": "string",
        "name": "string",
        "score": 0.89,
        "matchingFeatures": ["name", "phone", "address"]
      }
    ],
    "requiresReview": false
  }
}
```

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 400 | Missing entity data |
| RESOLUTION_FAILED | 500 | Internal matching error |

## Scoring Features

| Feature | Weight | Description |
|---------|--------|-------------|
| name_similarity | 0.40 | Fuzzy string match on name |
| phone_match | 0.20 | Phone number overlap |
| address_match | 0.15 | Address similarity |
| id_mark_match | 0.15 | ID marks comparison |
| age_proximity | 0.10 | Age range tolerance (5 years) |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `RESOLUTION_THRESHOLD` | `0.75` | Auto-link confidence threshold |
| `REVIEW_THRESHOLD` | `0.5` | Flag for manual review below this |
| `BLOCKING_KEYS` | `["phone_normalized", "name_initials"]` | Blocking key columns |

## Processing Flow

```
POST /entities/resolve
  → Normalize input (name, phone, address)
  → Generate blocking keys
  → Retrieve candidate blocks from Data Store
  → Compute weighted similarity scores
  → Apply threshold rules
  → Auto-link or flag for review
  → Update entity relationships
  → Return resolution result
```
