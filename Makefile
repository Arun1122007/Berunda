.PHONY: test lint build-web run-dev install

VENV = .venv
PYTHON = $(VENV)\Scripts\python
PIP = $(VENV)\Scripts\pip
NPM = npm.cmd

test:
	$(PYTHON) -m pytest tests/ -v --tb=short

lint:
	ruff check src/

lint-fix:
	ruff check --fix src/

typecheck:
	mypy src/

install:
	$(PIP) install -r requirements.txt

dev:
	$(PYTHON) -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

build-web:
	cd apps\web && $(NPM) run build

install-web:
	cd apps\web && $(NPM) install

run-web:
	cd apps\web && $(NPM) run dev

check:
	$(PYTHON) -c "from src.main import app; print('Import OK')"

all: check lint test
