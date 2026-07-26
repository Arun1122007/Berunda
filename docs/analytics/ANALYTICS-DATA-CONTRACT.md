# Analytics Data Contract

> **Document ID:** BERUNDA-PH3-ANALYTICS-CONTRACT-001
> **Version:** 1.0

This contract defines the strict schema expected by front-end clients from the Analytics Engine APIs.

## Global KPI Response Wrapper
All KPIs endpoints (`/api/v1/analytics/overview`) will return data in this format:

```json
{
  "success": true,
  "data": {
    "metric": "TOTAL_FIRS",
    "label": "Total FIRs",
    "value": 1248,
    "previous_value": 1130,
    "absolute_change": 118,
    "percentage_change": 10.44,
    "trend": "UP"
  },
  "context": {
    "filters": {},
    "period": {
      "start": "2026-07-01",
      "end": "2026-07-31"
    },
    "scope": "DISTRICT",
    "freshness_timestamp": "2026-07-26T10:30:00+05:30",
    "data_status": "COMPLETE"
  }
}
```

## Trends Response Wrapper
All trend endpoints (`/api/v1/analytics/firs/trends`) will return data in this format:

```json
{
  "success": true,
  "data": [
    {
      "period_label": "2026-07-01",
      "value": 42
    },
    {
      "period_label": "2026-07-02",
      "value": 38
    }
  ],
  "context": {
    "aggregation_grain": "daily"
  }
}
```

## Geographic Bounding
All endpoints under `/api/v1/analytics/geography/` are subject to the privacy suppression rule:
> Any bounding box or station zone with fewer than 5 records for the requested time period will return `{ "status": "SUPPRESSED_DUE_TO_LOW_COUNT" }` rather than leaking potential identifying timelines.
