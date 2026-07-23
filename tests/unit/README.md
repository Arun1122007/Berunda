# Unit Tests

Fast, isolated tests that validate individual functions and classes.

- **Framework**: pytest
- **Markers**: `@pytest.mark.unit`
- **Run**: `pytest -m unit -v`
- **Coverage target**: Core modules >= 90%, AI/ML >= 85%
- **No external dependencies**: All external services are mocked via `tests/conftest.py` fixtures
- **Deterministic**: Use `tests/fixtures/` data files for consistent results
