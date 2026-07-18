# Privacy Impact Assessment

[//]: # (Document ID: BERUNDA-SEC-004 | Version: 1.0 | Status: DRAFT | Classification: CONFIDENTIAL | Owner: Berunda Team | Audience: Governance, Compliance | Source: 01_Enterprise_Blueprint §12 + SRS security/privacy reqs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Assessment Scope

This PIA covers the Berunda platform operating on synthetic FIR data for the Datathon 2026 hackathon demo. Since no real personal data is used, privacy risks are limited but still documented for governance completeness.

## 2. Data Inventory

### 2.1 Data Collected

| Data Category | Examples | Source | Purpose | Retention |
|---------------|---------|--------|---------|-----------|
| Person identifiers (synthetic) | Name, age, gender | Synthetic data generator (Faker) | Entity resolution, case association | Hackathon + 30 days |
| Contact information (synthetic) | Address (implied via district) | Synthetic data generator | Jurisdiction filtering, geospatial analysis | Hackathon + 30 days |
| Identity markers (synthetic) | Caste, Religion (in ComplainantDetails) | Synthetic data generator | Statutory reporting demo (RESTRICTED) | Hackathon + 30 days |
| Legal data (synthetic) | Act, Section, Crime head | Synthetic data generator | Case classification demo | Hackathon + 30 days |
| Location data (synthetic) | Latitude, Longitude | Synthetic data generator | Hotspot mapping demo | Hackathon + 30 days |
| User data | Name, EmployeeID, role, district | Catalyst Authentication + Employee table | Authentication, authorization, audit | Demo duration |

### 2.2 Data NOT Collected

| Data Type | Reason |
|-----------|--------|
| Real personal data of any kind | Hackathon uses synthetic data only |
| Biometric data | Out of scope for Phase 1 |
| Health data | Not applicable to FIR domain |
| Financial account details | Not in source schema |
| Criminal record from external systems | Not integrated in Phase 1 |
| Device identifiers or telemetry | Not collected |
| Cookies or tracking data | Not implemented |

## 3. Privacy Principles

| Principle | Implementation |
|-----------|---------------|
| **Data minimization** | Only data required for the demo features is generated |
| **Purpose limitation** | Synthetic data is used only for demo and testing |
| **Access limitation** | RBAC + jurisdiction scoping restricts who sees what |
| **Storage limitation** | Data retained only through hackathon + 30 days |
| **Accuracy** | Synthetic data is deterministic (seeded) for reproducibility |
| **Security** | Encryption at rest and in transit; field-level controls for sensitive fields |
| **Accountability** | Full audit trail for all data access |

## 4. Privacy Risks and Mitigations

| Risk ID | Risk | Likelihood | Impact | Mitigation |
|---------|------|-----------|--------|------------|
| PR-001 | Synthetic name resembles real person after generation | LOW | LOW | All synthetic data labeled as such; accidental resemblance is coincidental; no real data sourced |
| PR-002 | Caste/Religion data exposed despite restriction | LOW | MEDIUM | Field-level access control restricts to Compliance role; access logged |
| PR-003 | Location data reveals specific incident location | LOW | LOW | Coordinates are synthetic and not real incident locations |
| PR-004 | User credentials compromised | LOW | HIGH | MFA required; short-lived JWT; audit logging identifies breach scope |
| PR-005 | Synthetic data mistaken for real data by demo observers | LOW | LOW | "SYNTHETIC DATA" watermark on all interfaces |
| PR-006 | Cross-entity resolution creates detailed person profile | LOW | LOW | PersonEntity only aggregates synthetic case data; labeled as AI-derived |

## 5. Data Subject Rights (Simulated for Demo)

Since the data is synthetic, no real data subject rights apply. However, the system architecture supports:

| Right | Mechanism | Implementation |
|-------|-----------|---------------|
| Right to access | Person search API | GET /persons/{id} |
| Right to rectification | Manual data correction (Admin) | Admin updates source records |
| Right to erasure | Full synthetic data purge | Delete schema or truncate tables |
| Right to restrict processing | Role-based access controls | RBAC determines processing scope |
