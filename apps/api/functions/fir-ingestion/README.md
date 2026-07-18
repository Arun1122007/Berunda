# fir-ingestion

Import and validate FIR (First Information Report) data into the Berunda platform.

## Trigger

**HTTP** — POST

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/fir/import` | Import FIR data (JSON/CSV) |
| POST | `/fir/validate` | Validate FIR data without importing |

## Input Schema

### POST /fir/import

```json
{
  "firs": [
    {
      "caseNumber": "string (required)",
      "district": "string (required)",
      "policeStation": "string (required)",
      "dateFiled": "ISO-8601 string (required)",
      "sections": ["string"],
      "narrative": "string (required)",
      "metadata": {}
    }
  ],
  "source": "string (csv | json)",
  "triggerExtraction": "boolean (default: true)"
}
```

### POST /fir/validate

Same schema as import — returns validation errors without persisting.

## Output Schema

```json
{
  "success": true,
  "data": {
    "imported": 42,
    "failed": 1,
    "errors": [
      {
        "index": 3,
        "field": "caseNumber",
        "message": "Case number is required"
      }
    ],
    "triggeredExtraction": true
  }
}
```

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 400 | Invalid input data |
| IMPORT_ERROR | 500 | Data store write failure |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `FIR_BATCH_SIZE` | `100` | Maximum FIRs per import batch |
| `TRIGGER_NER` | `true` | Auto-trigger NER extraction on import |

## Processing Flow

```
POST /fir/import
  → Validate schema
  → Check for duplicate case numbers
  → Store in Catalyst Data Store
  → Trigger ner-extraction (if enabled)
  → Update hotspot-analysis cache
  → Return import summary
```
