.PHONY: setup dev build test test-unit test-integration lint lint-fix typecheck clean \
        docker-build docker-up docker-down docker-logs security-check help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install all dependencies (Python + Node)
	pip install -r requirements.txt
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

test: ## Run all tests
	pytest --tb=short -x --cov=src --cov-report=term-missing
	cd apps/web && npm test

test-unit: ## Run unit tests only
	pytest -m unit --tb=short -x --cov=src --cov-report=term-missing

test-integration: ## Run integration tests only
	pytest -m integration --tb=short -x --cov=src --cov-report=term-missing

lint: ## Run all linters
	ruff check src/ tests/ scripts/
	ruff format --check src/ tests/ scripts/
	cd apps/web && npm run lint

lint-fix: ## Auto-fix lint issues
	ruff check --fix src/ tests/ scripts/
	ruff format src/ tests/ scripts/

typecheck: ## Run type checkers
	mypy src/ --ignore-missing-imports

clean: ## Remove build artifacts
	rm -rf apps/web/dist
	rm -rf apps/api/dist
	rm -rf apps/worker/dist
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage coverage htmlcov

security-check: ## Run security audits
	@echo "Running security checks..."
	-pip-audit --strict 2>/dev/null || echo "pip-audit not available"
	-cd apps/web && npm audit --audit-level=high 2>/dev/null || true

docker-build: ## Build Docker images
	docker-compose build

docker-up: ## Start Docker Compose services
	docker-compose up -d

docker-down: ## Stop Docker Compose services
	docker-compose down

docker-logs: ## View Docker Compose logs
	docker-compose logs -f
