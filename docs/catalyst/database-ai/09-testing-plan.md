# 09 - Testing Plan

## Objectives
Ensure reliability, performance, and correctness of the Database and AI integration using Zoho Catalyst.

## 1. Database Unit & Integration Tests
- **Repository Interface Tests**: `pytest tests/unit/test_repositories.py` using `LocalMemoryRepository` to verify CRUD logic.
- **Catalyst Data Store Mock Tests**: Mock the `zcatalyst_sdk` to ensure ZCQL queries are formed correctly (validating syntax without hitting the remote).
- **Service Layer Tests**: Ensure `FIRService`, `EntityService`, etc. properly inject repositories and return correct schema models.

## 2. AI Unit & Integration Tests
- **Prompt Validation**: Verify prompt compilation works without injecting raw user input directly.
- **Provider Adapters**: Mock QuickML and Zia API calls to test retry behavior, circuit breakers, and timeout handling.
- **RAG End-to-end (Mocked)**: Test the extraction, embedding logic, and response synthesis using fixed payloads.

## 3. End-to-End Tests
- User Login (Auth layer).
- FIR Creation -> Job Queued for Risk Score / Anomaly -> AI Provider Invoked -> Result Stored.
- FIR Query -> RAG -> Valid Answer.

## 4. Continuous Integration
All tests will be executed on Pull Request via the CI pipeline (e.g. GitHub Actions or Catalyst Pipelines) using `pytest`. Staging deployment will only occur if all tests pass.
