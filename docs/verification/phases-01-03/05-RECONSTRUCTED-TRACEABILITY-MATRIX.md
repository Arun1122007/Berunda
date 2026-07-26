# Reconstructed Traceability Matrix

| Epic | Feature | API Endpoint | Data Model / Service |
|------|---------|--------------|----------------------|
| Data Ingestion | F-001 (FIR import) | `POST /cases/import` | `CaseMaster` |
| Entity Resolution | F-002 (NER) | Internal Function | `PersonEntityLink`, `VehicleLink` |
| Entity Resolution | F-003 (Cross-case ER) | `GET /persons` | `PersonEntity` |
| Link Analysis | F-004 (Graph) | `GET /persons/{id}/relationships` | `RelationshipEdge` |
| Analytics | F-005 (Hotspots) | `GET /hotspots` | `CaseMaster.Inv_OccuranceTime` |
| AI/ML | F-006 (Risk score) | `GET /risk/scores/{id}` | `RiskScore`, Catalyst QuickML |
| Analytics | F-007 (Anomalies) | `GET /anomalies` | `AnomalyAlert` |
| Governance | F-007b (Human Review) | `PUT /persons/{id}/review` | AppSail UI / Flags |
| AI/ML | F-008 (Ask Berunda RAG) | `POST /rag/query` | Catalyst QuickML |
| Security | F-009 (Auth + RBAC) | N/A | Catalyst Authentication |
| Security | F-010 (Audit logging) | `GET /audit-log` | `AuditLog` |
| Governance | F-011 (Fairness check) | `GET /fairness-checks` | `FairnessCheckResult` |