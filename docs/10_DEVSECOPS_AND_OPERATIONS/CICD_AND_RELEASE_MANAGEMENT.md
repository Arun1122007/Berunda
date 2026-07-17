# CI/CD and Release Management

[//]: # (Document ID: BERUNDA-OPS-002 | Status: DRAFT | Classification: INTERNAL)

---

## 1. CI/CD Pipeline

| Stage | Tool | Trigger | Duration (est.) |
|-------|------|---------|-----------------|
| 1. Lint | Ruff (Python), ESLint (JS) | Push to any branch | 1 min |
| 2. Unit tests | pytest + Jest | Push to main / PR | 3 min |
| 3. Build | Catalyst Pipelines | Merge to main | 5 min |
| 4. Deploy (Testing) | Catalyst Pipelines | Build success | 5 min |
| 5. Integration tests | pytest | Deploy to Testing success | 5 min |
| 6. Security scan | OWASP ZAP + pip-audit | Weekly schedule | 10 min |
| 7. Deploy (Staging) | Catalyst Pipelines | Tagged release (v*.*.*) | 5 min |
| 8. Acceptance tests | Playwright | Deploy to Staging success | 5 min |
| 9. Manual approval | GitHub + Team Lead | Acceptance tests pass | Variable |
| 10. Deploy (Production) | Catalyst Pipelines | Manual approval | 5 min |

## 2. Branch Strategy

| Branch | Purpose | Protection | Deploys To |
|--------|---------|------------|------------|
| `main` | Stable, always deployable | Required PR review + passing CI | Testing |
| `develop` | Daily work branch | None | Development |
| `feature/*` | Feature branches | None | Manual |
| `hotfix/*` | Urgent fixes to main | Required PR review | Testing → Staging |

## 3. Release Process

| Step | Action | Owner |
|------|--------|-------|
| 1 | Create GitHub release with tag `v{major}.{minor}.{patch}` (e.g., `v1.0.0`) | Developer |
| 2 | CI/CD automatically deploys to Staging | Automation |
| 3 | Run full acceptance test suite | Developer |
| 4 | Team lead reviews acceptance test results | Team Lead |
| 5 | If passed: manual approval gate in Catalyst Pipelines | Team Lead |
| 6 | Deploy to Production | Automation |
| 7 | Run smoke tests against Production | Developer |
| 8 | Tag release in git with `v{major}.{minor}.{patch}` | Automation |

## 4. Versioning

| Component | Version Scheme | Example |
|-----------|---------------|---------|
| Application | Semver | v1.0.0 |
| Synthetic dataset | Major.Minor | v1.0 |
| Risk scoring model | Semver | v1.0.0 |
| Database schema | Date-based | V20260716 |
| API | URL path | /api/v1/ |

## 5. Rollback Strategy

| Scenario | Rollback Action | RTO | RPO |
|----------|----------------|-----|-----|
| Buggy code deployed | Revert git commit + redeploy from last stable tag | 15 min | N/A |
| Bad data import | Clear int_* tables, re-run seed script from dataset version | 30 min | N/A |
| Schema migration failed | Run revert migration script, fix, re-run forward migration | 30 min | N/A |
| Configuration error | Restore previous config from Stratus backup | 5 min | N/A |

## 6. Secrets and Credentials

| Secret | Stored In | Accessed By |
|--------|-----------|-------------|
| Catalyst project credentials | Catalyst managed | Catalyst Pipelines |
| API keys (external) | Catalyst Stratus (encrypted) | Application at runtime |
| JWT signing keys | Catalyst Authentication | Catalyst managed |
| Database connection strings | Catalyst Data Store connection | Catalyst managed |
