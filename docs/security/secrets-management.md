# Secrets Management Policy

**Document ID:** BERUNDA-SEC-SM-001 | **Version:** 1.0 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-20

---

## 1. Policy

No secrets, credentials, API keys, tokens, passwords, or private keys shall be committed to the Git repository at any time.

## 2. Secret Classification

| Class | Examples | Storage | Rotation |
|---|---|---|---|
| **Catalyst Credentials** | `CATALYST_CLIENT_SECRET`, `CATALYST_REFRESH_TOKEN` | Catalyst Console + GitHub Secrets | Per project lifecycle |
| **JWT Secrets** | `JWT_SECRET` | `.env` (dev), Catalyst Console (prod), GitHub Secrets (CI) | Per deployment |
| **Database Credentials** | `DATABASE_URL` with password | `.env` (dev), Catalyst Console (prod), GitHub Secrets (CI) | Per environment |
| **API Keys** | `OPEN_METEO_API_KEY`, `BHUVAN_API_KEY` | `.env` (dev), Catalyst Console (prod), GitHub Secrets (CI) | Per provider policy |
| **Test Secrets** | `AUTH_JWT_SECRET` in tests | `tests/conftest.py` (known test value only) | Not applicable |

## 3. Secret Storage

### Local Development
- All secrets go in `.env` file (gitignored)
- `.env.example` contains fake placeholder values only
- Never copy real values into `.env.example`

### CI/CD (GitHub Actions)
- All secrets stored as **GitHub Secrets** (repository → Settings → Secrets and variables → Actions)
- Secrets are injected as environment variables at runtime
- Never print secrets in workflow logs

### Production (Catalyst)
- Secrets configured in Catalyst Console (Environment Variables per project/environment)
- Never hardcode secrets in function code

## 4. `.gitignore` Verification

The following patterns protect secrets from accidental commit:

```
.env
.env.*
!.env.example
*.key
*.pem
*.p12
*.pfx
*.crt
credentials.json
token.json
catalyst-credentials.json
service-account.json
```

## 5. Prevention Mechanisms

| Mechanism | Tool/Config | Trigger |
|---|---|---|
| `.gitignore` | Git | Every commit |
| Pre-commit hook | `detect-private-key` (pre-commit-hooks) | Every commit |
| CI scan | TruffleHog in `security-scan.yml` | Every push to main |
| CI scan | GitHub Secret Scanning (built-in) | Every push |
| Dependency scan | `pip-audit` + `npm audit` | Every PR |
| Code scan | CodeQL | Every PR |

## 6. Incident Response

If a secret is accidentally committed:

1. **Immediately rotate the compromised secret**
2. **Remove the secret from Git history** using `git filter-branch` or `BFG Repo-Cleaner`
3. **Force-push the cleaned history**
4. **Verify removal** with TruffleHog
5. **Document the incident** in `logs/incidents/`
6. **Review access logs** for unauthorized use

## 7. Prohibited Patterns

- ❌ Hardcoded credentials in source code
- ❌ Secrets in configuration files committed to git
- ❌ Secrets in documentation files
- ❌ Secrets in log output (production or development)
- ❌ Secrets in error messages returned to clients
- ❌ Secrets in Docker images (use build args or runtime env)
- ❌ Secrets in frontend bundle (use runtime env vars)
- ❌ Printing secrets to console during debugging

## 8. Safe Development Practices

1. **Use `.env.example`** with obviously fake values
2. **Validate on startup** — application must fail with clear message if required secret is missing
3. **Mock external services** — unit tests should not require real credentials
4. **Redact in logs** — configuration dumps must mask secret values
5. **Use short-lived tokens** — prefer refresh token flows over long-lived API keys
6. **Review new dependencies** — check `dependabot.yml` for automated PR review

## 9. Tools

| Tool | Purpose | Run Frequency |
|---|---|---|
| `trufflehog` | Secret scanning | Every push (CI) |
| `pip-audit` | Python dependency vulnerability audit | Weekly + every PR |
| `npm audit` | Node.js dependency vulnerability audit | Weekly + every PR |
| `pre-commit` | Local secret detection | Every commit |
| `dependabot` | Automated dependency updates | Daily |

## 10. Testing Secrets

For unit tests, a test JWT secret is defined in `tests/conftest.py`:

```python
secret = os.environ.get("AUTH_JWT_SECRET", "test-secret")
```

This is a known, non-sensitive value used only for test token generation. It requires no rotation and poses no security risk.
