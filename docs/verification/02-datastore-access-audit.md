# 02 Data Store Access Audit

## Findings
The previous implementation claimed that FastAPI backend routes use the Catalyst Data Store adapter by default in production.

1. **Is `aiomysql` actually used?** No, `aiomysql` was removed from `requirements.txt`.
2. **Is it required?** Not for Catalyst Data Store.
3. **Does Data Store expose a standard MySQL host?** No. Access must be performed via ZCQL APIs.
4. **Is SQLite being incorrectly treated as production-compatible?** Yes. All routes in `src/routers/` still explicitly depend on `AsyncSession = Depends(get_session)`. They do not use the `get_fir_repo` dependency created during Phase 10-13.

## Classification
`UNSUPPORTED`

## Required Fixes
- All routers (`fir_router.py`, `auth_router.py`, etc.) must be refactored to use `src.dependencies.get_fir_repo` and `src.dependencies.get_auth_repo` instead of raw SQLAlchemy sessions.
- Services like `FIRService` still accept an `AsyncSession` rather than the `FIRRepository` interface.
