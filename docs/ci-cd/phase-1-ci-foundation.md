# Phase 1 — CI/CD Foundation

**Document ID:** BERUNDA-CICD-001 | **Version:** 1.1 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-24

---

## CI Workflow Overview

The project has 4 CI/CD workflows in `.github/workflows/`:

| Workflow | Trigger | Purpose |
|---|---|---|
| `ci.yml` | Push/PR to main | Lint, test, build, Docker build |
| `test.yml` | PR to any branch | Full test suite (unit, integration, e2e, performance) |
| `security-scan.yml` | Push to main, weekly schedule | Secrets, dependency, code, container scanning |
| `deploy.yml` | Manual dispatch | Deploy to staging/production |

---

## ci.yml — Main CI Pipeline

### Trigger Conditions
- Push to `main` branch
- Pull request targeting `main` branch

### Jobs

| Job | Language | Steps | Required |
|---|---|---|---|
| `lint` | Python, Node.js (matrix) | Ruff, mypy, ESLint, Prettier | Yes |
| `test` | Python, Node.js (matrix) | pytest with coverage, Vitest | Yes |
| `build` | Python, Node.js (matrix) | Python import check, Vite build | Yes |
| `docker-build` | Docker | Build frontend, API, worker images | No (informational) |

### Required Checks (Branch Protection)
- Lint (Python) — must pass
- Lint (Node.js) — must pass
- Test (Python) — must pass (coverage >= 62%)
- Test (Node.js) — must pass
- Build (Node.js) — must pass

### Quality Gate Reference

See [CI Workflow Guide](./ci-workflow-guide.md) for:
- Complete list of quality gates with pass/fail modes
- Local validation commands for every gate
- Failure diagnosis guide
- Pre-commit hook reference
- Python tool configuration summary

## Known Issues (See CI Workflow Guide for Details)

| Issue | Status |
|-------|--------|
| `mypy` has `continue-on-error` | ⚠️ Known — legacy type errors not yet fixed |
| `bandit` has `continue-on-error` | ⚠️ Known — false positive noise not yet suppressed |
| `test-node` has `continue-on-error` | ⚠️ Known — vitest JUnit reporter not configured |
| No `requirements.lock` committed | ⚠️ Known — run `pip freeze > requirements.lock` |

---

## test.yml — Full Test Suite

### Trigger Conditions
- Pull request to any branch
- Manual workflow dispatch

### Jobs

| Job | Services Required | Coverage |
|---|---|---|
| `unit` (Python) | None | Unit tests, module-level |
| `unit` (Node.js) | None | Component unit tests |
| `integration` | PostgreSQL 16, Redis 7 | Integration tests |
| `e2e` | Playwright | End-to-end browser tests |
| `performance` | None | k6 performance tests |

### Integration Test Services
```yaml
services:
  postgres:
    image: postgres:16-alpine
    env: { POSTGRES_USER: berunda, POSTGRES_PASSWORD: berunda_test, POSTGRES_DB: berunda_test }
  redis:
    image: redis:7-alpine
```

---

## security-scan.yml — Security Pipeline

### Trigger Conditions
- Push to `main` branch
- Weekly schedule (Monday 06:00 UTC)
- Manual workflow dispatch

### Jobs

| Job | Tool | Coverage |
|---|---|---|
| `secrets-scan` | TruffleHog | Git history secret detection |
| `dependency-scan` (Python) | pip-audit | Python CVEs |
| `dependency-scan` (Node.js) | npm audit | Node.js CVEs |
| `code-scan` | CodeQL | JavaScript/TypeScript + Python |
| `container-scan` | Trivy | Docker image vulnerabilities |

---

## deploy.yml — Deployment

### Trigger Conditions
- Manual workflow dispatch with environment selection

### Environments
- **Staging**: `https://staging.berunda.hack2skill.com`
- **Production**: `https://berunda.hack2skill.com`

### Jobs per Environment
1. Setup Node.js + install dependencies
2. Install Catalyst CLI
3. Deploy API functions
4. Build and deploy frontend static files
5. Deploy worker
6. Run smoke tests (health check)
7. Notify success/failure (via Slack webhook)

### Required Secrets for Deployment
- `CATALYST_PROJECT_ID`
- Catalyst credentials (managed in Catalyst Console)
- `SLACK_WEBHOOK` (for notifications)

---

## Artifacts

| Workflow | Artifact | Retention |
|---|---|---|
| `ci.yml` | Coverage reports (HTML) | Per run |
| `test.yml` | Playwright report | 7 days |
| `test.yml` | Performance results | 30 days |

---

## Failure Diagnosis

| Failure | Likely Cause | Check |
|---|---|---|
| `ruff check` fails | Python formatting/lint error | `ruff check .` locally |
| `pytest` coverage < 65% | Insufficient test coverage | `pytest --cov=src` locally |
| `vite build` fails | TypeScript error or missing dep | `cd apps/web && npm run build` |
| `docker build` fails | Dockerfile issue | `docker compose build` locally |
| `pip-audit` fails | Vulnerable Python dependency | `pip-audit --strict` locally |
| `trufflehog` fails | Secret detected in commit | Check TruffleHog output |
| `catalyst deploy` fails | Catalyst CLI config issue | Verify `catalyst.config.json` |

---

## Future CI/CD Stages (Post-Phase 1)

| Stage | Phase | Description |
|---|---|---|
| Automated deployment on merge | Phase 2 | Deploy to staging on main merge |
| Blue/green deployment | Phase 3 | Zero-downtime deployments |
| Canary releases | Phase 3 | Gradual rollout to production |
| Integration performance gates | Phase 2 | k6 threshold checks |
| License compliance check | Phase 2 | FOSSA or similar integration |
| SBOM generation | Phase 2 | Software Bill of Materials |
| Container signing | Phase 3 | Cosign signature verification |
