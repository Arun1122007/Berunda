# Security Policy (Draft)

[//]: # (Document ID: BERUNDA-OSS-003 | Status: DRAFT | Classification: PUBLIC)

---

## 1. Reporting a Vulnerability

If you discover a security vulnerability in Project Berunda, please report it privately.

**Do not** report security vulnerabilities via public GitHub Issues.

**Instead:** Email the team at (team email — to be set up) or contact via the hackathon organizer's channel.

## 2. What to Include

- Description of the vulnerability
- Steps to reproduce
- Affected version(s)
- Potential impact
- Any suggested fix (optional)

## 3. Response Timeline

| Timeframe | Action |
|-----------|--------|
| 48 hours | Acknowledgment of receipt |
| 5 business days | Initial triage and severity assessment |
| 30 days | Fix deployed (for confirmed vulnerabilities) |

## 4. Scope

| In Scope | Out of Scope |
|----------|-------------|
| API authentication bypass | Physical security of deployment servers |
| Authorization / RBAC bypass | Social engineering attacks |
| SQL injection vulnerabilities | Third-party dependencies (report to respective projects) |
| Cross-site scripting (XSS) | |
| Sensitive data exposure | |
| Audit log bypass | |

## 5. Security Contacts

- **Primary:** Berunda Team (via hackathon channel)
- **Secondary:** Catalyst Platform Security (via Catalyst support portal)

## 6. Supported Versions

| Version | Supported |
|---------|-----------|
| Latest release (v1.x) | ✅ |
| Development branch (main) | ⚠️ (limited support) |
| Older releases | ❌ |
