# Event and Job Contracts

[//]: # (Document ID: BERUNDA-API-003 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, QA | Source: Architecture docs + SRS | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Event Types (Phase 3+ Target)

Phase 1 uses synchronous function calls only. Event-driven patterns are documented here for Phase 3+ migration.

### 1.1 Catalyst Signals Events (Future)

| Event | Producer | Consumer(s) | Payload |
|-------|----------|-------------|---------|
| case.ingested | FIR Ingestion Function | NER Function, Entity Resolution Function | `{ caseMasterId: int, crimeNo: string }` |
| entity.resolved | Entity Resolution Function | Risk Scoring Function, Graph Update Function | `{ personEntityId: int, linkCount: int }` |
| risk.score.computed | Risk Scoring Function | Alert Function, Dashboard Update | `{ personEntityId: int, score: float, modelVersion: string }` |
| anomaly.detected | Anomaly Detection Function | Alert Function, Notification Function | `{ anomalyAlertId: int, zScore: float, districtId: int }` |

### 1.2 Phase 1 Function Call Contracts

In Phase 1, event triggers are replaced by direct function calls from the ingestion pipeline.

```
Ingestion Function
  → NER Function (direct HTTP call)
    → Entity Resolution Function (direct HTTP call)
  → Audit Log (direct write)
```

## 2. Cron Job Schedule

| Job ID | Name | Cron Expression | Function | Description |
|--------|------|----------------|----------|-------------|
| CRON-001 | Nightly Hotspot Recompute | `0 2 * * *` (daily 2 AM) | Hotspot Function | Recompute hexbin/KDE layers from CaseMaster data |
| CRON-002 | Nightly Anomaly Detection | `0 3 * * *` (daily 3 AM) | Anomaly Detection Function | Compute z-scores for each district-crime head-week |
| CRON-003 | Nightly Risk Scoring (full) | `0 4 Sat * *` (weekly Sat 4 AM) | Risk Scoring Function | Recompute risk scores for all PersonEntities |
| CRON-004 | Daily Fairness Check | `0 5 * * *` (daily 5 AM) | Fairness Check Function | Verify model exclusion + access control |
| CRON-005 | Synthetic Data Tag Verification | `0 6 * * *` (daily 6 AM) | Governance Function | Verify synthetic data tag is present |

### 2.1 Job Contract Format

```json
{
  "job": "CRON-001",
  "name": "Nightly Hotspot Recompute",
  "schedule": "0 2 * * *",
  "function": "hotspot-compute",
  "input": {
    "period": "weekly",
    "aggregation": "hexbin",
    "parameters": {
      "grid_size": 500,
      "bandwidth": 0.5
    }
  },
  "timeout_seconds": 300,
  "retry_count": 2,
  "on_failure": "email_notify"
}
```

### 2.2 Job Output Contract

```json
{
  "job": "CRON-001",
  "execution_id": "exec-20260717-020000-abc123",
  "status": "completed",
  "started_at": "2026-07-17T02:00:00Z",
  "completed_at": "2026-07-17T02:03:42Z",
  "result": {
    "tiles_updated": 1240,
    "districts_covered": 7,
    "weeks_computed": 104
  },
  "errors": []
}
```

## 3. Processing Guarantees

| Job | Guarantee | Rationale |
|-----|-----------|-----------|
| Hotspot Recompute | At-least-once | Idempotent — recompute overwrites existing tiles |
| Anomaly Detection | At-least-once | Idempotent — same inputs produce same z-scores |
| Risk Scoring | At-least-once | Idempotent — same PersonEntity + same data → same score |
| Fairness Check | At-least-once | Stateless check — same input → same result |

## 4. Data Import Contract

### 4.1 Import Request

```json
{
  "file_type": "csv",
  "data": [base64_encoded_csv],
  "options": {
    "skip_duplicate_check": false,
    "dry_run": false,
    "trigger_ner": true,
    "trigger_entity_resolution": true
  }
}
```

### 4.2 Import Response

```json
{
  "status": "completed",
  "cases_imported": 150,
  "cases_skipped_duplicate": 2,
  "ner_entities_extracted": 420,
  "person_entities_created": 180,
  "person_entities_linked": 150,
  "errors": [
    {
      "row": 47,
      "field": "CrimeRegisteredDate",
      "error": "Invalid date format: '2024/13/01'",
      "action": "skipped"
    }
  ],
  "import_id": "imp-20260717-abc456"
}
```

## 5. RAG Query Contract

### 5.1 Request

```json
{
  "question": "How many FIRs in Bengaluru Urban this year?",
  "options": {
    "max_chunks": 5,
    "include_citations": true,
    "include_raw_context": false
  }
}
```

### 5.2 Response

```json
{
  "answer": "There were 342 FIRs registered in Bengaluru Urban district between January 1, 2026 and July 17, 2026.",
  "citations": [
    {
      "case_no": "2026000156",
      "crime_no": "1044300062026000156",
      "chunk_index": 1,
      "relevance_score": 0.92
    }
  ],
  "confidence": "high",
  "processing_time_ms": 2340
}
```
