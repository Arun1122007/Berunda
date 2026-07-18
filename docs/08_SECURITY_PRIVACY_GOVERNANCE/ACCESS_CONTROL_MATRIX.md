# Access Control Matrix

[//]: # (Document ID: BERUNDA-SEC-003 | Version: 1.0 | Status: DRAFT | Classification: CONFIDENTIAL | Owner: Berunda Team | Audience: All stakeholders | Source: 01_Enterprise_Blueprint §12 + SRS security/privacy reqs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Role Definitions

| Role | Description | Assigned To | Implicit Jurisdiction |
|------|-------------|-------------|----------------------|
| INVESTIGATOR | Front-line police officer viewing case data and AI insights | Investigating Officers (IOs), Station House Officers (SHOs) | Own district only |
| SCRB_ANALYST | State-level crime analyst reviewing patterns across jurisdictions | State Crime Records Bureau analysts | All districts |
| COMPLIANCE | Governance officer ensuring data protection and fairness | Compliance Officer, Internal Audit | All districts (including restricted fields) |
| ADMIN | System administrator managing users, configuration, and deployment | Developer, System Admin | All districts (full access) |

## 2. Permission Matrix

| Resource | Action | INVESTIGATOR | SCRB_ANALYST | COMPLIANCE | ADMIN |
|----------|--------|-------------|--------------|------------|-------|
| **Cases** | | | | | |
| src_CaseMaster | Read | Own district | All | All | All |
| src_CaseMaster | Create | No | Yes | No | Yes |
| src_CaseMaster | Update | No | Yes (status only) | No | Yes |
| src_CaseMaster | Delete | No | No | No | Yes |
| **Complainant Details** | | | | | |
| src_ComplainantDetails | Read (excl. CasteID, ReligionID) | Own district | All | All | All |
| src_ComplainantDetails.CasteID | Read | No | No | Yes | No |
| src_ComplainantDetails.ReligionID | Read | No | No | Yes | No |
| **Persons** | | | | | |
| int_PersonEntity | Read | Own district | All | All | All |
| int_PersonEntity | Merge (confirm/reject) | Own district | No | No | Yes |
| int_PersonEntityLink | Read | Own district | All | All | All |
| **Relationships** | | | | | |
| int_RelationshipEdge | Read | Own district | All | All | All |
| int_RelationshipEdge | Shortest path | No | Yes | No | Yes |
| **Risk** | | | | | |
| int_RiskScore | Read | Own district | All | All | All |
| int_RiskScoreFeatureImportance | Read | Own district | All | All | All |
| int_RiskScore | Recompute | No | Yes | No | Yes |
| **Geospatial** | | | | | |
| int_HotspotLayer | Read | Own district | All | All | All |
| int_AnomalyAlert | Read | Own district | All | All | All |
| **RAG** | | | | | |
| int_RAGCorpusChunk | Query | Own district | All | All | All |
| **Governance** | | | | | |
| gov_AuditLog | Read | No (own actions only) | No (own actions only) | All | All |
| gov_FairnessCheckResult | Read | No | No | All | All |
| gov_DataProvenanceRecord | Read | No | No | All | All |
| **System** | | | | | |
| Configuration | Read | No | No | No | Yes |
| Configuration | Update | No | No | No | Yes |
| User management | Manage | No | No | No | Yes |
| /health | Read | Yes | Yes | Yes | Yes |
| /info | Read | Yes | Yes | Yes | Yes |

## 3. Jurisdiction Scoping

| Role | Scoping Rule | Implementation |
|------|-------------|----------------|
| INVESTIGATOR | `WHERE src_CaseMaster.PoliceStationID IN (user.assigned_stations)` | Extracted from Employee table linked to JWT subject |
| SCRB_ANALYST | No jurisdiction filter | All records visible |
| COMPLIANCE | No jurisdiction filter (except restricted fields — always visible) | All records visible |
| ADMIN | No jurisdiction filter | All records visible |

## 4. Field-Level Security

| Field | RESTRICTED | Visible To | Notes |
|-------|-----------|------------|-------|
| ComplainantDetails.CasteID | Yes | COMPLIANCE only | ADR-007 enforcement |
| ComplainantDetails.ReligionID | Yes | COMPLIANCE only | ADR-007 enforcement |
| CasteMaster.* | Yes | COMPLIANCE only | |
| ReligionMaster.* | Yes | COMPLIANCE only | |
| gov_AuditLog | No (but filtered) | Own actions + COMPLIANCE/ADMIN | Non-Compliance roles see only their own entries |

## 5. API Endpoint Authorization Mapping

See `docs/07_API_AND_CONTRACTS/ERROR_AUTHORIZATION_AND_AUDIT_CONTRACTS.md` Section 2.1 for the complete endpoint-to-permission mapping.
