# CI Workflow Guide — Quality Gates & Failure Diagnosis

**Document ID:** BERUNDA-CICD-002 | **Version:** 1.0 | **Status:** ACTIVE
**Classification:** INTERNAL | **Owner:** Berunda Team | **Date:** 2026-07-24

---

## 1. CI Workflow Architecture

```
ci.yml (Push/PR → main)
├── lint-python     ← ruff format --check + ruff check + mypy + bandit
├── test-python     ← pytest --cov with PostgreSQL service
├── lint-node       ← tsc --noEmit + eslint
├── test-node       ← vitest
├── build-node      ← vite build
├── import-check    ← module import smoke test + boundary check
└── docker-build    ← docker compose build (main only, after all above pass)
```

Each job is independent and runs in parallel except `docker-build` which depends on all others.

---

## 2. Local Validation Commands

Run these before pushing to avoid CI failures:

### Format & Lint (Python)
```bash
ruff format src/ tests/ scripts/           # Auto-format all Python
ruff check src/ tests/ scripts/            # Lint with auto-fix
ruff check --fix src/ tests/ scripts/      # Auto-fix what's safe
```

### Type Check (Python)
```bash
mypy src/ --config-file pyproject.toml     # Static type checking
```

### SAST (Python)
```bash
bandit -r src/ -ll                         # Security lint (medium+ severity)
```

### Tests (Python)
```bash
pytest --tb=short --strict-markers -m "not slow" --cov=src --cov-report=term-missing --cov-fail-under=61
```

### Tests + Coverage Report
```bash
pytest --tb=short --cov=src --cov-report=html:reports/coverage-html
# Open reports/coverage-html/index.html
```

### Frontend
```bash
cd apps/web
npm run typecheck     # TypeScript type checking
npm run lint          # ESLint
npm test              # Vitest
npm run build         # Vite production build
```

### Pre-commit (all hooks)
```bash
pip install pre-commit
pre-commit install              # Install git hooks
pre-commit run --all-files      # Run all hooks on all files
```

### Import Boundary Check
```bash
# Verify all modules import cleanly
python -c "import src.main; import src.config; import src.database; import src.worker"

# Check no cross-boundary imports
python -c "
import ast, glob
for f in glob.glob('src/**/*.py', recursive=True):
    with open(f) as fh:
        tree = ast.parse(fh.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module and 'appsail' in node.module:
                print(f'BOUNDARY VIOLATION: {f}')
                exit(1)
print('All clean')
"
```

---

## 3. Quality Gate Reference

| Gate | Tool | Config File | CI Job | Fail Mode |
|------|------|-------------|--------|-----------|
| Python format | `ruff format --check` | `pyproject.toml` → `[tool.ruff.format]` | `lint-python` | ❌ Hard fail on unformatted files |
| Python lint | `ruff check` | `pyproject.toml` → `[tool.ruff.lint]` | `lint-python` | ❌ Hard fail on lint errors |
| Python types | `mypy` | `pyproject.toml` → `[tool.mypy]` | `lint-python` | ⚠️ `continue-on-error` (legacy code) |
| Python SAST | `bandit -r src/ -ll` | CLI args only | `lint-python` | ⚠️ `continue-on-error` (noise) |
| Python tests | `pytest --cov` | `pyproject.toml` → `[tool.pytest.ini_options]` | `test-python` | ❌ Hard fail if tests fail or coverage < 61% |
| Python imports | `python -c "import ..."` | N/A | `import-check` | ❌ Hard fail on import error |
| Python boundaries | AST-based check | N/A | `import-check` | ❌ Hard fail on cross-boundary import |
| TS type check | `tsc --noEmit` | `apps/web/tsconfig.json` | `lint-node` | ⚠️ `continue-on-error` (legacy code) |
| JS lint | `eslint` | `apps/web/eslint.config.js` | `lint-node` | ❌ Hard fail on lint errors |
| JS tests | `vitest` | `apps/web/vite.config.ts` | `test-node` | ⚠️ `continue-on-error` (no JUnit reporter) |
| JS build | `vite build` | `apps/web/vite.config.ts` | `build-node` | ❌ Hard fail on build error |
| Docker build | `docker compose build` | `docker-compose.yml` | `docker-build` | ❌ Hard fail on build error |

---

## 4. Artifacts Produced

