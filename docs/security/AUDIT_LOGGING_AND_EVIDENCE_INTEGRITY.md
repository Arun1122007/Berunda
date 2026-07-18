# Audit Logging and Evidence Integrity

[//]: # (Document ID: BERUNDA-SEC-006 | Version: 1.0 | Status: DRAFT | Classification: CONFIDENTIAL | Owner: Berunda Team | Audience: Developers, Governance | Source: 01_Enterprise_Blueprint Â§12 + SRS security/privacy reqs | Last Verified: 2026-07-17 | Review: Monthly)

---

## 1. Audit Logging Requirements

### 1.1 Logging Principles

| Principle | Implementation |
|-----------|---------------|
| Append-only | Application layer prohibits UPDATE/DELETE on gov_AuditLog |
| Complete | Every sensitive read, AI output, and human decision is logged |
| Tamper-evident | Sequential auto-increment IDs; missing IDs indicate tampering |
| Queryable | Governance Officer can search and filter by user, action, entity, date |
| Retained | Through hackathon + 90 days |

### 1.2 What Gets Logged

| Category | Events | Rationale |
|----------|--------|-----------|
| Data access | Reads of person-level records (GET /persons/{id}) | Track who views person data |
| Data modification | Create, update, merge operations | Track data changes |
| AI inference | RAG queries, risk score views | Track AI output consumption |
| Authorization events | Jurisdiction overrides, restricted field access | Track privilege escalation |
| Authentication events | Login, logout, MFA challenge | Track user sessions |
| Configuration changes | Threshold updates, model deployment | Track system changes |
| Fairness checks | Automated check execution and results | Verify governance controls |

### 1.3 What Does NOT Get Logged

- GET list endpoints (without specific ID) â€” too noisy, low value
- Health check endpoint â€” high frequency, no data exposure
- Static file loads (CSS, JS, images) â€” no data exposure

## 2. Audit Log Schema

See `docs/data/CANONICAL_DATA_MODEL.md` Section 3.1 for the full `gov_AuditLog` schema.

## 3. Audit Log Integrity

### 3.1 Application-Level Protections

| Protection | Implementation |
|-----------|---------------|
| Append-only | All write operations use INSERT only; no UPDATE or DELETE exposed |
| No deletion API | No endpoint exists to delete audit records |
| Read-only for most users | Only Compliance and Admin can read audit log |
| Sequential IDs | Auto-increment BIGINT PK â€” gaps indicate tampering |

### 3.2 Phase 3+ Enhancement: Chain-of-Custody Hashing

For Phase 3+, audit log entries will include a SHA-256 hash chain:

```
Entry N: hash = SHA256(N-1_hash + entry_content + timestamp)
Entry N+1: hash = SHA256(N_hash + entry_content + timestamp)
```

This allows verification that no entries have been modified or deleted after creation. This is explicitly deferred to Phase 3+ (STRETCH) per ADR-008.

## 4. Evidence Integrity

### 4.1 What Constitutes Evidence

| Evidence Type | Source | Integrity Mechanism |
|--------------|--------|---------------------|
| Synthetic FIR case record | src_CaseMaster | Read-only after ingestion; audit log tracks all reads |
| AI-generated match recommendation | int_PersonEntityLink | Confidence score + audit log of review action |
| Entity merge confirmation | gov_AuditLog (MERGE_CONFIRM) | ReviewedBy + ReviewedAt + OldValue/NewValue JSON snapshot |
| Risk score computation | int_RiskScore | ModelVersion + ComputedAt + FeaturesJSON snapshot |
| RAG query and answer | gov_AuditLog (RAG_QUERY) | Full question + retrieved chunks + generated answer |

### 4.2 Demo Evidence Pack

The demo evidence pack is a pre-assembled collection demonstrating the system's capabilities:

**Contents:**
1. Synthetic dataset manifest (record counts, generation date, seed values)
2. Planting manifest (all planted hidden links for verification)
3. Screenshots of each feature with labeled AI outputs
4. Pre-computed "smoking gun" evidence path (navigating from FIR-001 to hidden link in FIR-042)
5. Audit log extract showing the trail of reads and AI outputs
6. Fairness check report showing CasteID/ReligionID exclusion

**Packaging:** PDF + screen recording (5 min max) stored in Catalyst Stratus.

### 4.3 Evidence Chain for the "One Person, Four Names" Demo

```
Step 1: Import 4 FIRs with name variants (Venkatesh / Venkatesha / Venkat / V.)
Step 2: NER extracts 4 distinct accused records
Step 3: Entity resolution computes similarity scores:
  - Venkatesh â†” Venkatesha: 0.82 (GREY ZONE)
  - Venkatesh â†” Venkat: 0.73 (GREY ZONE)
  - Venkatesh â†” V.: 0.51 (GREY ZONE)
Step 4: Investigator confirms all 4 links
Step 5: Audit log records 4 MERGE_CONFIRM entries
Step 6: Relationship graph now shows 1 PersonEntity connected to 4 FIRs
Step 7: Risk score computed for the merged entity using all 4 cases' data
```

This chain is fully auditable â€” each step is logged in `gov_AuditLog` with timestamps and reviewer identity.
