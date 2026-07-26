# Project Berunda — Catalyst Job Scheduling Specification

> **Document ID:** BERUNDA-DEP-006 | **Version:** 1.0  

---

## 1. Workload Registry

| Job Name | Schedule | Handler Endpoint | Description |
| :--- | :--- | :--- | :--- |
| `batch-risk-recompute` | Daily @ 02:00 IST | `/api/v1/jobs/risk-recompute` | Batch recomputes risk scores across active cases |
| `anomaly-detection-scan` | Hourly | `/api/v1/jobs/anomaly-scan` | Detects statistical anomalies in crime spikes |
| `audit-log-archival` | Weekly (Sun 00:00) | `/api/v1/jobs/audit-archive` | Archives older audit logs to cold storage |

---

## 2. Execution Safeguards

- **Authentication:** Scheduled triggers pass `X-Internal-Job-Secret` header.
- **Idempotency:** All job handlers use transaction locks and unique run keys.
- **Retries:** Failed jobs retry up to 3 times with exponential backoff.
