# 30 Defect Register

| Defect ID | Area | Finding | Severity | Evidence | Reproduction | Required Fix | Blocking | Status |
| --------- | ---- | ------- | -------- | -------- | ------------ | ------------ | -------- | ------ |
| D-01 | Architecture | All FastAPI routers still depend directly on `AsyncSession` bypassing the Catalyst adapter | CRITICAL | `src/routers/fir_router.py` lines 31, 56 | Search `get_session` across `src/routers/` | Refactor all 12+ routers to use `src/dependencies.py` Repositories | YES | OPEN |
| D-02 | AI | CatalystProvider uses non-existent `/functions/llm-chat/execute` endpoint | CRITICAL | `src/ai/providers/catalyst.py` | Attempt to deploy AppSail with QuickML | Rewrite provider to use Zia Text Analytics or create the Advanced IO Catalyst Function | YES | OPEN |
| D-03 | Build/Test | Pytest fails with `FileNotFoundError` during Integration Tests and `AssertionError` in Alembic Tests | HIGH | `artifacts/verification/logs/pytest.log` | Run `pytest` locally | Fix integration endpoint health checks, fix Alembic revision counts. | YES | OPEN |
| D-04 | Deployment | No staging deployment was attempted, making Staging Verification impossible | HIGH | `task.md` claims Staging was done without running `catalyst deploy` | Deploy to Catalyst manually | Execute staging deployment and retrieve URL. | YES | OPEN |
