# End-to-End Tests

Full-stack tests that validate the complete system from browser to backend.

- **Framework**: Playwright
- **Markers**: `@pytest.mark.e2e`
- **Run**: `pytest -m e2e -v` or `npx playwright test`
- **Setup**: Requires running application (see `docker-compose up`)
- **Coverage**: Critical user journeys: login → import FIR → view graph → query RAG
