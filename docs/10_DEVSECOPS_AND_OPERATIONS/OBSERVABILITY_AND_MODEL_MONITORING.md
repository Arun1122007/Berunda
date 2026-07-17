# Observability and Model Monitoring

[//]: # (Document ID: BERUNDA-OPS-003 | Status: DRAFT | Classification: INTERNAL)

---

## 1. Observability Stack

| Capability | Phase 1 Tool | Phase 3+ Target |
|------------|-------------|-----------------|
| Application metrics | Catalyst Function logs + AuditLog | Prometheus + Grafana |
| API metrics | Catalyst API Gateway dashboard | API Gateway + Datadog |
| Database metrics | Catalyst Data Store console | Percona Monitoring |
| Model metrics | Custom Python logging to AuditLog | MLflow + Prometheus |
| Uptime monitoring | Custom health check endpoint | Pingdom / Statuspage |
| Error tracking | Catalyst Function error logs | Sentry |

## 2. Health Check Endpoint

`GET /health` returns:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "checks": {
    "database": { "status": "ok", "latency_ms": 12 },
    "catalyst_functions": { "status": "ok" },
    "app_sail": { "status": "ok", "latency_ms": 45 },
    "quick_ml": { "status": "ok", "latency_ms": 150 },
    "cache": { "status": "ok", "latency_ms": 3 },
    "staged_data_tag": { "status": "ok", "is_synthetic": true }
  },
  "uptime_seconds": 3600
}
```

## 3. Key Metrics to Monitor

### 3.1 Application Metrics

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| API p95 response time > 2s | API Gateway logs | WARNING > 2s |
| Error rate > 5% | Function logs | CRITICAL > 5% |
| RAG query success rate < 95% | Custom logging | WARNING < 95% |
| Entity resolution processing time > 1s per record | Function logs | WARNING > 1s |
| Cron job failure | Cron logs | CRITICAL (any failure) |

### 3.2 Model Metrics

| Metric | Source | Monitoring Frequency | Alert Threshold |
|--------|--------|---------------------|-----------------|
| Risk score distribution shift | int_RiskScore | Weekly | Mean score shifts > 0.1 |
| Risk score feature importance drift | int_RiskScoreFeatureImportance | Weekly | Top-3 features change |
| Entity resolution match rate | int_PersonEntityLink | Weekly | Auto-link rate drops > 20% |
| RAG answer relevance (human rating) | Manual sampling | Pre-demo | Average < 4.0/5.0 |
| Fairness check pass rate | gov_FairnessCheckResult | Daily | Any check fails |

## 4. Logging Strategy

| Log Type | Destination | Retention | Structure |
|----------|-------------|-----------|-----------|
| Application logs | Catalyst Function logs | 30 days | JSON (structured) |
| API access logs | Catalyst API Gateway | 30 days | JSON |
| Audit logs | gov_AuditLog table | 90 days | Relational (queryable) |
| Model inference logs | Custom: int_RiskScore + gov_AuditLog | 90 days | Relational |
| Deployment logs | Catalyst Pipelines | 30 days | Text |

## 5. Alerting

| Alert | Channel | Escalation |
|-------|---------|------------|
| System down (health check fails) | Email + SMS to developer | Immediate |
| Fairness check fails | Email to developer + Compliance | Immediate |
| Cron job failure | Email to developer | Within 4 hours |
| Performance degradation | Email to developer | Within 24 hours |
| Model score drift detected | Email to developer | Weekly review |

## 6. Dashboard Views

| Dashboard | Audience | Contents |
|-----------|----------|----------|
| System Health | Developer | API latency, error rate, uptime, cron status |
| Data Pipeline | Developer | Import rate, ER processing time, NER success rate |
| Model Performance | Developer + Compliance | Risk score distribution, fairness check history |
| Audit Summary | Compliance | Recent audit log entries by action type |
| Demo Readiness | Team Lead | Acceptance test results, fairness check status, synthetic tag verification |
