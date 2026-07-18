# Data Quality, Profiling, and Validation Plan

[//]: # (Document ID: BERUNDA-DATA-007 | Version: 1.0 | Status: DRAFT | Classification: INTERNAL | Owner: Berunda Team | Audience: Developers, Data Engineers, QA | Source: SRS requirements | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Purpose

Define automated and manual checks to ensure synthetic data quality before import and during operation. Since all data is synthetic, data quality here means: (a) structural validity, (b) referential integrity, (c) realistic distributions, and (d) no accidental PII contamination from Faker's PRNG state.

## 2. Pre-Import Validation (SQL-level)

Run before importing any synthetic data into Catalyst Data Store.

| Check ID | Check | SQL / Rule | Severity | Action on Failure |
|----------|-------|-----------|----------|-------------------|
| DQ-001 | PK uniqueness | `SELECT COUNT(*) - COUNT(DISTINCT PK)` per table | BLOCKING | Abort import; fix generator |
| DQ-002 | FK referential integrity | All FK values must exist in parent table | BLOCKING | Abort import; fix generator |
| DQ-003 | NOT NULL violations | `SELECT * FROM table WHERE required_column IS NULL` | BLOCKING | Abort import; fix generator |
| DQ-004 | Data type conformance | `SELECT * FROM table WHERE column NOT LIKE pattern` for VARCHAR length, INT range | WARNING | Log + continue |
| DQ-005 | CrimeNo format | `SELECT * FROM CaseMaster WHERE CrimeNo NOT REGEXP '^[0-9]{18}$'` | BLOCKING | Abort import; fix CrimeNo generator |
| DQ-006 | Date sanity | `CrimeRegisteredDate <= GETDATE()` and `IncidentFromDate <= IncidentToDate` | WARNING | Log; review specific rows |
| DQ-007 | Latitude/Longitude range | `Latitude BETWEEN 11.5 AND 18.5 AND Longitude BETWEEN 74 AND 78.5` (Karnataka bounds) | WARNING | Log; fix generator |

## 3. Post-Import Profiling

Run after data is loaded to verify expected distributions.

| Profile ID | Profile | Expected Range | Action on Deviation |
|-----------|---------|---------------|-------------------|
| PR-001 | Total FIR count | 2,000 - 5,000 | Flag for manual review |
| PR-002 | Crime head distribution | Within ±5% of target per head | Log + document in demo notes |
| PR-003 | Gender ratio (complainants) | 60-70% Male, 30-40% Female | Informational only |
| PR-004 | Age distribution | 18-60 years, peak at 25-40 | Log + document |
| PR-005 | Cases per district | Even ±30% across districts | Log + document in demo notes |
| PR-006 | Arrest rate | 50-70% of accused have arrest records | Informational |
| PR-007 | Chargesheet rate (closed cases) | 40-60% | Informational |
| PR-008 | Planted link count | 20-30 planted test cases verified | Run planting manifest verification |

## 4. Operational Data Quality Monitoring

| Check | Frequency | Description |
|-------|-----------|-------------|
| Referential integrity scan | Weekly (Cron) | Detect orphaned records in int_* tables |
| RiskScore completeness | Per computation | Verify every int_PersonEntity with cases has a risk score |
| AnomalyAlert recency | Per Cron run | Verify alerts computed for latest week |
| RAGCorpusChunk coverage | Per ingestion | Verify every CaseMaster.BriefFacts has at least one chunk |
| AuditLog completeness | Per action | Spot-check that audit log has expected entries |

## 5. Demo-Day Validation Script

A single command (`python scripts/validate_demo_data.py`) runs a comprehensive check before the demo:

```
Checklist:
  [✓] 2,000-5,000 FIRs loaded
  [✓] All FKs valid
  [✓] Planted hidden links present (20-30)
  [✓] Entity resolution finds planted matches
  [✓] Risk scores computed for all PersonEntities
  [✓] Anomaly spike present in target district-week
  [✓] RAG corpus indexed
  [✓] No CasteID/ReligionID in risk score features
  [✓] Audit log entries exist for all major actions
  [✓] Synthetic data tag present
```

Output: `PASS` or `FAIL` with per-check detail.

## 6. Data Freshness SLAs

| Data Type | Freshness SLA | Mechanism |
|-----------|--------------|-----------|
| Source zone (src_*) | As-imported (static for demo) | Synthetic data generated once |
| PersonEntity (int_*) | Within 5 minutes of NER extraction | Triggered by ingestion function |
| RiskScore (int_*) | Within 1 hour of new PersonEntity creation | Cron-triggered batch or event-triggered |
| HotspotLayer (int_*) | Daily (nightly Cron) | Cron schedule |
| AnomalyAlert (int_*) | Daily (nightly Cron) | Cron schedule |
| RAGCorpusChunk (int_*) | Within 5 minutes of case ingestion | Triggered by ingestion function |
