# Security Architecture

## Overview

Berunda implements a defense-in-depth security architecture covering authentication, authorization, data protection, audit, and vulnerability management.

## Security Layers

```
┌────────────────────────────────────┐
│         Network Security           │
│  ┌──────────────────────────────┐  │
│  │     Application Security     │  │
│  │  ┌────────────────────────┐  │  │
│  │  │   Authentication       │  │  │
│  │  │  (Catalyst Auth/JWT)   │  │  │
│  │  ├────────────────────────┤  │  │
│  │  │   Authorization        │  │  │
│  │  │  (RBAC - Role Based)   │  │  │
│  │  ├────────────────────────┤  │  │
│  │  │   Data Encryption      │  │  │
│  │  │  (At rest / In transit)│  │  │
│  │  ├────────────────────────┤  │  │
│  │  │   Audit Logging        │  │  │
│  │  │  (All access logged)   │  │  │
│  │  ├────────────────────────┤  │  │
│  │  │   Input Validation     │  │  │
│  │  │  (Schema + Sanitize)   │  │  │
│  │  └────────────────────────┘  │  │
│  └──────────────────────────────┘  │
│  ┌──────────────────────────────┐  │
│  │    Vulnerability Management  │  │
│  │  (Scanning + Patching)       │  │
│  └──────────────────────────────┘  │
└────────────────────────────────────┘
```

## Authentication

- **Primary**: Zoho Catalyst Authentication (SSO, OAuth 2.0, SAML)
- **Local Dev**: Mock JWT tokens
- **MFA**: Available through Catalyst (optional policy)
- **Session**: JWT-based stateless sessions with configurable expiry

## Authorization (RBAC)

| Role | Permissions |
|------|-------------|
| `admin` | Full access — users, config, all data, audit logs |
| `analyst` | Read/write FIRs, entity resolution, reports |
| `viewer` | Read-only access to dashboards and reports |
| `ai_operator` | Manage ML models, trigger inferences |

## Data Encryption

| State | Method |
|-------|--------|
| **In transit** | TLS 1.3 (HTTPS/WSS) |
| **At rest** | Catalyst Data Store encryption (AES-256) |
| **Secrets** | Catalyst Console Environment Variables |
| **PII fields** | Field-level encryption for Aadhaar, phone, address |

## Audit Logging

All access to sensitive data is logged with:
- User ID and role
- Action performed
- Resource accessed
- Timestamp (ISO 8601)
- Source IP
- Request ID (correlation)

## Vulnerability Management

See `security/scanning/README.md` for tooling and procedures.
See `security/policies/README.md` for detailed policies.