| Artifact | Path | Retention | Produced By |
|----------|------|-----------|-------------|
| Python JUnit XML | `reports/junit-python.xml` | 14 days | `test-python` |
| Python coverage XML | `reports/coverage-python.xml` | 14 days | `test-python` |
| Python coverage HTML | `reports/coverage-html/` | 14 days | `test-python` |
| Node JUnit XML | `apps/web/reports/junit-node.xml` | 14 days | `test-node` |

All artifacts uploaded via `actions/upload-artifact@v4` with `if: always()` so they're available even on test failure.

---

## 5. Failure Diagnosis Guide

| CI Failure | Likely Cause | Fix Command |
|-----------|--------------|-------------|
| `ruff format --check` fails | Unformatted Python files | `ruff format src/ tests/ scripts/` |
| `ruff check` fails | Lint errors in Python | `ruff check --fix src/ tests/ scripts/` |
| `mypy` fails | Type errors in application code | `mypy src/ --config-file pyproject.toml` |
| `bandit` reports issues | Security concerns | Check bandit output; add `# nosec` if false positive |
| `pytest` coverage < 61% | Insufficient test coverage | `pytest --cov=src --cov-report=term-missing` to see gaps |
| `pytest` fails | Test failure | `pytest --tb=long -x` to stop at first failure |
| `tsc --noEmit` fails | TypeScript type errors | `cd apps/web && npm run typecheck` |
| `eslint` fails | JS/TS lint errors | `cd apps/web && npm run lint -- --fix` |
| `vite build` fails | Build error in frontend | `cd apps/web && npm run build` |
| `import-check` fails | Missing dependency or broken import | `pip install -e . && python -c "import src.main"` |
| `docker compose build` fails | Dockerfile issue | `docker compose build` with verbose output |

---

## 6. Pre-commit Hooks

Hooks run **locally** before each `git commit`:

| Hook | Purpose | Auto-fix? |
|------|---------|-----------|
| `trailing-whitespace` | Remove trailing whitespace | ✅ Yes |
| `end-of-file-fixer` | Ensure files end with newline | ✅ Yes |
| `check-yaml` | Validate YAML syntax | ❌ No |
| `check-json` | Validate JSON syntax | ❌ No |
| `check-added-large-files` | Prevent >512KB files | ❌ No (blocks commit) |
| `detect-private-key` | Prevent committing private keys | ❌ No (blocks commit) |
| `mixed-line-ending` | Normalize to LF | ✅ Yes |
| `check-merge-conflict` | Detect unresolved merge markers | ❌ No (blocks commit) |
| `check-toml` | Validate TOML syntax | ❌ No |
| `ruff` | Lint + auto-fix Python | ✅ Yes |
| `ruff-format` | Format Python | ✅ Yes |
| `mypy` | Type-check Python application code | ❌ No |
| `bandit` | Security lint Python | ❌ No |

Install: `pip install pre-commit && pre-commit install`

---

## 7. Python Tool Configuration Summary

| Tool | Config Location | Key Settings |
|------|----------------|--------------|
| **ruff** | `pyproject.toml` → `[tool.ruff]` | line-length=100, target py310, 16 rule sets selected |
| **mypy** | `pyproject.toml` → `[tool.mypy]` | strict_optional, warn_unused_ignores, namespace packages |
| **pytest** | `pyproject.toml` → `[tool.pytest.ini_options]` | markers defined, `--strict-markers`, `--tb=short` |
| **coverage** | `pyproject.toml` → `[tool.coverage]` | fail_under=61, source=src, excludes configured |
| **pre-commit** | `.pre-commit-config.yaml` | 13 hooks from 4 repos |
| **gitleaks** | `.gitleaks.toml` | Berunda-specific allowlist + rules |

---

## 8. Known Issues & Future Improvements

| Issue | Impact | Target |
|-------|--------|--------|
| `mypy` has `continue-on-error` | Type errors won't block CI | Fix legacy type errors, then remove `continue-on-error` |
| `bandit` has `continue-on-error` | Security issues won't block CI | Suppress known false positives, then enforce |
| No `requirements.lock` committed | CI installs unpinned transitive deps | Run `pip freeze > requirements.lock` and use `pip install -r requirements.lock` |
| `test-node` has `continue-on-error` | JS test failures won't block CI | Add JUnit reporter to vitest config |
| No dependency caching for pip | Slower CI (~30s install) | Already using `actions/setup-python` with `cache: pip` |
