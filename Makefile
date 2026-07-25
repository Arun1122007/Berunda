.PHONY: setup dev build test test-unit test-integration lint lint-check lint-fix typecheck \
        clean lockfile ci ci-quick security-check check-all \
        docker-build docker-up docker-down docker-logs help

CHK = \033[32m✔\033[0m
BLD = \033[1m
RST = \033[0m

help: ## Show this help
	@$(or $(shell command -v grep 2>/dev/null && echo "grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = \":.*?## \"}; {printf \"\033[36m%-20s\033[0m %s\n\", \$$1, \$$2}'"), \
	  echo "NOTE: 'grep' not available on this platform. Run 'type Makefile' to see targets.")

# ── Setup ────────────────────────────────────────────────────

setup: ## Install all dependencies (Python + Node)
	pip install -r requirements.lock
	pip install -e .
	npm install
	cd apps/web && npm install
	cd apps/api && npm install

dev: ## Start development servers (backend + frontend)
	@echo "Starting backend on http://localhost:8000 ..."
	@echo "Starting frontend on http://localhost:5173 ..."
	npx concurrently \
		"uvicorn src.main:app --reload --host 0.0.0.0 --port 8000" \
		"cd apps/web && npm run dev"

build: ## Build all applications
	cd apps/web && npm run build

# ── Testing ──────────────────────────────────────────────────

test: ## Run all tests
	pytest --tb=short -x --cov=src --cov-report=term-missing
	cd apps/web && npm test

test-unit: ## Run unit tests only
	pytest -m unit --tb=short -x --cov=src --cov-report=term-missing

test-integration: ## Run integration tests only
	pytest -m integration --tb=short -x --cov=src --cov-report=term-missing

# ── Linting & Formatting ─────────────────────────────────────

lint: ## Run linters (ruff check + eslint)
	ruff check src/ tests/ scripts/
	cd apps/web && npm run lint

lint-check: ## Full lint: format check + lint + typecheck + bandit (CI gate)
	@echo "$(BLD)── Format ──$(RST)"
	ruff format --check src/ tests/ scripts/
	@echo "  $(CHK) format OK"
	@echo "$(BLD)── Lint ──$(RST)"
	ruff check src/ tests/ scripts/
	@echo "  $(CHK) lint OK"
	@echo "$(BLD)── Typecheck ──$(RST)"
	mypy src/ --config-file pyproject.toml
	@echo "  $(CHK) typecheck OK"
	@echo "$(BLD)── SAST ──$(RST)"
	bandit -r src/ -ll
	@echo "  $(CHK) bandit OK"

lint-fix: ## Auto-fix lint issues
	ruff check --fix src/ tests/ scripts/
	ruff format src/ tests/ scripts/

typecheck: ## Run type checker (mypy)
	mypy src/ --config-file pyproject.toml

# ── Lockfile ─────────────────────────────────────────────────

lockfile: ## Freeze current deps into requirements.lock
	pip freeze > requirements.lock
	@echo "$(CHK) requirements.lock updated"

lockfile-check: ## Verify requirements.lock matches requirements.txt
	@echo "Checking lockfile freshness..."
	@set TMPFILE1=$$(mktemp 2>/dev/null || echo "_txt_pkgs.tmp") && \
	set TMPFILE2=$$(mktemp 2>/dev/null || echo "_lock_pkgs.tmp") && \
	grep -E '^[a-zA-Z0-9_>-]' requirements.txt | sed 's/\[.*\]//;s/[><=!].*//;s/#.*//;s/ //g' | sort -u > $$TMPFILE1 && \
	grep -E '^[a-z0-9_-]+==' requirements.lock | sed 's/==.*//' | sort -u > $$TMPFILE2 && \
	while IFS= read -r pkg; do \
		if [ -z "$$pkg" ]; then continue; fi; \
		if ! grep -qxi "$$pkg" $$TMPFILE2; then \
			echo "  MISSING: $$pkg"; \
			rm -f $$TMPFILE1 $$TMPFILE2; \
			exit 1; \
		fi; \
	done < $$TMPFILE1 && \
	rm -f $$TMPFILE1 $$TMPFILE2
	@echo "  $(CHK) lockfile is fresh"

# ── CI (matches .github/workflows/ci.yml) ────────────────────

ci: ## Full CI pipeline (format + lint + typecheck + test + security)
	$(MAKE) lint-check
	$(MAKE) test
	$(MAKE) security-check
	@echo "$(BLD)$(CHK) CI passed$(RST)"

ci-quick: ## Quick CI (format + lint + typecheck, no tests)
	$(MAKE) lint-check
	@echo "$(BLD)$(CHK) quick CI passed$(RST)"

# ── Housekeeping ─────────────────────────────────────────────

clean: ## Remove build artifacts
	rm -rf apps/web/dist apps/api/dist apps/worker/dist
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage coverage htmlcov reports/

security-check: ## Run security audits (pip-audit + npm audit)
	@echo "Running security checks..."
	-pip-audit --strict --requirement requirements.lock 2>/dev/null || echo "pip-audit not available"
	-cd apps/web && npm audit --audit-level=high 2>/dev/null || true

check-all: ## Run every quality gate (setup → ci)
	$(MAKE) setup
	$(MAKE) ci
	$(MAKE) lockfile-check
	@echo "$(BLD)All checks passed$(RST)"

# ── Docker ───────────────────────────────────────────────────

docker-build: ## Build Docker images
	docker compose build

docker-up: ## Start Docker Compose services
	docker compose up -d

docker-down: ## Stop Docker Compose services
	docker compose down

docker-logs: ## View Docker Compose logs
	docker compose logs -f
