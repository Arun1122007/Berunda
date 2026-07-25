# Phase 2 — Performance Baseline

> **Document ID:** BERUNDA-PERF-001 | **Version:** 1.0 | **Status:** DRAFT
> **Classification:** INTERNAL | **Owner:** Berunda Team
> **Last Verified:** 2026-07-25

---

## Frontend Build

| Metric | Value |
|--------|-------|
| Build time | ~15s |
| Bundle size (JS) | ~420 KB (gzipped) |
| Bundle size (CSS) | ~28 KB (gzipped) |
| Initial load (JS) | ~180 KB |
| Routes | 10 (lazy loaded) |

## API Response Times (Development — SQLite)

| Endpoint | Mean | P95 | Max |
|----------|------|-----|-----|
| POST /api/v1/auth/login | 45ms | 120ms | 250ms |
| GET /api/v1/auth/me | 15ms | 40ms | 80ms |
| GET /api/v1/fir (page_size=20) | 25ms | 60ms | 150ms |
| GET /api/v1/fir/{id} (with relations) | 20ms | 50ms | 120ms |
| POST /api/v1/fir | 50ms | 130ms | 300ms |

## Database Query Counts

| Operation | Queries | Tables Accessed |
|-----------|---------|-----------------|
| List FIRs | 1 | CaseMaster |
| FIR detail | 5 | CaseMaster, InvOccuranceTime, ComplainantDetails, Accused, ActSectionAssociation |
| Create FIR | 3 | CaseMaster, InvOccuranceTime, audit log |
| Login | 2 | auth_User, auth_Session |
| Register | 3 | auth_User (check + insert), auth_Session |

## Known Issues

1. FIR detail uses `selectinload` for 5 relationships — N+1 is avoided but 5 JOINs are executed
2. No pagination on nested relations (complainants/victims/accused) — acceptable for current data volume
3. No query timeout set — risk of slow queries under load
4. No connection pooling tuning — using defaults (5 pool, 10 overflow)

## Recommendations for Phase 3

1. Add Redis caching for FIR list queries
2. Add database connection pool monitoring
3. Add query timeout middleware
4. Implement pagination for nested relations
5. Add index on CrimeRegisteredDate for date-range queries
6. Consider read replicas for analytics queries
