# Incident Response and Breach Playbook

[//]: # (Document ID: BERUNDA-SEC-007 | Version: 1.0 | Status: DRAFT | Classification: CONFIDENTIAL | Owner: Berunda Team | Audience: All stakeholders | Source: 01_Enterprise_Blueprint §12 + SRS security/privacy reqs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Incident Severity Levels

| Level | Definition | Examples | Response Time |
|-------|-----------|----------|---------------|
| SEV-1 | Demonstrable harm or unauthorized access to restricted data | Caste/Religion data exposed to non-Compliance role; real PII found in synthetic data | Immediate (< 1 hour) |
| SEV-2 | System integrity or availability impact | Audit log tampered; entity resolution merging incorrect persons in bulk | < 4 hours |
| SEV-3 | Minor breach of policy with limited impact | User accesses data outside jurisdiction without override | < 24 hours |
| SEV-4 | Informational — no harm, but worth documenting | Synthetic data labeling missing from one interface | < 48 hours |

## 2. Incident Detection

| Detection Method | Description | Automated? |
|-----------------|-------------|------------|
| Fairness check failure | FC-003 (daily access control check) fails | Yes (Cron) |
| Audit log gap detection | Missing sequential IDs in gov_AuditLog | No (manual spot-check) |
| Unauthorized access alert | Multiple 403 responses from same user | Yes (API Gateway rate limiting + alert) |
| User report | User reports seeing data they shouldn't | No |
| Monitor alert | Service health check failure | Yes |

## 3. Incident Response Procedures

### 3.1 SEV-1: Restricted Data Exposure

**Scenario:** CasteID/ReligionID field exposed to Investigator role.

**Response:**
1. **IMMEDIATE:** Revoke the affected user's access (Admin → Catalyst Authentication)
2. **IMMEDIATE:** Verify the API endpoint that exposed the field → fix the query
3. **WITHIN 1 HOUR:** Run full audit log scan for all views of the affected field
4. **WITHIN 4 HOURS:** Document the incident in the incident register
5. **WITHIN 24 HOURS:** Add automated test to prevent recurrence

### 3.2 SEV-1: Real PII Found in Synthetic Data

**Scenario:** A generated synthetic name coincidentally matches a real person.

**Response:**
1. **IMMEDIATE:** Document the affected records
2. **IMMEDIATE:** Determine if PII was exposed to any user (check audit log)
3. **WITHIN 4 HOURS:** Regenerate the synthetic dataset with a new seed to change all names
4. **WITHIN 24 HOURS:** Add name collision check against a public names database (if available)

### 3.3 SEV-2: Entity Resolution Bulk Error

**Scenario:** Entity resolution incorrectly merges many distinct persons due to a threshold/weight bug.

**Response:**
1. **IMMEDIATE:** Disable the entity resolution auto-link feature
2. **WITHIN 2 HOURS:** Identify affected PersonEntity records
3. **WITHIN 4 HOURS:** Roll back to last known-good data snapshot (if available)
4. **WITHIN 24 HOURS:** Fix bug, re-run ER, verify against planted test cases

### 3.4 SEV-3: Jurisdiction Violation

**Scenario:** Investigator views case data from outside their assigned district.

**Response:**
1. **WITHIN 24 HOURS:** Review audit log to determine scope of access
2. **WITHIN 48 HOURS:** Verify jurisdiction scoping filter is correct
3. **WITHIN 48 HOURS:** Add additional logging or alerting for cross-jurisdiction access

## 4. Incident Register

| Date | Severity | Description | Action Taken | Status |
|------|----------|-------------|-------------|--------|
| (No incidents to date — pre-hackathon) | | | | |

## 5. Post-Incident Review

Every SEV-1 and SEV-2 incident triggers a post-incident review:

1. Root cause analysis (documented in incident register)
2. Timeline reconstruction from audit logs
3. Identification of control gaps
4. Remediation plan with owner and deadline
5. Lessons learned shared with the team

## 6. Contact and Escalation

| Role | Name | Contact | Escalation Path |
|------|------|---------|-----------------|
| Developer (on-call) | Berunda Team | (hackathon channel) | First responder |
| Team Lead | Berunda Team Lead | (hackathon channel) | SEV-1/SEV-2 escalation |
| Admin | Catalyst Platform Admin | Catalyst support portal | Platform-level issues |

## 7. Hackathon-Specific Notes

Since this is a hackathon with synthetic data only:
- No legal obligation to report breaches to data protection authorities
- No real data subjects to notify
- Focus is on demonstrating governance controls, not achieving production-grade security
- The incident response process itself is a demo artifact (show the judges we have a plan)
