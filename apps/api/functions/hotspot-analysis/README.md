# hotspot-analysis

Compute crime hotspot data using Kernel Density Estimation (KDE) and hexbin aggregation with district and police-station drill-down.

## Trigger

**HTTP** — POST | **Cron** — Nightly recompute

### Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/hotspot/compute` | Compute hotspots for given period |
| GET | `/hotspot/data` | Get computed hotspot data |
| GET | `/hotspot/districts` | List available districts |

## Input Schema

```json
{
  "district": "string",
  "policeStation": "string",
  "crimeType": "string",
  "period": {
    "start": "ISO-8601",
    "end": "ISO-8601"
  },
  "resolution": "kde | hexbin (default: hexbin)",
  "gridSize": "number (default: 100)"
}
```

## Output Schema

```json
{
  "success": true,
  "data": [
    {
      "district": "string",
      "policeStation": "string",
      "crimeType": "string",
      "lat": 12.9716,
      "lng": 77.5946,
      "intensity": 0.85,
      "trend": "increasing",
      "period": "2026-Q2",
      "caseCount": 42
    }
  ]
}
```

## Error Codes

| Code | Status | Description |
|------|--------|-------------|
| VALIDATION_ERROR | 400 | Invalid period or district |
| NO_DATA | 404 | No data for the specified criteria |

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `HOTSPOT_GRID_SIZE` | `100` | Grid cells per degree |
| `HOTSPOT_BANDWIDTH` | `0.05` | KDE bandwidth in degrees |
| `HOTSPOT_CACHE_TTL` | `3600` | Cache TTL in seconds |

## Processing Flow

```
POST /hotspot/compute
  → Load geo-tagged cases for period
  → Apply KDE or hexbin aggregation
  → Compute intensity and trend
  → Store results in Data Store
  -> Update cache
  -> Return hotspot data
```
