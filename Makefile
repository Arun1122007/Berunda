.PHONY: install dev-backend dev-frontend test test-unit test-api lint typecheck seed-demo reset-demo evaluate-ai clean

# ==============================================================================
# Berunda Local Development Makefile
# ==============================================================================

# Install all dependencies (backend + frontend)
install:
	python -m pip install -r requirements.txt
	cd apps/web && npm install

# Start Backend locally using uvicorn
dev-backend:
	uvicorn src.main:app --host 0.0.0.0 --port 9000 --reload

# Start Frontend locally using Vite
dev-frontend:
	cd apps/web && npm run dev

# Run all test suites
test:
	pytest tests/

# Run unit tests only
test-unit:
	pytest tests/unit/

# Run API component tests only
test-api:
	pytest tests/api/

# Run linter on backend and frontend
lint:
	ruff check src/ tests/
	cd apps/web && npm run lint

# Run type checks on backend and frontend
typecheck:
	mypy src/ --ignore-missing-imports
	cd apps/web && npm run typecheck

# Seed the database with synthetic demo data
seed-demo:
	python scripts/data/generate_synthetic.py --tier demo

# Reset the database demo data idempotently
reset-demo:
	python scripts/data/generate_synthetic.py --tier demo --idempotent

# Run AI evaluation metrics
evaluate-ai:
	python scripts/validation/eval_ner.py

# Clean Python bytecode and cache
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
