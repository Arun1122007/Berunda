# 31 Reverification Plan

This document outlines the required remediation for all Critical, High, and Medium findings in the Defect Register.

## D-01: FastAPI Router Dependency Injection
**Required Code Change:** 
- Open `src/routers/*.py`.
- Replace `session: AsyncSession = Depends(get_session)` with `repo: FIRRepository = Depends(get_fir_repo)`.
- Update corresponding Service layer (e.g. `src/services/fir_service.py`) to accept `FIRRepository` instead of `AsyncSession`.
**Required Test:** Ensure `pytest` passes with the mocked `SQLiteFIRRepository`.
**Reverification Status:** NOT STARTED.

## D-02: Catalyst AI Provider
**Required Code Change:** 
- Open `src/ai/providers/catalyst.py`.
- Remove `httpx` POST to `/functions/llm-chat/execute`.
- Initialize `app.zia()` and use official APIs, OR generate a new Catalyst Function via `catalyst init` and implement the chat handler in Java/Node/Python to broker the LLM request.
**Required Test:** Test against an active Catalyst environment.
**Reverification Status:** NOT STARTED.

## D-03: Pytest Failures
**Required Code Change:** 
- Fix `AlembicRevisionChain` test by either consolidating the migration scripts or updating the expected revision counts.
- Investigate `FileNotFoundError` in integration tests (likely due to missing `.env.test` or improper mocking of an OS path).
**Required Test:** `pytest` exits with code 0.
**Reverification Status:** NOT STARTED.

## D-04: Catalyst Staging Deployment
**Required Code Change:** 
- Successfully execute `catalyst deploy` from the root directory.
- Verify AppSail allocates memory properly.
**Required Test:** Access the deployed URL and test a basic CRUD operation.
**Reverification Status:** NOT STARTED.
