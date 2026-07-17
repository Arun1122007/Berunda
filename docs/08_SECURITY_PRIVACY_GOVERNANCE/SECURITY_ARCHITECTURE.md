# Security Architecture

[//]: # (Document ID: BERUNDA-SEC-001 | Status: DRAFT | Classification: CONFIDENTIAL)

---

## 1. Security Principles

1. **Defense in depth** — Multiple layers of security controls (auth, RBAC, jurisdiction scoping, field-level access, audit).
2. **Least privilege** — Each role has the minimum permissions needed (see ACCESS_CONTROL_MATRIX.md).
3. **Secure by default** — Deny access unless explicitly granted. No public access to person-level data.
4. **All access is audited** — Every data read and AI output is traceable.
5. **Synthetic data boundary** — Synthetic data is clearly labeled; no real PII enters the system.

## 2. Security Layers

```
┌─────────────────────────────────────────────┐
│  Catalyst Authentication (AuthN)            │
│  JWT tokens, MFA for person-level access    │
├─────────────────────────────────────────────┤
│  Catalyst API Gateway (AuthZ enforcement)   │
│  Role validation, rate limiting, IP filter  │
├─────────────────────────────────────────────┤
│  Application Layer (RBAC + Jurisdiction)    │
│  Per-request role/jurisdiction check        │
├─────────────────────────────────────────────┤
│  Field-Level Access Control                 │
│  CasteID/ReligionID → Compliance role only  │
├─────────────────────────────────────────────┤
│  Data Store Security                        │
│  Column-level encryption for restricted     │
│  fields; parameterized queries (no SQL inj) │
├─────────────────────────────────────────────┤
│  Audit Logging (gov_AuditLog)               │
│  Append-only; immutable at application lvl  │
└─────────────────────────────────────────────┘
```

## 3. Authentication (Catalyst Authentication)

| Feature | Implementation |
|---------|---------------|
| Identity provider | Catalyst Authentication |
| Token format | JWT (RS256 signed) |
| Token expiry | 15 minutes (access), 7 days (refresh) |
| MFA | Required for accounts accessing person-level records |
| Session management | Catalyst managed; revocable by Admin |
| Password policy | Catalyst default (min 8 chars, complexity) |

## 4. Data Security

### 4.1 Encryption

| Data State | Protection | Implementation |
|------------|-----------|---------------|
| At rest (Data Store) | AES-256 | Catalyst Data Store default |
| At rest (NoSQL) | AES-256 | Catalyst NoSQL default |
| At rest (Stratus files) | AES-256 | Catalyst Stratus default |
| In transit | TLS 1.2+ | Catalyst API Gateway enforced |
| Restricted fields (CasteID, ReligionID) | Column-level encryption | Application-layer encryption + restricted decryption in Compliance role handler |

### 4.2 SQL Injection Prevention

All database queries use parameterized statements or prepared statements. No string concatenation for SQL query construction.

### 4.3 API Security

| Control | Implementation |
|---------|---------------|
| Rate limiting | API Gateway: tiered (see API_DESIGN_SPECIFICATION.md) |
| Input validation | JSON schema validation on all POST/PUT endpoints |
| CORS | Restricted to dashboard origin only |
| Request size limit | 10 MB (file uploads), 100 KB (JSON payloads) |

## 5. Secrets Management

| Secret | Storage | Rotation |
|--------|---------|----------|
| JWT signing keys | Catalyst managed | Automatic |
| Database credentials | Catalyst managed (Data Store connection) | Automatic |
| API keys (external services) | Catalyst Stratus (encrypted) + Catalyst Cache | Manual |
| QuickML model keys | Catalyst managed | Automatic |

## 6. Synthetic Data Safety

| Control | Implementation |
|---------|---------------|
| Clear labeling | `_synthetic_data_tag` table; "SYNTHETIC DATA" in headers/watermarks |
| No real PII | Generator uses Faker; no real FIR data loaded |
| Accidental PII response | See INCIDENT_RESPONSE_AND_BREACH_PLAYBOOK.md |
| Demo evidence pack | Contains only pre-approved synthetic data |
