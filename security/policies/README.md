# Security Policies

## Password Policy

| Parameter | Requirement |
|-----------|-------------|
| Minimum length | 12 characters |
| Complexity | Uppercase + Lowercase + Digit + Special character |
| Maximum age | 90 days |
| History | 5 previous passwords remembered |
| Lockout | 5 failed attempts, 15-minute lockout |
| MFA | Required for admin and analyst roles |

## Session Policy

| Parameter | Value |
|-----------|-------|
| Token type | JWT (RS256) |
| Access token expiry | 1 hour (production) |
| Refresh token expiry | 7 days |
| Max concurrent sessions | 3 per user |
| Inactivity timeout | 30 minutes |
| Token rotation | Every refresh cycle |

## API Key Policy

- API keys are generated per application, not per user.
- Keys have full access control scope limitations.
- Keys expire every 90 days (auto-rotation).
- Revoked keys are logged and invalidated immediately.
- Keys are stored as SHA-256 hashes in the database.

## Data Classification Policy

| Level | Description | Examples | Handling |
|-------|-------------|----------|----------|
| **Public** | Non-sensitive data that can be freely shared | Crime statistics, reports | No restrictions |
| **Internal** | Data for internal use only | Aggregated analysis, patterns | Access control required |
| **Confidential** | Sensitive case data | FIR details, witness info | Encryption + access logging |
| **Restricted** | Highly sensitive personal data | Aadhaar numbers, biometrics | Field-level encryption, strict need-to-know |

## Incident Response

1. **Detection** — Automated alerts from monitoring/scanning.
2. **Triage** — Assess severity (Low/Medium/High/Critical).
3. **Containment** — Isolate affected systems, revoke credentials.
4. **Eradication** — Remove threat, patch vulnerability.
5. **Recovery** — Restore from clean backup, verify integrity.
6. **Post-mortem** — Document incident, update playbooks.

## Compliance

- Data processed in accordance with **DPDP Act 2023** (India).
- Crime data classification follows **BPRD guidelines**.
- NCRB data usage complies with their data sharing policies.
