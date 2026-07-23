# Integration Tests

Tests that validate interactions between components with real or containerized dependencies.

- **Framework**: pytest + httpx
- **Markers**: `@pytest.mark.integration`
- **Run**: `pytest -m integration -v`
- **Dependencies**: PostgreSQL (testcontainers), Redis (testcontainers)
- **Fixtures**: Provided in `tests/integration/conftest.py`
- **Database**: Transaction rollback after each test for isolation
