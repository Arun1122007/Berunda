# Testing Strategy

## Test Categories

| Category | Tool | Location | Marks |
|----------|------|----------|-------|
| **Unit** | pytest, vitest | `tests/unit/` | `unit` |
| **Integration** | pytest, httpx | `tests/integration/` | `integration` |
| **End-to-End** | Playwright | `tests/e2e/` | `e2e` |
| **Performance** | k6 | `tests/performance/` | `performance` |
| **Security** | OWASP ZAP | `tests/security/` | `security` |

## Running Tests

### All tests

```powershell
# Python
pytest tests/ -v

# Node
npx vitest run
```

### Unit tests only

```powershell
pytest tests/ -v -m "unit"
npx vitest run --reporter=verbose
```

### Integration tests

```powershell
pytest tests/integration/ -v -m "integration"
```

### With coverage

```powershell
pytest tests/ --cov=. --cov-report=html --cov-fail-under=80
```

### Slow tests

```powershell
pytest tests/ -v -m "slow" --runslow
```

## Test Naming Conventions

- **Files**: `test_<module>.py` or `<module>.test.ts`
- **Classes**: `Test<Component>`
- **Functions**: `test_<feature>_<scenario>`

## Coverage Requirements

- **Overall**: 80%+
- **Core modules** (`src/`, `apps/api/`): 90%+
- **AI/ML modules** (`src/ai/`, `src/ml/`): 85%+
- **UI components**: 70%+

## Test Data

Synthetic test data is in `tests/fixtures/`:

| File | Description |
|------|-------------|
| `sample-fir.json` | Synthetic FIR records for testing |
| `sample-entities.json` | Entity resolution test data |
| `crime-types.csv` | Standard crime type codes |
