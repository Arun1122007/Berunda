# Threat Model

[//]: # (Document ID: BERUNDA-SEC-002 | Version: 1.0 | Status: DRAFT | Classification: CONFIDENTIAL | Owner: Berunda Team | Audience: Security, DevOps | Source: 01_Enterprise_Blueprint §12 + SRS security/privacy reqs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Methodology

STRIDE per component. Since all data is synthetic and the deployment is a hackathon demo, the threat model focuses on realistic risks rather than hypothetical nation-state threats.

## 2. Assets

| Asset ID | Asset | Confidentiality | Integrity | Availability | Owner |
|----------|-------|----------------|-----------|-------------|-------|
| A-001 | Synthetic FIR case data (src_*) | INTERNAL | HIGH | HIGH | Developer |
| A-002 | Entity resolution data (int_PersonEntity) | INTERNAL | HIGH | HIGH | Developer |
| A-003 | Risk scores (int_RiskScore) | INTERNAL | HIGH | MEDIUM | Developer |
| A-004 | RAG corpus embeddings (int_RAGCorpusChunk) | INTERNAL | MEDIUM | MEDIUM | Developer |
| A-005 | Audit logs (gov_AuditLog) | CONFIDENTIAL | HIGH | LOW | Developer |
| A-006 | Caste/Religion data (src_CasteMaster, src_ReligionMaster) | RESTRICTED | HIGH | LOW | Developer |
| A-007 | JWT signing keys | HIGH | HIGH | MEDIUM | Catalyst managed |
| A-008 | Demo evidence pack | PUBLIC | HIGH | MEDIUM | Developer |

## 3. Threat Table

| ID | Threat | STRIDE Category | Asset | Likelihood | Impact | Mitigation |
|----|--------|----------------|-------|------------|--------|------------|
| T-001 | Unauthorized access to case data via API | Spoofing | A-001 | LOW | HIGH | JWT auth + RBAC + jurisdiction scoping |
| T-002 | SQL injection via RAG query | Tampering | A-001 | LOW | CRITICAL | Parameterized queries; no free-form SQL |
| T-003 | CasteID/ReligionID exposed in API response | Information Disclosure | A-006 | LOW | HIGH | Field-level access control; separate handler for Compliance role |
| T-004 | Audit log tampering (delete/modify) | Tampering | A-005 | LOW | HIGH | Append-only at application layer |
| T-005 | Cross-tenant data access (jurisdiction bypass) | Elevation of Privilege | A-001 | LOW | HIGH | Jurisdiction scoped per request; X-Jurisdiction-Override logged |
| T-006 | Session hijacking | Spoofing | A-007 | LOW | HIGH | Short-lived JWT (15 min); MFA required |
| T-007 | Synthetic data mistaken for real data | Spoofing | A-001 | LOW | MEDIUM | Clear labeling + "SYNTHETIC DATA" watermark |
| T-008 | LLM hallucination in RAG answers | Repudiation | A-004 | MEDIUM | MEDIUM | Retrieval-before-generation; citation requirement; insufficient-evidence response |
| T-009 | Rate limit bypass | Denial of Service | A-001 | LOW | LOW | Catalyst API Gateway rate limiting |
| T-010 | Unauthorized use of X-Jurisdiction-Override | Elevation of Privilege | A-001 | LOW | HIGH | Only Compliance/Admin role; every use logged |
| T-011 | Proxy variables for caste/religion in risk model | Information Disclosure | A-003 | MEDIUM | HIGH | Feature importance monitoring; district+caste correlation checks |
| T-012 | Non-repudiation of AI-assisted decisions | Repudiation | A-005 | MEDIUM | HIGH | Full audit trail: who saw what AI output, when, and what action they took |

## 4. Mitigation Verification

| Threat ID | Verification Method | Frequency |
|-----------|-------------------|-----------|
| T-001 | Automated API auth tests | CI/CD |
| T-002 | SQL injection scan in test suite | CI/CD |
| T-003 | Integration test: Compliance role sees fields; others get 403 | CI/CD |
| T-004 | Audit log append-only verified by test | CI/CD |
| T-005 | Jurisdiction filter integration tests | CI/CD |
| T-006 | MFA enforcement test | CI/CD |
| T-007 | Synthetic tag presence verified by Cron job (CRON-005) | Daily |
| T-008 | RAG test suite (20 demo questions) | CI/CD + pre-demo |
| T-0010 | Audit log review for override usage | Weekly (manual) |
| T-0011 | Feature importance scan (FC-002) | Per model version |
