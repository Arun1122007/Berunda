# ner-extraction

Extract named entities from FIR narratives using spaCy-based NLP pipeline.

## Trigger

**HTTP** — POST | **Event** — Triggered by fir-ingestion

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/ner/extract` | Extract entities from FIR narrative |
| POST | `/ner/extract-batch` | Batch extraction for multiple FIRs |

## Input Schema

```json
{
  "firId": "string (required)",
  "caseNumber": "string",
  "narrative": "string (required)",
  "language": "string (default: hi/en)"
}
```

### Batch input

```json
{
  "firs": [{ "firId": "string", "narrative": "string" }]
}
```

## Output Schema

```json
{
  "success": true,
  "data": {
    "firId": "string",
    "persons": [
      {
        "name": "string",
        "mentions": ["string"],
        "role": "accused | victim | witness | complainant | informant",
        "confidence": 0.95
      }
    ],
    "vehicles": [
      {
        "registrationNumber": "string",
        "type": "string",
        "confidence": 0.85
      }
    ],
    "locations": [
      {
        "name": "string",
        "type": "crime-scene | residence | other",
        "confidence": 0.9
      }
    ],
    "organizations": [{ "name": "string", "confidence": 0.7 }],
    "dates": [{ "value": "ISO-8601", "confidence": 0.8 }],
    "processingTimeMs": 245
  }
}
```

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 400 | Missing or invalid narrative |
| NER_FAILED | 500 | SpaCy model returned no results |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `NER_MODEL` | `en_core_web_sm` | spaCy model to use |
| `NER_MIN_CONFIDENCE` | `0.5` | Minimum confidence threshold |

## Processing Flow

```
POST /ner/extract
  → Validate input
  → Load spaCy pipeline
  → Extract persons, vehicles, locations, orgs, dates
  → Classify person roles using heuristics
  → Store entities in Catalyst Data Store
  → Trigger entity-resolution
  → Return extracted entities
```
