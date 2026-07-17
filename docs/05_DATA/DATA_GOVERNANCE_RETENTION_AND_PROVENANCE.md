# Data Governance, Retention, and Provenance

[//]: # (Document ID: BERUNDA-DATA-008 | Status: DRAFT | Classification: CONFIDENTIAL)

---

## 1. Governance Principles

Berunda operates under the following data governance principles, derived from ADR-007 (Sensitive Field Exclusion) and ADR-003 (Source of Record vs Intelligence Layer):

1. **Source data is authoritative.** The `src_` schema is never modified by AI/analytics functions.
2. **AI output is advisory.** All computed scores, matches, and recommendations are flagged as AI-generated and subject to human review.
3. **Restricted fields are never used in models.** CasteID, ReligionID, and their proxies are hard-excluded from all predictive features.
4. **Every action is audited.** All sensitive reads, AI inferences, and human approvals are logged.
5. **Provenance is tracked.** Every derived record (int_*) traces back to its source record(s) via gov_DataProvenanceRecord.

## 2. Data Classification

| Classification | Definition | Examples | Access Restriction |
|---------------|-----------|----------|-------------------|
| PUBLIC | Non-sensitive aggregate data | Crime head distribution, hotspot maps by district | No auth required for demo |
| INTERNAL | Operational data accessible to authenticated users | CaseMaster, ComplainantDetails, Victim, Accused (without CasteID/ReligionID) | Requires authentication + role authorization |
| RESTRICTED | Sensitive fields with limited access | CasteID, ReligionID, PersonEntity linkage | Compliance role only |
| CONFIDENTIAL | Audit and governance records | AuditLog, FairnessCheckResult | Governance + Admin roles only |

## 3. Access Control by Role (Data-Level)

| Data / Table | Investigator | SCRB Analyst | Compliance Officer | Admin |
|-------------|-------------|--------------|-------------------|-------|
| src_CaseMaster (all columns except RESTRICTED) | Own jurisdiction only | All jurisdictions | All jurisdictions | All |
| src_CaseMaster.CasteID | ❌ | ❌ | ✅ | ❌ |
| src_CaseMaster.ReligionID | ❌ | ❌ | ✅ | ❌ |
| src_ComplainantDetails (all columns except RESTRICTED) | Own jurisdiction only | All | All | All |
| src_ComplainantDetails.CasteID | ❌ | ❌ | ✅ | ❌ |
| src_ComplainantDetails.ReligionID | ❌ | ❌ | ✅ | ❌ |
| All other src_* tables | Own jurisdiction | All | All | All |
| int_PersonEntity | Own jurisdiction | All | All | All |
| int_RiskScore | Own jurisdiction | All | All | All |
| int_RiskScoreFeatureImportance | Own jurisdiction (view only) | All (view only) | All | All |
| int_RelationshipEdge | Own jurisdiction | All | All | All |
| int_AnomalyAlert | Own jurisdiction | All | All | All |
| gov_AuditLog | ❌ | Own actions only | All | All |
| gov_FairnessCheckResult | ❌ | ❌ | All | All |

## 4. Data Retention Policy

Since all Phase 1 data is synthetic, retention is simplified. For production deployment (Phase 3+), these policies would apply:

| Data Category | Retention Period | Deletion Procedure |
|--------------|-----------------|-------------------|
| Synthetic source data (src_*) | Retained through hackathon + 30 days | Drop schema or truncate tables |
| Synthetic intelligence data (int_*) | Retained through hackathon + 30 days | Drop schema or truncate tables |
| Audit logs (gov_AuditLog) | Retained through hackathon + 90 days | Export + purge per GDPR-like policy |
| Synthetic data tag | Permanent | Metadata-only |

**For hypothetical production:**
- CaseMaster data: 10 years (legal requirement per police records retention)
- Audit logs: 7 years
- Risk scores: 5 years after case closure
- RAG corpus: Duration of case + 2 years

## 5. Data Provenance Tracking

Every derived record in `int_*` tables traces back to its source via `gov_DataProvenanceRecord`.

**When provenance is created:**

| Trigger | Source | Target | Transformation |
|---------|--------|--------|---------------|
| NER extraction | src_CaseMaster.BriefFacts | int_PersonEntityLink | "NER extraction from BriefFacts" |
| NER extraction | src_CaseMaster.BriefFacts | int_VehicleLink | "Vehicle NER extraction from BriefFacts" |
| Entity resolution | src_ComplainantDetails, src_Victim, or src_Accused | int_PersonEntity | "Entity resolution: rule-based matching" |
| Risk scoring | int_PersonEntity + src_CaseMaster | int_RiskScore | "QuickML AutoML risk scoring" |
| Chunking | src_CaseMaster.BriefFacts | int_RAGCorpusChunk | "Narrative chunking for RAG" |
| Anomaly detection | src_CaseMaster aggregated | int_AnomalyAlert | "Z-score anomaly detection" |

## 6. Fairness Check Procedures

| Check ID | Frequency | Procedure | Responsible |
|----------|-----------|-----------|-------------|
| FC-001 | Per RiskScore model training | Verify CasteID/ReligionID not in feature set | Automated (QuickML pipeline) |
| FC-002 | Per RiskScore inference | Scan int_RiskScoreFeatureImportance for restricted field names | Automated (post-scoring) |
| FC-003 | Daily | Verify Compliance role can access restricted fields; other roles cannot | Automated (Cron) |
| FC-004 | Weekly | Review AuditLog for unauthorized access attempts to restricted data | Manual (Compliance Officer) |

All fairness check results are written to `gov_FairnessCheckResult`.

## 7. Synthetic Data Disclaimer

Every system output that surfaces data to a user must include one of:

| Context | Disclaimer |
|---------|------------|
| Dashboard header | "⚠ Synthetic Data for Demo — Not Real FIR Records" |
| CSV/JSON export | "# GENERATED SYNTHETIC DATA — NOT REAL FIR RECORDS #" (as first line) |
| Graph visualization | Title: "Demo Dataset (Synthetic) — Relationship Graph" |
| RAG answer footer | "Answer generated from synthetic demo corpus. Not based on real case data." |
| Pitch deck demo screenshot | "SYNTHETIC DATA" watermark diagonally overlaid |

## 8. Incident Response (Data-Related)

| Scenario | Response | Responsible |
|----------|----------|-------------|
| Accidental real PII in synthetic data | Immediately delete the dataset, regenerate from clean seed | Developer |
| Unauthorized access detected | Revoke access, review AuditLog scope, notify team lead | Admin |
| Fairness check fails (CasteID in features) | Block model deployment, retrain without restricted features | Developer + Compliance |
| Provenance link broken | Re-run the generating pipeline for affected records | Developer |
