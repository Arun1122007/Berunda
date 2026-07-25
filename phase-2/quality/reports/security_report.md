# Security Validation Report

**Project:** Berunda — AI-Native Crime Intelligence Platform
**Date:** {{DATE}}
**Run ID:** {{RUN_ID}}

---

## Summary

| Category | Passed | Failed | Skipped | Status |
|----------|--------|--------|---------|--------|
| Secret Scanning | {{SECRETS_PASSED}} | {{SECRETS_FAILED}} | {{SECRETS_SKIPPED}} | {{SECRETS_STATUS}} |
| Auth Behavior | {{AUTH_PASSED}} | {{AUTH_FAILED}} | {{AUTH_SKIPPED}} | {{AUTH_STATUS}} |
| Authorization (RBAC) | {{AUTHZ_PASSED}} | {{AUTHZ_FAILED}} | {{AUTHZ_SKIPPED}} | {{AUTHZ_STATUS}} |
| Input Validation | {{INPUT_PASSED}} | {{INPUT_FAILED}} | {{INPUT_SKIPPED}} | {{INPUT_STATUS}} |
| CORS Configuration | {{CORS_PASSED}} | {{CORS_FAILED}} | {{CORS_SKIPPED}} | {{CORS_STATUS}} |
| Security Headers | {{HEADERS_PASSED}} | {{HEADERS_FAILED}} | {{HEADERS_SKIPPED}} | {{HEADERS_STATUS}} |
| Rate Limiting | {{RATELIMIT_PASSED}} | {{RATELIMIT_FAILED}} | {{RATELIMIT_SKIPPED}} | {{RATELIMIT_STATUS}} |
| Request Size Limits | {{SIZE_PASSED}} | {{SIZE_FAILED}} | {{SIZE_SKIPPED}} | {{SIZE_STATUS}} |
| **Overall** | **{{TOTAL_PASSED}}** | **{{TOTAL_FAILED}}** | **{{TOTAL_SKIPPED}}** | **{{OVERALL_STATUS}}** |

---

## Detail: Secret Scanning

| Check | Result | Detail |
|-------|--------|--------|
{{SECRETS_DETAILS}}

## Detail: Auth Behavior

| Endpoint | Status |
|----------|--------|
{{AUTH_DETAILS}}

## Detail: Authorization (RBAC)

| Test | Status | Detail |
|------|--------|--------|
{{AUTHZ_DETAILS}}

## Detail: Input Validation

| Input | Status |
|-------|--------|
{{INPUT_DETAILS}}

---

## Security Headers

| Header | Expected | Present | Value |
|--------|----------|---------|-------|
{{HEADERS_DETAILS}}

---

## Failed Item Details

{{FAILED_DETAILS}}

---

## Recommendations

{{RECOMMENDATIONS}}
