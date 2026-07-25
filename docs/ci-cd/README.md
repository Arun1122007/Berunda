# Berunda CI/CD

## Overview

Berunda uses **GitHub Actions** for continuous integration. Every push/PR to `main` triggers automated quality gates across the Python backend and Node.js frontend.

## Workflows

| Workflow | File | Trigger | Purpose |
|----------|------|---------|---------|
| **CI** | `.github/workflows/ci.yml` | Push/PR to `main` | Full quality gate: lint, typecheck, test, build, import check, docker |
| **Full Test Suite** | `.github/workflows/test.yml` | Any PR + manual | Extended tests: unit, integration, e2e, performance |
| **Security Scan** | `.github/workflows/security-scan.yml` | Push/PR to `main` + weekly | Secrets scan, pip-audit, npm audit, CodeQL |
| **Deploy** | `.github/workflows/deploy.yml` | Manual dispatch | Build and deploy to staging/production |

## CI Pipeline (`ci.yml`) — What Runs

### 1. Lockfile Check
Verifies `requirements.lock` contains every package listed in `requirements.txt`. If stale, run `make lockfile` to regenerate.

### 2. Lint & Type (Python)
- `ruff format --check` — formatting conformance
- `ruff check` — lint rules (E, W, F, I, N, UP, D, SIM, ARG, RUF)
- `mypy` — static type checking
- `bandit` — SAST security scan

### 3. Test (Python)
- `pytest` with coverage (`--cov-fail-under=61`)
- PostgreSQL 16 service container
- JUnit XML + Cobertura XML + HTML reports uploaded as artifacts

### 4. Lint, Test & Build (Node.js)
- TypeScript type checking
- ESLint
- Test with JUnit reports
- `npm run build`

### 5. Import / Boundary Check
- Verifies all application modules import cleanly
- Scans for cross-boundary imports (e.g., `appsail` in `src/`)

### 6. Docker Build (main branch only)
- `docker compose build` — only if all preceding jobs pass

## Quality Gates (Hard Failures)

| Gate | Fail Condition |
|------|---------------|
| Ruff format | Any unformatted file |
| Ruff lint | Any lint error (except per-file ignores) |
| mypy | Any type error |
| bandit | Any issue with severity >= LOW |
| pytest | Any test failure or coverage < 61% |
| Import check | Any module fails to import or boundary violation |
| Lockfile check | Package missing from `requirements.lock` |

> **Note:** Frontend typecheck uses `continue-on-error` — informational only.

## Local Validation

### One-shot full CI
```bash
make ci
```

### Quick (no tests)
```bash
make ci-quick
```

### Individual gates
```bash
make lint-check        # format + lint + typecheck + bandit
make lint              # ruff check only
make typecheck         # mypy only
make test              # pytest + npm test
make security-check    # pip-audit + npm audit
make lockfile-check    # verify lockfile freshness
```

### Windows (PowerShell)
```powershell
.\berunda.ps1 ci       # lint + typecheck + test
.\berunda.ps1 lint     # ruff + eslint
.\berunda.ps1 typecheck # mypy + tsc
.\berunda.ps1 lockfile  # regenerate requirements.lock
```

### Pre-commit (local)
```bash
pip install pre-commit
pre-commit install     # installs git hooks
pre-commit run --all-files  # run once on everything
```

## Lockfile Strategy

`requirements.lock` is **tracked in git** for reproducible installs.

### Update the lockfile
```bash
# After adding/removing packages in requirements.txt:
pip install -r requirements.txt
make lockfile           # pip freeze > requirements.lock
git add requirements.lock
git commit -m "chore(deps): update requirements.lock"
```

### Dependency management workflow
1. Edit `requirements.txt` (add/remove/update pins)
2. `pip install -r requirements.txt && make lockfile`
3. Commit both `requirements.txt` and `requirements.lock` together
4. CI verifies lockfile is fresh in the `lockfile-check` job

## Failure Diagnosis

### CI is red — what now?

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `ruff format` fails | Code not formatted | `make lint-fix` |
| `ruff check` fails | Lint violations | `ruff check --fix` then review |
| `mypy` fails | Type annotation error | Read mypy output, fix type hints |
| `bandit` fails | Security issue | Review bandit output, add `# nosec` if false positive |
| `pytest` fails | Test failure | `pytest --tb=long -x` to see full traceback |
| Coverage < 61% | Insufficient coverage | Add tests for uncovered code |
| `lockfile-check` fails | Lockfile stale | `make lockfile` and commit |
| Import check fails | Broken import or boundary violation | Check the module path or remove forbidden import |

### Reports (CI artifacts)
- **JUnit XML**: `reports/junit-python.xml` — import into CI dashboard
- **Coverage XML**: `reports/coverage-python.xml` — for coverage tools
- **Coverage HTML**: `reports/coverage-html/` — open in browser
- **Node reports**: `apps/web/reports/junit-node.xml`
